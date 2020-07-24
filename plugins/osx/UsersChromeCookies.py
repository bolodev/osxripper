""" Module to parse Google Chrome Cookies database"""
import codecs
import logging
import os
import sqlite3
import riplib.osxripper_time
from riplib.plugin import Plugin


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
        self.set_name("User Chrome Browser Cookies")
        self.set_description("Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Cookies")
        self.set_data_file("Cookies")
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
                    history_path = os.path.join(users_path, username, "Library", "Application Support", "Google", "Chrome", "Default")
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
        Read the History SQLite database
        """
        query = "SELECT host_key,name,value,path,creation_utc,last_access_utc,expires_utc," \
                    "secure,httponly,has_expires,persistent,priority " \
                    "FROM cookies ORDER BY creation_utc;"

        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_Cookies.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, self._data_file)
            if os.path.isfile(history_db):
                output_file.write("Source File: {0}\r\n\r\n".format(history_db))
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

                            output_file.write("Host Key       : {0}\r\n".format(row["host_key"]))
                            output_file.write("Name           : {0}\r\n".format(row["name"]))
                            output_file.write("Value          : {0}\r\n".format(row["value"]))
                            output_file.write("Path           : {0}\r\n".format(row["path"]))
                            output_file.write("Creation UTC   : {0}\r\n".format(creation_utc))
                            output_file.write("Last Access UTC: {0}\r\n".format(last_access_utc))
                            output_file.write("Expires UTC    : {0}\r\n".format(expires_utc))
                            output_file.write("Secure         : {0}\r\n".format(row["secure"]))
                            output_file.write("HTTP Only      : {0}\r\n".format(row["httponly"]))
                            output_file.write("Has Expires    : {0}\r\n".format(row["has_expires"]))
                            output_file.write("Persistent     : {0}\r\n".format(row["persistent"]))
                            output_file.write("Priority       : {0}\r\n".format(row["priority"]))
                            output_file.write("\r\n")
                except sqlite3.Error as _:
                    self.__parse_alt(output_file, conn)
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()

    def __parse_alt(self, output_file, db_connection):
        """
        Alternate schema
        """
        query_alt = "SELECT host_key,name,value,path,creation_utc,last_access_utc,expires_utc,is_secure," \
                    "is_httponly,has_expires,is_persistent,priority FROM cookies ORDER BY creation_utc;"
        try:
            cur = db_connection.cursor()
            cur.execute(query_alt)
            rows = cur.fetchall()
            for row in rows:
                creation_utc = riplib.osxripper_time.get_gregorian_micros(row["creation_utc"])
                last_access_utc = riplib.osxripper_time.get_gregorian_micros(row["last_access_utc"])
                expires_utc = riplib.osxripper_time.get_gregorian_micros(row["expires_utc"])

                output_file.write("Host Key       : {0}\r\n".format(row["host_key"]))
                output_file.write("Name           : {0}\r\n".format(row["name"]))
                output_file.write("Value          : {0}\r\n".format(row["value"]))
                output_file.write("Path           : {0}\r\n".format(row["path"]))
                output_file.write("Creation UTC   : {0}\r\n".format(creation_utc))
                output_file.write("Last Access UTC: {0}\r\n".format(last_access_utc))
                output_file.write("Expires UTC    : {0}\r\n".format(expires_utc))
                output_file.write("Secure         : {0}\r\n".format(row["is_secure"]))
                output_file.write("HTTP Only      : {0}\r\n".format(row["is_httponly"]))
                output_file.write("Has Expires    : {0}\r\n".format(row["has_expires"]))
                output_file.write("Persistent     : {0}\r\n".format(row["is_persistent"]))
                output_file.write("Priority       : {0}\r\n".format(row["priority"]))
                output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))
        finally:
            if db_connection:
                db_connection.close()
