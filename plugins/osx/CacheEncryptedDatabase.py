from riplib.plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class CacheEncryptedDatabase(Plugin):
    """
    Parse information from /private/var/folders/.../cache_encryptedA.db
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Wifi Locations - cache_encryptedA.db"
        self._description = "Parse information from /private/var/folders/.../cache_encryptedA.db"
        self._data_file = "cache_encryptedA.db"
        self._output_file = "Wifi_Cache_Encrypted.txt"
        self._type = "sqlite"

    def parse(self):
        """
        Read the /private/var/folders/.../cache_encryptedA.db
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")

            start_folder = os.path.join(self._input_dir, "private", "var", "folders")
            file_list = []
            for root, subdirs, files in os.walk(start_folder):
                if self._data_file in files:
                    file_list.append(os.path.join(root, self._data_file))

            if len(file_list) == 0:
                logging.warning("File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
                of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(self._data_file))
                return
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks"]:
                query = "SELECT mac,channel,timestamp,latitude," \
                        "longitude,horizontalaccuracy,altitude,verticalaccuracy,speed,course," \
                        "confidence,score,reach FROM wifilocation ORDER BY timestamp, mac"
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
                                        timestamp = riplib.osxripper_time.get_cocoa_seconds(row["timestamp"])
                                        of.write("MAC Address        : {0}\r\n".format(row["mac"]))
                                        of.write("Channel            : {0}\r\n".format(row["channel"]))
                                        of.write("Timestamp          : {0}\r\n".format(timestamp))
                                        of.write("Latitude           : {0}\r\n".format(row["latitude"]))
                                        of.write("Longitude          : {0}\r\n".format(row["longitude"]))
                                        of.write("Horizontal Accuracy: {0}\r\n".format(row["horizontalaccuracy"]))
                                        of.write("Altitude           : {0}\r\n".format(row["altitude"]))
                                        of.write("Vertical Accuracy  : {0}\r\n".format(row["verticalaccuracy"]))
                                        of.write("Speed              : {0}\r\n".format(row["speed"]))
                                        of.write("Course             : {0}\r\n".format(row["course"]))
                                        of.write("Confidence         : {0}\r\n".format(row["confidence"]))
                                        of.write("Score              : {0}\r\n".format(row["score"]))
                                        of.write("Reach              : {0}\r\n".format(row["reach"]))
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

            elif self._os_version == "mountain_lion":
                query = "SELECT mac,channel,datetime(timestamp + 978307200, 'unixepoch'),latitude," \
                        "longitude,horizontalaccuracy,altitude,verticalaccuracy,speed,course," \
                        "confidence,score FROM wifilocation ORDER BY timestamp, mac"

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
                                        timestamp = riplib.osxripper_time.get_cocoa_seconds(row["timestamp"])
                                        of.write("MAC Address        : {0}\r\n".format(row["mac"]))
                                        of.write("Channel            : {0}\r\n".format(row["channel"]))
                                        of.write("Timestamp          : {0}\r\n".format(timestamp))
                                        of.write("Latitude           : {0}\r\n".format(row["latitude"]))
                                        of.write("Longitude          : {0}\r\n".format(row["longitude"]))
                                        of.write("Horizontal Accuracy: {0}\r\n".format(row["horizontalaccuracy"]))
                                        of.write("Altitude           : {0}\r\n".format(row["altitude"]))
                                        of.write("Vertical Accuracy  : {0}\r\n".format(row["verticalaccuracy"]))
                                        of.write("Speed              : {0}\r\n".format(row["speed"]))
                                        of.write("Course             : {0}\r\n".format(row["course"]))
                                        of.write("Confidence         : {0}\r\n".format(row["confidence"]))
                                        of.write("Score              : {0}\r\n".format(row["score"]))
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

            elif self._os_version in ["lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
        of.close()
