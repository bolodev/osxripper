from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersChromeCookies(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Cookies
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Chrome Browser Cookies"
        self._description = "Parse information from " \
                            "/Users/<username>/Library/Application Support/Google/Chrome/Default/Cookies"
        self._data_file = "Cookies"
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
        Read the History SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_Cookies.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, self._data_file)
            query = "SELECT host_key,name,value,path,creation_utc,last_access_utc,expires_utc," \
                    "secure,httponly,has_expires,persistent,priority " \
                    "FROM cookies ORDER BY creation_utc;"

            query_alt = "SELECT host_key,name,value,path,creation_utc,last_access_utc,expires_utc,is_secure," \
                        "is_httponly,has_expires,is_persistent,priority FROM cookies ORDER BY creation_utc;"

            if os.path.isfile(history_db):
                of.write("Source File: {0}\r\n\r\n".format(history_db))
                conn = None
                try:
                    conn = sqlite3.connect(history_db)
                    conn.row_factory = sqlite3.Row
                    with conn:    
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        for row in rows:
                            creation_utc = riplib.osxripper_time.get_gregorian_micros(row["creation_utc"])
                            last_access_utc = riplib.osxripper_time.get_gregorian_micros(row["last_access_utc"])
                            expires_utc = riplib.osxripper_time.get_gregorian_micros(row["expires_utc"])

                            of.write("Host Key       : {0}\r\n".format(row["host_key"]))
                            of.write("Name           : {0}\r\n".format(row["name"]))
                            of.write("Value          : {0}\r\n".format(row["value"]))
                            of.write("Path           : {0}\r\n".format(row["path"]))
                            of.write("Creation UTC   : {0}\r\n".format(creation_utc))
                            of.write("Last Access UTC: {0}\r\n".format(last_access_utc))
                            of.write("Expires UTC    : {0}\r\n".format(expires_utc))
                            of.write("Secure         : {0}\r\n".format(row["secure"]))
                            of.write("HTTP Only      : {0}\r\n".format(row["httponly"]))
                            of.write("Has Expires    : {0}\r\n".format(row["has_expires"]))
                            of.write("Persistent     : {0}\r\n".format(row["persistent"]))
                            of.write("Priority       : {0}\r\n".format(row["priority"]))
                            of.write("\r\n")
                except sqlite3.Error as e:
                    try:
                        cur = conn.cursor()
                        cur.execute(query_alt)
                        rows = cur.fetchall()
                        for row in rows:
                            creation_utc = riplib.osxripper_time.get_gregorian_micros(row["creation_utc"])
                            last_access_utc = riplib.osxripper_time.get_gregorian_micros(row["last_access_utc"])
                            expires_utc = riplib.osxripper_time.get_gregorian_micros(row["expires_utc"])

                            of.write("Host Key       : {0}\r\n".format(row["host_key"]))
                            of.write("Name           : {0}\r\n".format(row["name"]))
                            of.write("Value          : {0}\r\n".format(row["value"]))
                            of.write("Path           : {0}\r\n".format(row["path"]))
                            of.write("Creation UTC   : {0}\r\n".format(creation_utc))
                            of.write("Last Access UTC: {0}\r\n".format(last_access_utc))
                            of.write("Expires UTC    : {0}\r\n".format(expires_utc))
                            of.write("Secure         : {0}\r\n".format(row["is_secure"]))
                            of.write("HTTP Only      : {0}\r\n".format(row["is_httponly"]))
                            of.write("Has Expires    : {0}\r\n".format(row["has_expires"]))
                            of.write("Persistent     : {0}\r\n".format(row["is_persistent"]))
                            of.write("Priority       : {0}\r\n".format(row["priority"]))
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
            of.write("="*40 + "\r\n\r\n")
        of.close()
