from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemAuthDB(Plugin):
    """
    Parse information from /private/var/db/auth.db
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Auth DB"
        self._description = "Parse information from /private/var/db/auth.db"
        self._data_file = "auth.db"
        self._output_file = "System_Auth.txt"
        self._type = "sqlite"

    def parse(self):
        """
        Read the /private/var/db/auth.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            query = "SELECT name, rules.'group', type, class, tries, version, kofn, created, modified, " \
                    "identifier, comment FROM rules ORDER BY name"
            file = os.path.join(self._input_dir, "private", "var", "db", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan",
                                    "yosemite", "mavericks"]:
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
                                created = riplib.osxripper_time.get_cocoa_seconds(row["created"])
                                modified = riplib.osxripper_time.get_cocoa_seconds(row["modified"])
                                of.write("Name      : {0}\r\n".format(row["name"]))
                                of.write("Group     : {0}\r\n".format(row["group"]))
                                of.write("Type      : {0}\r\n".format(row["type"]))
                                of.write("Class     : {0}\r\n".format(row["class"]))
                                of.write("Tries     : {0}\r\n".format(row["tries"]))
                                of.write("Version   : {0}\r\n".format(row["version"]))
                                of.write("K-OF-N    : {0}\r\n".format(row["kofn"]))
                                of.write("Created   : {0}\r\n".format(created))
                                of.write("Modified  : {0}\r\n".format(modified))
                                of.write("Identifier: {0}\r\n".format(row["identifier"]))
                                of.write("Comment   : {0}\r\n".format(row["comment"]))
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
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version in ["mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
