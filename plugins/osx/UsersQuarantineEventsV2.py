from riplib.Plugin import Plugin
import codecs
import datetime
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersQuarantineEventsV2(Plugin):
    """
    Parse information from /Users/<username>/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User LaunchServices.QuarantineEventsV2"
        self._description = "Parse information from " \
                            "/Users/<username>/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2"
        self._data_file = "com.apple.LaunchServices.QuarantineEventsV2"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "sqlite"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    if self._os_version != "snow_leopard":
                        sqlite_db = os.path.join(users_path, username, "Library", "Preferences", self._data_file)
                    else:
                        sqlite_db = os.path\
                            .join(users_path, username, "Library", "Preferences",
                                  "com.apple.LaunchServices.QuarantineEvents")
                    if os.path.isfile(sqlite_db):
                        self.__parse_sqlite_db(sqlite_db, username)
                    else:
                        logging.warning("{0} does not exist.".format(sqlite_db))
                        print("[WARNING] {0} does not exist.".format(sqlite_db))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))
    
    def __parse_sqlite_db(self, file, username):
        """
        Read the com.apple.LaunchServices.QuarantineEventsV2 SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Quarantine_Events.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion"]:
                query = "SELECT LSQuarantineEventIdentifier,LSQuarantineTimeStamp,LSQuarantineAgentBundleIdentifier," \
                        "LSQuarantineAgentName,LSQuarantineDataURLString,LSQuarantineSenderName," \
                        "LSQuarantineSenderAddress,LSQuarantineTypeNumber,LSQuarantineOriginTitle," \
                        "LSQuarantineOriginURLString,LSQuarantineOriginAlias FROM LSQuarantineEvent"
                if os.path.isfile(file):
                    of.write("Source File: {0}\r\n\r\n".format(file))
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        conn.row_factory = sqlite3.Row
                        with conn:    
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                timestamp = riplib.osxripper_time.get_cocoa_seconds(row["LSQuarantineTimeStamp"])
                                of.write("Event Identifier      : {0}\r\n".format(row["LSQuarantineEventIdentifier"]))
                                of.write("Timestamp             : {0}\r\n".format(timestamp))
                                of.write("AgentBundle Identifier: {0}\r\n"
                                         .format(row["LSQuarantineAgentBundleIdentifier"]))
                                of.write("Agent Name            : {0}\r\n".format(row["LSQuarantineAgentName"]))
                                of.write("Data URL String       : {0}\r\n".format(row["LSQuarantineDataURLString"]))
                                of.write("Sender Name           : {0}\r\n".format(row["LSQuarantineSenderName"]))
                                of.write("Sender Address        : {0}\r\n".format(row["LSQuarantineSenderAddress"]))
                                of.write("Type Number           : {0}\r\n".format(row["LSQuarantineTypeNumber"]))
                                of.write("Origin Title          : {0}\r\n".format(row["LSQuarantineOriginTitle"]))
                                of.write("Origin URL String     : {0}\r\n".format(row["LSQuarantineOriginURLString"]))
                                of.write("Origin Alias          : {0}\r\n".format(row["LSQuarantineOriginAlias"]))
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
                query = "SELECT LSQuarantineEventIdentifier,LSQuarantineTimeStamp,LSQuarantineAgentBundleIdentifier," \
                        "LSQuarantineAgentName,LSQuarantineDataURLString,LSQuarantineSenderName," \
                        "LSQuarantineSenderAddress,LSQuarantineTypeNumber,LSQuarantineOriginTitle," \
                        "LSQuarantineOriginURLString,LSQuarantineOriginAlias FROM LSQuarantineEvent"
                if os.path.isfile(file):
                    of.write("Source File: {0}\r\n\r\n".format(file))
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        conn.row_factory = sqlite3.Row
                        with conn:
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                timestamp = riplib.osxripper_time.get_cocoa_seconds(row["LSQuarantineTimeStamp"])
                                of.write("Event Identifier      : {0}\r\n".format(row["LSQuarantineEventIdentifier"]))
                                of.write("Timestamp             : {0}\r\n".format(timestamp))
                                of.write("AgentBundle Identifier: {0}\r\n"
                                         .format(row["LSQuarantineAgentBundleIdentifier"]))
                                of.write("Agent Name            : {0}\r\n".format(row["LSQuarantineAgentName"]))
                                of.write("Data URL String       : {0}\r\n".format(row["LSQuarantineDataURLString"]))
                                of.write("Sender Name           : {0}\r\n".format(row["LSQuarantineSenderName"]))
                                of.write("Sender Address        : {0}\r\n".format(row["LSQuarantineSenderAddress"]))
                                of.write("Type Number           : {0}\r\n".format(row["LSQuarantineTypeNumber"]))
                                of.write("Origin Title          : {0}\r\n".format(row["LSQuarantineOriginTitle"]))
                                of.write("Origin URL String     : {0}\r\n".format(row["LSQuarantineOriginURLString"]))
                                of.write("Origin Alias          : {0}\r\n".format(row["LSQuarantineOriginAlias"]))
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
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
