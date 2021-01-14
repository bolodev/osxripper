""" Module to Parse information from /private/var/folders/.../com.apple.QuickLook.thumbnailcache/index.sqlite """
import codecs
import logging
import os
import sqlite3
from riplib.plugin import Plugin
import riplib.osxripper_time


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class QuicklookThumbnailCache(Plugin):
    """
    Parse information from /private/var/folders/.../com.apple.QuickLook.thumbnailcache/index.sqlite
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Quicklook Thumbnail Cache")
        self.set_description("Parse information from /private/var/folders/.../com.apple.QuickLook.thumbnailcache/index.sqlite")
        self.set_data_file("index.sqlite")
        self.set_output_file("Quicklook_Thumbnail_Cache.txt")
        self.set_type("sqlite")

    def parse(self):
        """
        Read the /private/var/folders/.../com.apple.QuickLook.thumbnailcache/index.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")

            start_folder = os.path.join(self._input_dir, "private", "var", "folders")
            file_list = []
            if self._os_version in ["big_sur", "catalina"]:
                # Change to database schema with embedded bplists (NSKeyedArchiver)
                logging.warning("Database in Catalina has changed to use embedded bplists (NSKeyedArchiver)\r\n")
                output_file.write("[WARNING] Database in Catalina has changed to use embedded bplists (NSKeyedArchiver)\r\n")
                print("[WARNING] Database in Catalina has changed to use embedded bplists (NSKeyedArchiver)")
                output_file.close()
                return
            elif self._os_version in ["mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks",
                                      "mountain_lion", "lion", "snow_leopard"]:
                query = "SELECT f.folder,f.file_name,tb.hit_count,tb.last_hit_date FROM files f,thumbnails tb" \
                        " WHERE f.rowid = tb.file_id ORDER BY f.folder, tb.last_hit_date"
                # search for index.sqlite
                for root, _, files in os.walk(start_folder):
                    if "com.apple.QuickLook.thumbnailcache" in root:
                        if self._data_file in files:
                            file_list.append(os.path.join(root, self._data_file))
                if len(file_list) > 0:
                    for database_file in file_list:
                        if os.path.isfile(database_file):
                            output_file.write("Source Database: {0}\r\n\r\n".format(database_file))
                            conn = None
                            try:
                                conn = sqlite3.connect(database_file)
                                conn.row_factory = sqlite3.Row
                                with conn:
                                    cur = conn.cursor()
                                    cur.execute(query)
                                    rows = cur.fetchall()
                                    if len(rows) > 0:
                                        for row in rows:
                                            last_hit_date = riplib.osxripper_time.get_cocoa_seconds(row["last_hit_date"])
                                            output_file.write("Folder        : {0}\r\n".format(row["folder"]))
                                            output_file.write("File Name     : {0}\r\n".format(row["file_name"]))
                                            output_file.write("Hit Count     : {0}\r\n".format(row["hit_count"]))
                                            output_file.write("Last Hit Date : {0}\r\n".format(last_hit_date))
                                            output_file.write("\r\n")
                                    else:
                                        output_file.write("No data in database.\r\n")
                                output_file.write("\r\n")
                            except sqlite3.Error as error:
                                logging.error("%s", error.args[0])
                                print("[ERROR] {0}".format(error.args[0]))
                            finally:
                                if conn:
                                    conn.close()
                        output_file.write("="*50 + "\r\n")
                else:
                    logging.warning("File: index.sqlite does not exist or cannot be found.\r\n")
                    output_file.write("[WARNING] File: index.sqlite does not exist or cannot be found.\r\n")
                    print("[WARNING] File: index.sqlite does not exist or cannot be found.")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
        output_file.close()
