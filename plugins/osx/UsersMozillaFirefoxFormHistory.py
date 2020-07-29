""" Module to parse Firefox form history database """
import codecs
import logging
import os
import sqlite3
import riplib.osxripper_time
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersMozillaFirefoxFormHistory(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Firefox/Profiles/*.default/formhistory.sqlite
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Mozilla Firefox Form History")
        self.set_description("Parse information from /Users/<username>/Library/Application Support/Firefox/Profiles/*.default/formhistory.sqlite")
        self.set_data_file("formhistory.sqlite")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("sqlite")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
        else:
            logging.warning("%s does not exist.", users_path)
            print("[WARNING] {0} does not exist.".format(users_path))
            return
        for username in user_list:
            profile_search_path = "None"
            if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                profile_search_path = os.path.join(users_path, username, "Library", "Application Support", "Firefox", "Profiles")
            if os.path.isdir(profile_search_path):
                profiles_list = os.listdir(profile_search_path)
                for profile in profiles_list:
                    if profile.endswith(".default"):
                        sqlite_db = os.path.join(profile_search_path, profile, self._data_file)
                        if os.path.isfile(sqlite_db):
                            self.__parse_sqlite_db(sqlite_db, username)
                        else:
                            logging.warning("%s does not exist.", sqlite_db)
                            print("[WARNING] {0} does not exist.".format(sqlite_db))

    def __parse_sqlite_db(self, file, username):
        """
        Read the formhistory.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Firefox_Form_History.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if os.path.isfile(file):
                output_file.write("Source File: {0}\r\n\r\n".format(file))
                conn = None
                try:
                    query = "SELECT fieldname,value,timesUsed," \
                            "firstUsed," \
                            "lastUsed " \
                            "FROM moz_formhistory ORDER BY firstUsed"

                    conn = sqlite3.connect(file)
                    conn.row_factory = sqlite3.Row
                    with conn:
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        for row in rows:
                            first_used = riplib.osxripper_time.get_unix_micros(row["firstUsed"])
                            last_used = riplib.osxripper_time.get_unix_micros(row["lastUsed"])
                            output_file.write("Field Name: {0}\r\n".format(row["fieldname"]))
                            output_file.write("Value     : {0}\r\n".format(row["value"]))
                            output_file.write("Times Used: {0}\r\n".format(row["timesUsed"]))
                            output_file.write("First Used: {0}\r\n".format(first_used))
                            output_file.write("Last Used : {0}\r\n".format(last_used))
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
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
