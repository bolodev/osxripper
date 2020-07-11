from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.osxripper_time
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersChromeWebData(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Web Data
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Chrome Browser Web Data"
        self._description = "Parse information from " \
                            "/Users/<username>/Library/Application Support/Google/Chrome/Default/Web Data"
        self._data_file = "Web Data"
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
        Read the Web Data SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_Web_Data.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            web_data_db = os.path.join(file, "Web Data")

            query = "SELECT name,value,value_lower,date_created,date_last_used,count FROM autofill"
            if os.path.isfile(web_data_db):
                of.write("Source File: {0}\r\n\r\n".format(web_data_db))
                conn = None
                try:
                    conn = sqlite3.connect(web_data_db)
                    conn.row_factory = sqlite3.Row
                    with conn:    
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                date_created = riplib.osxripper_time.get_unix_seconds(row["date_created"])
                                date_last_used = riplib.osxripper_time.get_unix_seconds(row["date_last_used"])
                                of.write("Name          : {0}\r\n".format(row["name"]))
                                of.write("Value         : {0}\r\n".format(row["value"]))
                                of.write("Value Lower   : {0}\r\n".format(row["value_lower"]))
                                of.write("Date Created  : {0}\r\n".format(date_created))
                                of.write("Date Last Used: {0}\r\n".format(date_last_used))
                                of.write("Count         : {0}\r\n".format(row["count"]))
                        else:
                            of.write("No data found in Autofill table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid, email FROM autofill_profile_emails"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profile Emails " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                of.write("GUID : {0}\r\n".format(row["guid"]))
                                of.write("Email: {0}\r\n".format(row["email"]))
                        else:
                            of.write("No data found in Autofill Profile Email table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid, first_name, middle_name, last_name, full_name FROM autofill_profile_names"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profile Names " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                of.write("GUID       : {0}\r\n".format(row["guid"]))
                                of.write("First Name : {0}\r\n".format(row["first_name"]))
                                of.write("Middle Name: {0}\r\n".format(row["middle_name"]))
                                of.write("Last Name  : {0}\r\n".format(row["last_name"]))
                                of.write("Full Name  : {0}\r\n".format(row["full_name"]))
                        else:
                            of.write("No data found in Autofill Profile Names table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid, number FROM autofill_profile_phones"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profile Phones " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                of.write("GUID        : {0}\r\n".format(row["guid"]))
                                of.write("Phone Number: {0}\r\n".format(row["number"]))
                        else:
                            of.write("No data found in Autofill Profile Phones table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid,company_name,street_address,dependent_locality,city,state,zipcode," \
                                "sorting_code,country_code," \
                                "date_modified," \
                                "origin,language_code FROM autofill_profiles"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profiles " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                date_modified = riplib.osxripper_time.get_unix_seconds(row["date_modified"])
                                of.write("GUID              : {0}\r\n".format(row["guid"]))
                                of.write("Company Name      : {0}\r\n".format(row["company_name"]))
                                of.write("Street Address    : {0}\r\n".format(row["street_address"]))
                                of.write("Dependent Locality: {0}\r\n".format(row["dependent_locality"]))
                                of.write("City              : {0}\r\n".format(row["city"]))
                                of.write("State             : {0}\r\n".format(row["state"]))
                                of.write("Zipcode           : {0}\r\n".format(row["zipcode"]))
                                of.write("Sorting Code      : {0}\r\n".format(row["sorting_code"]))
                                of.write("Country Code      : {0}\r\n".format(row["country_code"]))
                                of.write("Date Modified     : {0}\r\n".format(date_modified))
                                of.write("Origin            : {0}\r\n".format(row["origin"]))
                                of.write("Language Code     : {0}\r\n".format(row["language_code"]))
                        else:
                            of.write("No data found in Autofill Profiles table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid FROM autofill_profiles_trash"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profile Trash " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("GUID:\r\n")
                                else:
                                    of.write("GUID: {0}\r\n".format(row[0]))
                        else:
                            of.write("No data found in Autofill Profile Trash table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid, name_on_card,expiration_month,expiration_year,date_modified,origin " \
                                "FROM credit_cards"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Credit Cards " + "="*10 + "\r\n")
                        of.write("N.B. Card Number is encrypted. Ommitted by plugin.\r\n\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                date_modified = riplib.osxripper_time.get_unix_seconds(row["date_modified"])
                                of.write("GUID            : {0}\r\n".format(row["guid"]))
                                of.write("Name on Card    : {0}\r\n".format(row["name_on_card"]))
                                of.write("Expiration Month: {0}\r\n".format(row["expiration_month"]))
                                of.write("Expiration Year : {0}\r\n".format(row["expiration_year"]))
                                of.write("Date Modified   : {0}\r\n".format(date_modified))
                                of.write("Origin          : {0}\r\n".format(row["origin"]))
                        else:
                            of.write("No data found in Credit Cards table.\r\n")
                        of.write("\r\n")

                        query = "SELECT	id,short_name,keyword,favicon_url,url,safe_for_autoreplace," \
                                "originating_url,date_created,usage_count,input_encodings,suggest_url," \
                                "prepopulate_id,created_by_policy,last_modified,sync_guid,alternate_urls," \
                                "image_url,search_url_post_params,suggest_url_post_params,image_url_post_params," \
                                "new_tab_url FROM keywords"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Keywords " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                kw_created = riplib.osxripper_time.get_unix_seconds(row["date_created"])
                                kw_modified = riplib.osxripper_time.get_unix_seconds(row["last_modified"])
                                of.write("ID                          : {0}\r\n".format(row["id"]))
                                of.write("Short Name                  : {0}\r\n".format(row["short_name"]))
                                of.write("Keyword                     : {0}\r\n".format(row["keyword"]))
                                of.write("FavIcon URL                 : {0}\r\n".format(row["favicon_url"]))
                                of.write("URL                         : {0}\r\n".format(row["url"]))
                                of.write("Safe for Autoreplace        : {0}\r\n".format(row["safe_for_autoreplace"]))
                                of.write("Originating URL             : {0}\r\n".format(row["originating_url"]))
                                of.write("Date Created                : {0}\r\n".format(kw_created))
                                of.write("Usage Count                 : {0}\r\n".format(row["usage_count"]))
                                of.write("Input Encodings             : {0}\r\n".format(row["input_encodings"]))
                                # of.write("Show in Default List        : {0}\r\n".format(row["show_in_default_list"]))
                                of.write("Suggest URL                 : {0}\r\n".format(row["suggest_url"]))
                                of.write("Prepoulate ID               : {0}\r\n".format(row["prepopulate_id"]))
                                of.write("Created by Policy           : {0}\r\n".format(row["created_by_policy"]))
                                # of.write("Instant URL                 : {0}\r\n".format(row["instant_url"]))
                                of.write("Last Modified               : {0}\r\n".format(kw_modified))
                                of.write("Sync GUID                   : {0}\r\n".format(row["sync_guid"]))
                                of.write("Alternate URLs              : {0}\r\n".format(row["alternate_urls"]))
                                # of.write("Search Terms Replacement Key: {0}\r\n".
                                #          format(row["search_terms_replacement_key"]))
                                of.write("Image URL                   : {0}\r\n".format(row["image_url"]))
                                of.write("Search URL POST Params      : {0}\r\n".format(row["search_url_post_params"]))
                                of.write("Suggest URL POST Params     : {0}\r\n".format(row["suggest_url_post_params"]))
                                # of.write("Instant URL POST Params
                                # : {0}\r\n".format(row["instant_url_post_params"]))
                                of.write("Image URL POST Params       : {0}\r\n".format(row["image_url_post_params"]))
                                of.write("New Tab URL                 : {0}\r\n".format(row["new_tab_url"]))
                                of.write("\r\n")
                        else:
                            of.write("No data found in Keywords table.\r\n")
                        of.write("\r\n")

                        query = "SELECT service FROM token_service"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Token Service " + "="*10 + "\r\n")
                        of.write("N.B. Service tokens are encrypted. Not retrieved by this plugin\r\n\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                of.write("Service: {0}\r\n".format(row["service"]))
                        else:
                            of.write("No data found in Token Service table.\r\n")
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
