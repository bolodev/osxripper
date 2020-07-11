from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersChromeDownloads(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/History
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Chrome Browser Download History"
        self._description = "Parse information from " \
                            "/Users/<username>/Library/Application Support/Google/Chrome/Default/History"
        self._data_file = "History"
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
        with codecs.open(os.path.join(self._output_dir, "Users_" + username
                + "_Chrome_Downloads.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, "History")
            query = "SELECT id, current_path, target_path," \
                    "start_time," \
                    "received_bytes, total_bytes, referrer FROM downloads"
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
                            start_time = riplib.osxripper_time.get_gregorian_micros(row["start_time"])
                            of.write("ID          : {0}\r\n".format(row["id"]))
                            of.write("Current Path: {0}\r\n".format(row["current_path"]))
                            of.write("Target Path : {0}\r\n".format(row["target_path"]))
                            of.write("Start Time  : {0}\r\n".format(start_time))
                            of.write("Received    : {0}\r\n".format(row["received_bytes"]))
                            of.write("Total Bytes : {0}\r\n".format(row["total_bytes"]))
                            of.write("Referer     : {0}\r\n".format(row["referrer"]))
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
