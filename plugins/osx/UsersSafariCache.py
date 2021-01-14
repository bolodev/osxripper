""" Module to parse Safari cache database """
import codecs
import logging
import os
import sqlite3
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersSafariCache(Plugin):
    """
    Parse information from /Users/<username>/Library/Caches/com.apple.safari/Cache.db
    For Mojave and later /Users/<username>/Library/Containers/com.apple.Safari/Data/Library/Caches/com.apple.Safari/
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Safari Cache")
        self.set_description("Parse information from /Users/<username>/Library/Caches/com.apple.safari/Cache.db " \
                             "or /Users/<username>/Library/Containers/com.apple.Safari/Data/Library/Caches/com.apple.Safari/Cache.db")
        self.set_data_file("Cache.db")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("sqlite")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                sqlite_db = None
                if self._os_version in ["mojave", "catalina"]:
                    if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                        sqlite_db = os.path.join(users_path, username, "Library", "Containers", "com.apple.Safari", "Data", "Library", "Caches", "com.apple.safari", self._data_file)
                    else:
                        if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                            sqlite_db = os.path.join(users_path, username, "Library", "Caches", "com.apple.safari", self._data_file)
                    if os.path.isfile(sqlite_db):
                        self.__parse_sqlite_db(sqlite_db, username)
                    else:
                        logging.warning("%s does not exist.", sqlite_db)
                        print("[WARNING] {0} does not exist.".format(sqlite_db))
        else:
            logging.warning("%s does not exist.", users_path)
            print("[WARNING] {0} does not exist.".format(users_path))

    def __parse_sqlite_db(self, file, username):
        """
        Read the WebpageIcons.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Cache.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("=" * 10 + " " + self._name + " " + "=" * 10 + "\r\n")
            # if self._os_version in ["big_sur", "mojave", "catalina"]:
            if self._os_version in ["mojave", "catalina"]:
                # Does not exist in Mojave or Catalina
                pass
            if self._os_version in ["high_sierra", "sierra", "el_capitan", "yosemite", "mavericks", "mountain_lion"]:
                if os.path.isfile(file):
                    output_file.write("Source File: {0}\r\n\r\n".format(file))
                    parse_os = ParseVers1013108(output_file, file)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version in ["lion", "snow_leopard"]:
                if os.path.isfile(file):
                    output_file.write("Source File: {0}\r\n\r\n".format(file))
                    parse_os = ParseVers107106(output_file, file)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("=" * 40 + "\r\n\r\n")
        output_file.close()

class ParseVers1013108():
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
        conn = None
        query = "SELECT request_key, partition, time_stamp FROM cfurl_cache_response"
        try:
            conn = sqlite3.connect(self._data_file)
            conn.row_factory = sqlite3.Row
            with conn:
                cur = conn.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                for row in rows:
                    self._output_file.write("Request Key: {0}\r\n".format(row["request_key"]))
                    self._output_file.write("Partition  : {0}\r\n".format(row["partition"]))
                    self._output_file.write("Timestamp  : {0}\r\n".format(row["time_stamp"]))
                    self._output_file.write("\r\n")

        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))
        finally:
            if conn:
                conn.close()

class ParseVers107106():
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
        query = "SELECT request_key, time_stamp FROM cfurl_cache_response"
        conn = None
        try:
            conn = sqlite3.connect(self._data_file)
            conn.row_factory = sqlite3.Row
            with conn:
                cur = conn.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                for row in rows:
                    self._output_file.write("Request Key: {0}\r\n".format(row["request_key"]))
                    self._output_file.write("Timestamp  : {0}\r\n".format(row["time_stamp"]))
                    self._output_file.write("\r\n")

        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))
        finally:
            if conn:
                conn.close()
