""" Module to parse Safari History plist """
import codecs
import datetime
import logging
import os
import sqlite3
import riplib.ccl_bplist
import riplib.osxripper_time
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersSafariHistory(Plugin):
    """
    Parse information from /Users/<username>/Library/Safari/History.db or /Users/<username>/Library/Safari/History.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Safari History")
        self.set_description("Parse information from /Users/<username>/Library/Safari")
        self.set_data_file("")  # multiple files, Yosemite is a SQLite DB and others are Plists
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("multi")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    history_path = os.path.join(users_path, username, "Library", "Safari")
                    if os.path.isdir(history_path):
                        # if self._os_version in ["big_sur", "catalina"]:
                        if self._os_version in ["catalina"]:
                            self._parse_sqlite_db2(history_path, username)
                        if self._os_version in ["mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                            self.__parse_sqlite_db(history_path, username)
                        elif self._os_version in ["mavericks", "mountain_lion", "lion", "snow_leopard"]:
                            self.__parse_history_plist(history_path, username)
                        else:
                            logging.warning("Not a known OSX version.")
                            print("[WARNING] Not a known OSX version.")
                    else:
                        logging.warning("%s does not exist.", history_path)
                        print("[WARNING] {0} does not exist.".format(history_path))
        else:
            logging.warning("%s does not exist.", users_path)
            print("[WARNING] {0} does not exist.".format(users_path))

    def _parse_sqlite_db2(self, file, username):
        """
        Read the History.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_History.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("=" * 10 + " " + self._name + " " + "=" * 10 + "\r\n")
            history_db = os.path.join(file, "History.db")
            query = "SELECT hi.id,hi.url,hi.visit_count,hv.visit_time," \
                    "hv.title,hv.redirect_source,hv.redirect_destination " \
                    "FROM history_items hi,history_visits hv" \
                    " WHERE hi.id = hv.history_item"
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
                            visit_time = riplib.osxripper_time.get_cocoa_seconds(row["visit_time"])
                            output_file.write("ID               : {0}\r\n".format(row["id"]))
                            output_file.write("URL              : {0}\r\n".format(row["url"]))
                            output_file.write("Visit Count      : {0}\r\n".format(row["visit_count"]))
                            output_file.write("Visit Time       : {0}\r\n".format(visit_time))
                            output_file.write("Title            : {0}\r\n".format(row["title"]))
                            output_file.write("Redirect ID      : {0}\r\n".format(row["redirect_source"]))
                            output_file.write("Redirect Dest. ID: {0}\r\n".format(row["redirect_destination"]))
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
            output_file.write("=" * 40 + "\r\n\r\n")
        output_file.close()

    def __parse_sqlite_db(self, file, username):
        """
        Read the History.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_History.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, "History.db")
            query = "SELECT hi.id,hi.url,hi.visit_count,hv.visit_time," \
                    "hv.title,hv.redirect_source,hv.redirect_destination " \
                    "FROM history_items hi,history_visits hv" \
                    " WHERE hi.id = hv.id"
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
                            visit_time = riplib.osxripper_time.get_cocoa_seconds(row["visit_time"])
                            output_file.write("ID               : {0}\r\n".format(row["id"]))
                            output_file.write("URL              : {0}\r\n".format(row["url"]))
                            output_file.write("Visit Count      : {0}\r\n".format(row["visit_count"]))
                            output_file.write("Visit Time       : {0}\r\n".format(visit_time))
                            output_file.write("Title            : {0}\r\n".format(row["title"]))
                            output_file.write("Redirect ID      : {0}\r\n".format(row["redirect_source"]))
                            output_file.write("Redirect Dest. ID: {0}\r\n".format(row["redirect_destination"]))
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

    def __parse_history_plist(self, file, username):
        """
        Read the History.plist
        """
        mac_absolute = datetime.datetime(2001, 1, 1, 0, 0, 0)
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_History.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_plist = os.path.join(file, "History.plist")
            if os.path.isfile(history_plist):
                output_file.write("Source File: {0}\r\n\r\n".format(history_plist))
                bplist = open(history_plist, "rb")
                plist = riplib.ccl_bplist.load(bplist)
            try:
                if "WebHistoryFileVersion" in plist:
                    output_file.write("Web History File Version: {0}\r\n".format(plist["WebHistoryFileVersion"]))
                if "WebHistoryDates" in plist:
                    output_file.write("Web History:\r\n")
                    for whd in plist["WebHistoryDates"]:
                        output_file.write("\tURL: {0}\r\n".format(whd[""]))
                        # title
                        if "title" in whd:
                            output_file.write("\tTitle: {0}\r\n".format(whd["title"]))
                        if "lastVisitedDate" in whd:
                            output_file.write("\tLast Visited Date: {0}\r\n".format(mac_absolute + datetime.timedelta(0, float(whd["lastVisitedDate"]))))
                        if "visitCount" in whd:
                            output_file.write("\tVisit Count: {0}\r\n".format(whd["visitCount"]))
                        if "redirectURLs" in whd:
                            for redirect in whd["redirectURLs"]:
                                output_file.write("\tRedirect URL: {0}\r\n".format(redirect))
                        output_file.write("\r\n")
                if "WebHistoryDomains.v2" in plist:
                    output_file.write("Web History Domains v2:\r\n")

                output_file.write("\r\n")
            except KeyError:
                pass
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
