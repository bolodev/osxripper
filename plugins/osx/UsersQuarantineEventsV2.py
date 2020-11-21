""" Module to parse QuarantineEventsV2 database """
import codecs
# import datetime
import logging
import os
import sqlite3
import riplib.osxripper_time
from riplib.plugin import Plugin

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
        self.set_name("User LaunchServices.QuarantineEventsV2")
        self.set_description("Parse information from /Users/<username>/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2")
        self.set_data_file("com.apple.LaunchServices.QuarantineEventsV2")
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
                        logging.warning("%s does not exist.", sqlite_db)
                        print("[WARNING] {0} does not exist.".format(sqlite_db))
        else:
            logging.warning("%s does not exist.", users_path)
            print("[WARNING] {0} does not exist.".format(users_path))

    def __parse_sqlite_db(self, file, username):
        """
        Read the com.apple.LaunchServices.QuarantineEventsV2 SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Quarantine_Events.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            #                         "mavericks", "mountain_lion", "lion"]:
                query = "SELECT LSQuarantineEventIdentifier,LSQuarantineTimeStamp,LSQuarantineAgentBundleIdentifier," \
                        "LSQuarantineAgentName,LSQuarantineDataURLString,LSQuarantineSenderName," \
                        "LSQuarantineSenderAddress,LSQuarantineTypeNumber,LSQuarantineOriginTitle," \
                        "LSQuarantineOriginURLString,LSQuarantineOriginAlias FROM LSQuarantineEvent"
                if os.path.isfile(file):
                    output_file.write("Source File: {0}\r\n\r\n".format(file))
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
                                output_file.write("Event Identifier      : {0}\r\n".format(row["LSQuarantineEventIdentifier"]))
                                output_file.write("Timestamp             : {0}\r\n".format(timestamp))
                                output_file.write("AgentBundle Identifier: {0}\r\n".format(row["LSQuarantineAgentBundleIdentifier"]))
                                output_file.write("Agent Name            : {0}\r\n".format(row["LSQuarantineAgentName"]))
                                output_file.write("Data URL String       : {0}\r\n".format(row["LSQuarantineDataURLString"]))
                                output_file.write("Sender Name           : {0}\r\n".format(row["LSQuarantineSenderName"]))
                                output_file.write("Sender Address        : {0}\r\n".format(row["LSQuarantineSenderAddress"]))
                                output_file.write("Type Number           : {0}\r\n".format(row["LSQuarantineTypeNumber"]))
                                output_file.write("Origin Title          : {0}\r\n".format(row["LSQuarantineOriginTitle"]))
                                output_file.write("Origin URL String     : {0}\r\n".format(row["LSQuarantineOriginURLString"]))
                                output_file.write("Origin Alias          : {0}\r\n".format(row["LSQuarantineOriginAlias"]))
                                output_file.write("\r\n")

                    except sqlite3.Error as error:
                        logging.error("%s", error.args[0])
                        print("[ERROR] {0}".format(error.args[0]))
                    finally:
                        if conn:
                            conn.close()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            elif self._os_version == "snow_leopard":
                query = "SELECT LSQuarantineEventIdentifier,LSQuarantineTimeStamp,LSQuarantineAgentBundleIdentifier," \
                        "LSQuarantineAgentName,LSQuarantineDataURLString,LSQuarantineSenderName," \
                        "LSQuarantineSenderAddress,LSQuarantineTypeNumber,LSQuarantineOriginTitle," \
                        "LSQuarantineOriginURLString,LSQuarantineOriginAlias FROM LSQuarantineEvent"
                if os.path.isfile(file):
                    output_file.write("Source File: {0}\r\n\r\n".format(file))
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
                                output_file.write("Event Identifier      : {0}\r\n".format(row["LSQuarantineEventIdentifier"]))
                                output_file.write("Timestamp             : {0}\r\n".format(timestamp))
                                output_file.write("AgentBundle Identifier: {0}\r\n".format(row["LSQuarantineAgentBundleIdentifier"]))
                                output_file.write("Agent Name            : {0}\r\n".format(row["LSQuarantineAgentName"]))
                                output_file.write("Data URL String       : {0}\r\n".format(row["LSQuarantineDataURLString"]))
                                output_file.write("Sender Name           : {0}\r\n".format(row["LSQuarantineSenderName"]))
                                output_file.write("Sender Address        : {0}\r\n".format(row["LSQuarantineSenderAddress"]))
                                output_file.write("Type Number           : {0}\r\n".format(row["LSQuarantineTypeNumber"]))
                                output_file.write("Origin Title          : {0}\r\n".format(row["LSQuarantineOriginTitle"]))
                                output_file.write("Origin URL String     : {0}\r\n".format(row["LSQuarantineOriginURLString"]))
                                output_file.write("Origin Alias          : {0}\r\n".format(row["LSQuarantineOriginAlias"]))
                                output_file.write("\r\n")

                    except sqlite3.Error as error:
                        logging.error("%s", error.args[0])
                        print("[ERROR] {0}".format(error.args[0]))
                    finally:
                        if conn:
                            conn.close()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
