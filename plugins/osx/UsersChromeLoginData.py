from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

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
        self._name = "User Chrome Browser Login Data"
        self._description = "Parse information from " \
                            "/Users/<username>/Library/Application Support/Google/Chrome/Default/Login Data"
        self._data_file = "Login Data"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "sqlite"
    
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
                        logging.warning("{0} does not exist.".format(history_path))
                        print("[WARNING] {0} does not exist.".format(history_path))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))
    
    def __parse_sqlite_db(self, file, username):
        """
        Read the Login Data SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_Login_Data.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
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
                of.write("Source File: {0}\r\n\r\n".format(history_db))
                of.write("N.B. Creds are stored as BLOBS, not retrieved by this plugin\r\n\r\n")
                conn = None
                try:
                    conn = sqlite3.connect(history_db)
                    conn.row_factory = sqlite3.Row
                    with conn:    
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        if len(rows) == 0:
                            of.write("No data found in this database.\r\n\r\n")
                        else:
                            for row in rows:
                                date_created = riplib.osxripper_time.get_gregorian_micros(row["date_created"])
                                date_synced = riplib.osxripper_time.get_gregorian_micros(row["date_synced"])
                                of.write("Username           : {0}\r\n".format(row["username_value"]))
                                of.write("Display Name       : {0}\r\n".format(row["display_name"]))
                                of.write("Origin URL         : {0}\r\n".format(row["origin_url"]))
                                of.write("Action URL         : {0}\r\n".format(row["action_url"]))
                                of.write("Date Created       : {0}\r\n".format(date_created))
                                of.write("Date Synced        : {0}\r\n".format(date_synced))
                                of.write("Signon Realm       : {0}\r\n".format(row["signon_realm"]))
                                of.write("SSL Valid          : {0}\r\n".format(row["ssl_valid"]))
                                of.write("Preferred          : {0}\r\n".format(row["preferred"]))
                                of.write("Times Used         : {0}\r\n".format(row["times_used"]))
                                of.write("Blacklisted by User: {0}\r\n".format(row["blacklisted_by_user"]))
                                of.write("Scheme             : {0}\r\n".format(row["scheme"]))
                                of.write("Password Type      : {0}\r\n".format(row["password_type"]))
                                # of.write("Avatar URL         : {0}\r\n".format(row["avatar_url"]))
                                of.write("Federation URL     : {0}\r\n".format(row["federation_url"]))
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
            of.write("="*40 + "\r\n\r\n")
        of.close()
