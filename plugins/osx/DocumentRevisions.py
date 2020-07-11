from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class DocumentRevisions(Plugin):
    """
    Parse information from /.DocumentRevisions-V100/db-V1/db.sqlite
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Document Revisions"
        self._description = "Parse information from /.DocumentRevisions-V100/db-V1/db.sqlite"
        self._data_file = "db.sqlite"
        self._output_file = "DocumentRevisions.txt"  # this will have to be defined per user account
        self._type = "sqlite"
    
    def parse(self):
        """
        Read the db.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, ".DocumentRevisions-V100", "db-V1", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina"]:
            if self._os_version == "catalina":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            elif self._os_version in ["mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks",
                                      "mountain_lion", "lion"]:
                query = "SELECT file_row_id,file_name,file_parent_id,file_path,file_inode,file_last_seen," \
                        "file_status, file_storage_id FROM files"
                if os.path.isfile(file):
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        conn.row_factory = sqlite3.Row
                        with conn:    
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                file_last_seen = riplib.osxripper_time.get_unix_seconds(row["file_last_seen"])
                                of.write("Row ID         : {0}\r\n".format(row["file_row_id"]))
                                of.write("File Name      : {0}\r\n".format(row["file_name"]))
                                of.write("Parent ID      : {0}\r\n".format(row["file_parent_id"]))
                                of.write("File Path      : {0}\r\n".format(row["file_path"]))
                                of.write("File Inode     : {0}\r\n".format(row["file_inode"]))
                                of.write("File Last Seen : {0}\r\n".format(file_last_seen))
                                of.write("File Status     : {0}\r\n".format(row["file_status"]))
                                of.write("File Storage ID : {0}\r\n".format(row["file_storage_id"]))
                                of.write("\r\n")
                    except sqlite3.Error as e:
                        logging.error("{0}".format(e.args[0]))
                        print("[ERROR] {0}".format(e.args[0]))
                    finally:
                        if conn:
                            conn.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
