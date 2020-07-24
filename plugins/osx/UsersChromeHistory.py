""" Module to parse Google Chrome History """
import codecs
import logging
import os
import sqlite3
import riplib.osxripper_time
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersChromeHistory(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/History
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Chrome Browser History")
        self.set_description("Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/History ")
        self.set_data_file("History")
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
        Read the History SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_History.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, "History")
            query = "SELECT id, url,title,term,visit_count,last_visit_time," \
                    "typed_count,hidden FROM urls, keyword_search_terms WHERE keyword_search_terms.url_id=urls.id"
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
                            last_visit_time = riplib.osxripper_time.get_gregorian_micros(row["last_visit_time"])
                            output_file.write("ID         : {0}\r\n".format(row["id"]))
                            output_file.write("URL        : {0}\r\n".format(row["url"]))
                            output_file.write("Title      : {0}\r\n".format(row["term"]))
                            output_file.write("Search Term: {0}\r\n".format(row["term"]))
                            output_file.write("Visit Count: {0}\r\n".format(row["visit_count"]))
                            output_file.write("Last Visit : {0}\r\n".format(last_visit_time))
                            output_file.write("Typed Count: {0}\r\n".format(row["typed_count"]))
                            output_file.write("Hidden     : {0}\r\n".format(row["hidden"]))
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
