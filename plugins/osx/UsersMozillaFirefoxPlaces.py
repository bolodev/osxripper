from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersMozillaFirefoxPlaces(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Firefox/Profiles/*.default/places.sqlite
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Mozilla Firefox Places"
        self._description = "Parse information from " \
                            "/Users/<username>/Library/Application Support/Firefox/Profiles/*.default/places.sqlite"
        self._data_file = "places.sqlite"
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
                    profile_search_path = os.path\
                        .join(users_path, username, "Library", "Application Support", "Firefox", "Profiles")
                    if os.path.isdir(profile_search_path):
                        profiles_list = os.listdir(profile_search_path)
                        for profile in profiles_list:
                            if profile.endswith(".default"):
                                sqlite_db = os.path.join(profile_search_path, profile, self._data_file)
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
        Read the places.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Firefox_Places.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if os.path.isfile(file):
                of.write("Source File: {0}\r\n\r\n".format(file))
                conn = None
                try:
                    query = "SELECT url, title, rev_host, visit_count," \
                            "last_visit_date," \
                            "hidden, typed FROM moz_places ORDER BY visit_count DESC"
                    conn = sqlite3.connect(file)
                    conn.row_factory = sqlite3.Row
                    with conn:
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        for row in rows:
                            last_visit_date = riplib.osxripper_time.get_unix_micros(row["last_visit_date"])
                            of.write("URL            : {0}\r\n".format(row["url"]))
                            of.write("Title          : {0}\r\n".format(row["title"]))
                            of.write("Rev. Host      : {0}\r\n".format(row["rev_host"]))
                            of.write("Visit Count    : {0}\r\n".format(row["visit_count"]))
                            of.write("Last Visit Date: {0}\r\n".format(last_visit_date))
                            of.write("Hidden         : {0}\r\n".format(row["hidden"]))
                            of.write("Typed          : {0}\r\n".format(row["typed"]))
                            of.write("\r\n")

                        of.write("="*10 + " Mozilla Firefox Annotations " + "="*10 + "\r\n")
                        query = "SELECT mp.url,ma.content,maa.name," \
                                "ma.dateAdded," \
                                "ma.lastModified " \
                                "FROM moz_annos ma,moz_anno_attributes maa,moz_places mp " \
                                "WHERE ma.anno_attribute_id = maa.id AND mp.id = ma.place_id"
                        cur.execute(query)
                        rows = cur.fetchall()
                        for row in rows:
                            date_added = riplib.osxripper_time.get_unix_micros(row["dateAdded"])
                            last_modified = riplib.osxripper_time.get_unix_micros(row["lastModified"])
                            of.write("URL               : {0}\r\n".format(row["url"]))
                            of.write("Content           : {0}\r\n".format(row["content"]))
                            of.write("Name              : {0}\r\n".format(row["name"]))
                            of.write("Date Added        : {0}\r\n".format(date_added))
                            of.write("Date Last Modified: {0}\r\n".format(last_modified))
                            of.write("\r\n")

                        of.write("="*10 + " Mozilla Firefox Input History " + "="*10 + "\r\n")
                        query = "SELECT mp.url,mi.input,mi.use_count FROM moz_inputhistory mi,moz_places mp " \
                                "WHERE mi.place_id = mp.id ORDER BY use_count DESC"
                        cur.execute(query)
                        rows = cur.fetchall()
                        if len(rows) == 0:
                            of.write("No input history data.\r\n\r\n")
                        else:
                            for row in rows:
                                of.write("URL      : {0}\r\n".format(row["url"]))
                                of.write("Input    : {0}\r\n".format(row["input"]))
                                of.write("Use Count: {0}\r\n".format(row["use_count"]))
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
