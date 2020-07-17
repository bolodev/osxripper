from riplib.plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersSafariWebIcons(Plugin):
    """
    Parse information from /Users/<username>/Library/Safari/WebpageIcons.db
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Safari Webpage Icons"
        self._description = "Parse information from /Users/<username>/Library/Safari/WebpageIcons.db"
        self._data_file = "WebpageIcons.db"
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
                    sqlite_db = os.path.join(users_path, username, "Library", "Safari", self._data_file)
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
        Read the WebpageIcons.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Webpage_Icons.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra"]:
            if self._os_version in ["catalina", "mojave", "high_sierra"]:
                # Does not exist
                return
            elif self._os_version in ["sierra", "el_capitan", "yosemite", "mavericks",
                                    "mountain_lion", "lion", "snow_leopard"]:
                query = "SELECT pu.url AS p_url,ii.url AS i_url,ii.stamp FROM IconInfo ii,PageURL pu " \
                        "WHERE pu.iconID = ii.iconID"
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
                                stamp = riplib.osxripper_time.get_unix_seconds(row["stamp"])
                                of.write("Page URL      : {0}\r\n".format(row["p_url"]))
                                of.write("Icon URL      : {0}\r\n".format(row["i_url"]))
                                of.write("Timestamp     : {0}\r\n".format(stamp))
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
