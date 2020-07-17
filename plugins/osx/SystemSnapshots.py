from riplib.plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemSnapshots(Plugin):
    """
    Parse information from /private/var/db/systemstats/snapshots.db
    N.B. database not in macOS Sierra, replaced by .stats files
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Snapshots"
        self._description = "Parse information from /private/var/db/systemstats/snapshots.db"
        self._data_file = "snapshots.db"
        self._output_file = "System_Snapshots.txt"
        self._type = "sqlite"
    
    def parse(self):
        """
        Read the /private/var/db/systemstats/snapshots.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            query = "SELECT time, pid, uniqueid, comm FROM snapshots ORDER BY time"
            file = os.path.join(self._input_dir, "private", "var", "db", "systemstats", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["el_capitan", "yosemite", "mavericks"]:
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
                                snap_time = riplib.osxripper_time.get_unix_micros(row["time"])
                                of.write("Comm     : {0}\r\n".format(row["comm"]))
                                of.write("Time     : {0}\r\n".format(snap_time))
                                of.write("PID      : {0}\r\n".format(row["pid"]))
                                of.write("Unique ID: {0}\r\n".format(row["uniqueid"]))
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

            # elif self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra",
            elif self._os_version in ["catalina", "mojave", "high_sierra", "sierra",
                                      "mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
