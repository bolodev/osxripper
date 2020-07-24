""" Module to parse information from Google Chrome login data """
import codecs
import logging
import os
import sqlite3
import riplib.osxripper_time
from riplib.plugin import Plugin

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersChromeLoginData(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Login Data
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Chrome Browser Login Data")
        self.set_description("Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Login Data")
        self.set_data_file("Login Data")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("sqlite")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        # username = None
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    history_path = os.path\
                        .join(users_path, username, "Library", "Application Support", "Google", "Chrome", "Default")
                    if os.path.isdir(history_path):
                        self.__parse_sqlite_db(history_path, username)
                    else:
                        logging.warning("%s does not exist.", history_path)
                        print("[WARNING] {0} does not exist.".format(history_path))
        else:
            logging.warning("%s does not exist.", users_path)
            print("[WARNING] {0} does not exist.".format(users_path))

    def __parse_sqlite_db(self, file, username):
        """
        Read the Login Data SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_Login_Data.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, self._data_file)
            # query = "SELECT username_value,display_name,origin_url,action_url," \
            #         "date_created,date_synced," \
            #         "signon_realm,ssl_valid,preferred,times_used,blacklisted_by_user," \
            #         "scheme,password_type,avatar_url,federation_url FROM logins ORDER BY username_value"
            query = "SELECT username_value,display_name,origin_url,action_url," \
                    "date_created,date_synced," \
                    "signon_realm,preferred,times_used,blacklisted_by_user," \
                    "scheme,password_type,federation_url FROM logins ORDER BY username_value"
            if os.path.isfile(history_db):
                output_file.write("Source File: {0}\r\n\r\n".format(history_db))
                output_file.write("N.B. Creds are stored as BLOBS, not retrieved by this plugin\r\n\r\n")
                conn = None
                try:
                    conn = sqlite3.connect(history_db)
                    conn.row_factory = sqlite3.Row
                    with conn:
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        if len(rows) == 0:
                            output_file.write("No data found in this database.\r\n\r\n")
                        else:
                            for row in rows:
                                date_created = riplib.osxripper_time.get_gregorian_micros(row["date_created"])
                                date_synced = riplib.osxripper_time.get_gregorian_micros(row["date_synced"])
                                output_file.write("Username           : {0}\r\n".format(row["username_value"]))
                                output_file.write("Display Name       : {0}\r\n".format(row["display_name"]))
                                output_file.write("Origin URL         : {0}\r\n".format(row["origin_url"]))
                                output_file.write("Action URL         : {0}\r\n".format(row["action_url"]))
                                output_file.write("Date Created       : {0}\r\n".format(date_created))
                                output_file.write("Date Synced        : {0}\r\n".format(date_synced))
                                output_file.write("Signon Realm       : {0}\r\n".format(row["signon_realm"]))
                                output_file.write("SSL Valid          : {0}\r\n".format(row["ssl_valid"]))
                                output_file.write("Preferred          : {0}\r\n".format(row["preferred"]))
                                output_file.write("Times Used         : {0}\r\n".format(row["times_used"]))
                                output_file.write("Blacklisted by User: {0}\r\n".format(row["blacklisted_by_user"]))
                                output_file.write("Scheme             : {0}\r\n".format(row["scheme"]))
                                output_file.write("Password Type      : {0}\r\n".format(row["password_type"]))
                                # output_file.write("Avatar URL         : {0}\r\n".format(row["avatar_url"]))
                                output_file.write("Federation URL     : {0}\r\n".format(row["federation_url"]))
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
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
