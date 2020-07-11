from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

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
        self._name = "Quicklook Thumbnail Cache"
        self._description = "Parse information from " \
                            "/private/var/folders/.../com.apple.QuickLook.thumbnailcache/index.sqlite"
        self._data_file = "index.sqlite"
        self._output_file = "Quicklook_Thumbnail_Cache.txt"
        self._type = "sqlite"

    def parse(self):
        """
        Read the /private/var/folders/.../com.apple.QuickLook.thumbnailcache/index.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")

            start_folder = os.path.join(self._input_dir, "private", "var", "folders")
            file_list = []
            # if self._os_version in ["big_sur", "catalina"]:
            if self._os_version in ["catalina"]:
                # Change to database schema with embedded bplists (NSKeyedArchiver)
                logging.warning("Database in Catalina has changed to use embedded bplists (NSKeyedArchiver)\r\n")
                of.write("[WARNING] Database in Catalina has changed to use embedded bplists (NSKeyedArchiver)\r\n")
                print("[WARNING] Database in Catalina has changed to use embedded bplists (NSKeyedArchiver)")
                return
            elif self._os_version in ["mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks",
                                    "mountain_lion", "lion", "snow_leopard"]:
                query = "SELECT f.folder,f.file_name,tb.hit_count,tb.last_hit_date FROM files f,thumbnails tb" \
                        " WHERE f.rowid = tb.file_id ORDER BY f.folder, tb.last_hit_date"
                # search for index.sqlite
                for root, subdirs, files in os.walk(start_folder):
                    if "com.apple.QuickLook.thumbnailcache" in root:
                        if self._data_file in files:
                            file_list.append(os.path.join(root, self._data_file))
                if len(file_list) > 0:
                    for database_file in file_list:
                        if os.path.isfile(database_file):
                            of.write("Source Database: {0}\r\n\r\n".format(database_file))
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
                                            last_hit_date = \
                                                riplib.osxripper_time.get_cocoa_seconds(row["last_hit_date"])
                                            of.write("Folder        : {0}\r\n".format(row["folder"]))
                                            of.write("File Name     : {0}\r\n".format(row["file_name"]))
                                            of.write("Hit Count     : {0}\r\n".format(row["hit_count"]))
                                            of.write("Last Hit Date : {0}\r\n".format(last_hit_date))
                                            of.write("\r\n")
                                    else:
                                        of.write("No data in database.\r\n")
                                of.write("\r\n")
                            except sqlite3.Error as e:
                                logging.error("{0}".format(e.args[0]))
                                print("[ERROR] {0}".format(e.args[0]))
                            finally:
                                if conn:
                                    conn.close()
                        of.write("="*50 + "\r\n")
                else:
                    logging.warning("File: index.sqlite does not exist or cannot be found.\r\n")
                    of.write("[WARNING] File: index.sqlite does not exist or cannot be found.\r\n")
                    print("[WARNING] File: index.sqlite does not exist or cannot be found.")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
        of.close()
