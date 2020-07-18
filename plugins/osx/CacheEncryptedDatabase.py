""" Module to parse cache_encryptedA.db """
import codecs
import logging
import os
import sqlite3
import riplib.osxripper_time
from riplib.plugin import Plugin


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
        self.set_name("Wifi Locations - cache_encryptedA.db")
        self.set_description("Parse information from /private/var/folders/.../cache_encryptedA.db")
        self.set_data_file("cache_encryptedA.db")
        self.set_output_file("Wifi_Cache_Encrypted.txt")
        self.set_type("sqlite")

    def parse(self):
        """
        Read the /private/var/folders/.../cache_encryptedA.db
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            start_folder = os.path.join(self._input_dir, "private", "var", "folders")
            file_list = []
            for root, _, files in os.walk(start_folder):
                if self._data_file in files:
                    file_list.append(os.path.join(root, self._data_file))

            if len(file_list) == 0:
                logging.warning("File: %s does not exist or cannot be found.\r\n", self._data_file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(self._data_file))
                return

            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks"]:
                for database_file in file_list:
                    if os.path.isfile(database_file):
                        output_file.write("Source Database: {0}\r\n\r\n".format(database_file))
                        parse_os = Parse01(output_file, database_file)
                        parse_os.parse()

            elif self._os_version == "mountain_lion":
                for database_file in file_list:
                    if os.path.isfile(database_file):
                        output_file.write("Source Database: {0}\r\n\r\n".format(database_file))
                        parse_os = Parse02(output_file, database_file)
                        parse_os.parse()

            elif self._os_version in ["lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                output_file.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
        output_file.close()

class Parse01():
    """
    Convenience class for parsing macOS data
    """
    def __init__(self, output_file, data_file):
        self._output_file = output_file
        self._data_file = data_file

    def parse(self):
        """
        Parse data
        """
        query = "SELECT mac,channel,timestamp,latitude," \
                "longitude,horizontalaccuracy,altitude,verticalaccuracy,speed,course," \
                "confidence,score,reach FROM wifilocation ORDER BY timestamp, mac"

        conn = None
        try:
            conn = sqlite3.connect(self._data_file)
            conn.row_factory = sqlite3.Row
            with conn:
                cur = conn.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        timestamp = riplib.osxripper_time.get_cocoa_seconds(row["timestamp"])
                        self._output_file.write("MAC Address        : {0}\r\n".format(row["mac"]))
                        self._output_file.write("Channel            : {0}\r\n".format(row["channel"]))
                        self._output_file.write("Timestamp          : {0}\r\n".format(timestamp))
                        self._output_file.write("Latitude           : {0}\r\n".format(row["latitude"]))
                        self._output_file.write("Longitude          : {0}\r\n".format(row["longitude"]))
                        self._output_file.write("Horizontal Accuracy: {0}\r\n".format(row["horizontalaccuracy"]))
                        self._output_file.write("Altitude           : {0}\r\n".format(row["altitude"]))
                        self._output_file.write("Vertical Accuracy  : {0}\r\n".format(row["verticalaccuracy"]))
                        self._output_file.write("Speed              : {0}\r\n".format(row["speed"]))
                        self._output_file.write("Course             : {0}\r\n".format(row["course"]))
                        self._output_file.write("Confidence         : {0}\r\n".format(row["confidence"]))
                        self._output_file.write("Score              : {0}\r\n".format(row["score"]))
                        self._output_file.write("Reach              : {0}\r\n".format(row["reach"]))
                        self._output_file.write("\r\n")
                else:
                    self._output_file.write("No data in database.\r\n")
            self._output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))
        finally:
            if conn:
                conn.close()
        self._output_file.write("="*50 + "\r\n")

class Parse02():
    """
    Convenience class for parsing macOS data
    """
    def __init__(self, output_file, data_file):
        self._output_file = output_file
        self._data_file = data_file

    def parse(self):
        """
        Parse data
        """
        query = "SELECT mac,channel,datetime(timestamp + 978307200, 'unixepoch'),latitude," \
                "longitude,horizontalaccuracy,altitude,verticalaccuracy,speed,course," \
                "confidence,score FROM wifilocation ORDER BY timestamp, mac"
        conn = None
        try:
            conn = sqlite3.connect(self._data_file)
            conn.row_factory = sqlite3.Row
            with conn:
                cur = conn.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        timestamp = riplib.osxripper_time.get_cocoa_seconds(row["timestamp"])
                        self._output_file.write("MAC Address        : {0}\r\n".format(row["mac"]))
                        self._output_file.write("Channel            : {0}\r\n".format(row["channel"]))
                        self._output_file.write("Timestamp          : {0}\r\n".format(timestamp))
                        self._output_file.write("Latitude           : {0}\r\n".format(row["latitude"]))
                        self._output_file.write("Longitude          : {0}\r\n".format(row["longitude"]))
                        self._output_file.write("Horizontal Accuracy: {0}\r\n".format(row["horizontalaccuracy"]))
                        self._output_file.write("Altitude           : {0}\r\n".format(row["altitude"]))
                        self._output_file.write("Vertical Accuracy  : {0}\r\n".format(row["verticalaccuracy"]))
                        self._output_file.write("Speed              : {0}\r\n".format(row["speed"]))
                        self._output_file.write("Course             : {0}\r\n".format(row["course"]))
                        self._output_file.write("Confidence         : {0}\r\n".format(row["confidence"]))
                        self._output_file.write("Score              : {0}\r\n".format(row["score"]))
                        self._output_file.write("\r\n")
                else:
                    self._output_file.write("No data in database.\r\n")
            self._output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))
        finally:
            if conn:
                conn.close()
        self._output_file.write("="*50 + "\r\n")
