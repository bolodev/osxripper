""" Module to parse Autofill data form Google Chrome """
import codecs
import logging
import os
import sqlite3
import riplib.osxripper_time
from riplib.plugin import Plugin


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
        self.set_name("User Chrome Browser Web Data")
        self.set_description("Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Web Data")
        self.set_data_file("Web Data")
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
        Read the Web Data SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_Web_Data.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            web_data_db = os.path.join(file, "Web Data")

            if os.path.isfile(web_data_db):
                output_file.write("Source File: {0}\r\n\r\n".format(web_data_db))
                conn = None
                try:
                    conn = sqlite3.connect(web_data_db)
                    conn.row_factory = sqlite3.Row
                    self._parse_autofill(output_file, conn)
                    self._parse_autofill_profile_emails(output_file, conn)
                    self._parse_autofill_profile_names(output_file, conn)
                    self._parse_autofill_profile_phones(output_file, conn)
                    self._parse_autofill_profiles(output_file, conn)
                    self._parse_autofill_profiles_trash(output_file, conn)
                    self._parse_credit_cards(output_file, conn)
                    self._parse_keywords(output_file, conn)
                    self._parse_service(output_file, conn)
                finally:
                    if conn:
                        conn.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()


    @classmethod
    def _parse_autofill(cls, output_file, db_connection):
        """
        Collate data from autofill table
        """
        try:
            query = "SELECT name,value,value_lower,date_created,date_last_used,count FROM autofill"
            cur = db_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            output_file.write("="*10 + " Autofill " + "="*10 + "\r\n")
            if len(rows) != 0:
                for row in rows:
                    date_created = riplib.osxripper_time.get_unix_seconds(row["date_created"])
                    date_last_used = riplib.osxripper_time.get_unix_seconds(row["date_last_used"])
                    output_file.write("Name          : {0}\r\n".format(row["name"]))
                    output_file.write("Value         : {0}\r\n".format(row["value"]))
                    output_file.write("Value Lower   : {0}\r\n".format(row["value_lower"]))
                    output_file.write("Date Created  : {0}\r\n".format(date_created))
                    output_file.write("Date Last Used: {0}\r\n".format(date_last_used))
                    output_file.write("Count         : {0}\r\n".format(row["count"]))
            else:
                output_file.write("No data found in Autofill table.\r\n")
            if cur:
                cur.close()
            output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))


    @classmethod
    def _parse_autofill_profile_emails(cls, output_file, db_connection):
        """
        Collate data from autofill profiles emails table
        """
        try:
            query = "SELECT guid, email FROM autofill_profile_emails"
            cur = db_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            output_file.write("="*10 + " Autofill Profile Emails " + "="*10 + "\r\n")
            if len(rows) != 0:
                for row in rows:
                    output_file.write("GUID : {0}\r\n".format(row["guid"]))
                    output_file.write("Email: {0}\r\n".format(row["email"]))
            else:
                output_file.write("No data found in Autofill Profile Email table.\r\n")
            if cur:
                cur.close()
            output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))


    @classmethod
    def _parse_autofill_profile_names(cls, output_file, db_connection):
        """
        Collate data from autofill profiles names table
        """
        try:
            query = "SELECT guid, first_name, middle_name, last_name, full_name FROM autofill_profile_names"
            cur = db_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            output_file.write("="*10 + " Autofill Profile Names " + "="*10 + "\r\n")
            if len(rows) != 0:
                for row in rows:
                    output_file.write("GUID       : {0}\r\n".format(row["guid"]))
                    output_file.write("First Name : {0}\r\n".format(row["first_name"]))
                    output_file.write("Middle Name: {0}\r\n".format(row["middle_name"]))
                    output_file.write("Last Name  : {0}\r\n".format(row["last_name"]))
                    output_file.write("Full Name  : {0}\r\n".format(row["full_name"]))
            else:
                output_file.write("No data found in Autofill Profile Names table.\r\n")
            if cur:
                cur.close()
            output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))


    @classmethod
    def _parse_autofill_profile_phones(cls, output_file, db_connection):
        """
        Collate data from autofill profiles phones table
        """
        try:
            query = "SELECT guid, number FROM autofill_profile_phones"
            cur = db_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            output_file.write("="*10 + " Autofill Profile Phones " + "="*10 + "\r\n")
            if len(rows) != 0:
                for row in rows:
                    output_file.write("GUID        : {0}\r\n".format(row["guid"]))
                    output_file.write("Phone Number: {0}\r\n".format(row["number"]))
            else:
                output_file.write("No data found in Autofill Profile Phones table.\r\n")
            if cur:
                cur.close()
            output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))


    @classmethod
    def _parse_autofill_profiles(cls, output_file, db_connection):
        """
        Collate data from autofill profiles table
        """
        try:
            query = "SELECT guid,company_name,street_address,dependent_locality,city,state,zipcode," \
                    "sorting_code,country_code," \
                    "date_modified," \
                    "origin,language_code FROM autofill_profiles"
            cur = db_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            output_file.write("="*10 + " Autofill Profiles " + "="*10 + "\r\n")
            if len(rows) != 0:
                for row in rows:
                    date_modified = riplib.osxripper_time.get_unix_seconds(row["date_modified"])
                    output_file.write("GUID              : {0}\r\n".format(row["guid"]))
                    output_file.write("Company Name      : {0}\r\n".format(row["company_name"]))
                    output_file.write("Street Address    : {0}\r\n".format(row["street_address"]))
                    output_file.write("Dependent Locality: {0}\r\n".format(row["dependent_locality"]))
                    output_file.write("City              : {0}\r\n".format(row["city"]))
                    output_file.write("State             : {0}\r\n".format(row["state"]))
                    output_file.write("Zipcode           : {0}\r\n".format(row["zipcode"]))
                    output_file.write("Sorting Code      : {0}\r\n".format(row["sorting_code"]))
                    output_file.write("Country Code      : {0}\r\n".format(row["country_code"]))
                    output_file.write("Date Modified     : {0}\r\n".format(date_modified))
                    output_file.write("Origin            : {0}\r\n".format(row["origin"]))
                    output_file.write("Language Code     : {0}\r\n".format(row["language_code"]))
            else:
                output_file.write("No data found in Autofill Profiles table.\r\n")
            if cur:
                cur.close()
            output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))


    @classmethod
    def _parse_autofill_profiles_trash(cls, output_file, db_connection):
        """
        Collate data from autofill profiles trash table
        """
        try:
            query = "SELECT guid FROM autofill_profiles_trash"
            cur = db_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            output_file.write("="*10 + " Autofill Profile Trash " + "="*10 + "\r\n")
            if len(rows) != 0:
                for row in rows:
                    if row[0] is None:
                        output_file.write("GUID:\r\n")
                    else:
                        output_file.write("GUID: {0}\r\n".format(row[0]))
            else:
                output_file.write("No data found in Autofill Profile Trash table.\r\n")
            if cur:
                cur.close()
            output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))


    @classmethod
    def _parse_credit_cards(cls, output_file, db_connection):
        """
        Collate data from credit cards table
        """
        try:
            query = "SELECT guid, name_on_card,expiration_month,expiration_year,date_modified,origin " \
                    "FROM credit_cards"
            cur = db_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            output_file.write("="*10 + " Credit Cards " + "="*10 + "\r\n")
            output_file.write("N.B. Card Number is encrypted. Ommitted by plugin.\r\n\r\n")
            if len(rows) != 0:
                for row in rows:
                    date_modified = riplib.osxripper_time.get_unix_seconds(row["date_modified"])
                    output_file.write("GUID            : {0}\r\n".format(row["guid"]))
                    output_file.write("Name on Card    : {0}\r\n".format(row["name_on_card"]))
                    output_file.write("Expiration Month: {0}\r\n".format(row["expiration_month"]))
                    output_file.write("Expiration Year : {0}\r\n".format(row["expiration_year"]))
                    output_file.write("Date Modified   : {0}\r\n".format(date_modified))
                    output_file.write("Origin          : {0}\r\n".format(row["origin"]))
            else:
                output_file.write("No data found in Credit Cards table.\r\n")
            if cur:
                cur.close()
            output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))


    @classmethod
    def _parse_keywords(cls, output_file, db_connection):
        """
        Collate data from keywords table
        """
        try:
            query = "SELECT	id,short_name,keyword,favicon_url,url,safe_for_autoreplace," \
                    "originating_url,date_created,usage_count,input_encodings,suggest_url," \
                    "prepopulate_id,created_by_policy,last_modified,sync_guid,alternate_urls," \
                    "image_url,search_url_post_params,suggest_url_post_params,image_url_post_params," \
                    "new_tab_url FROM keywords"
            cur = db_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            output_file.write("="*10 + " Keywords " + "="*10 + "\r\n")
            if len(rows) != 0:
                for row in rows:
                    kw_created = riplib.osxripper_time.get_unix_seconds(row["date_created"])
                    kw_modified = riplib.osxripper_time.get_unix_seconds(row["last_modified"])
                    output_file.write("ID                          : {0}\r\n".format(row["id"]))
                    output_file.write("Short Name                  : {0}\r\n".format(row["short_name"]))
                    output_file.write("Keyword                     : {0}\r\n".format(row["keyword"]))
                    output_file.write("FavIcon URL                 : {0}\r\n".format(row["favicon_url"]))
                    output_file.write("URL                         : {0}\r\n".format(row["url"]))
                    output_file.write("Safe for Autoreplace        : {0}\r\n".format(row["safe_for_autoreplace"]))
                    output_file.write("Originating URL             : {0}\r\n".format(row["originating_url"]))
                    output_file.write("Date Created                : {0}\r\n".format(kw_created))
                    output_file.write("Usage Count                 : {0}\r\n".format(row["usage_count"]))
                    output_file.write("Input Encodings             : {0}\r\n".format(row["input_encodings"]))
                    # output_file.write("Show in Default List        : {0}\r\n".format(row["show_in_default_list"]))
                    output_file.write("Suggest URL                 : {0}\r\n".format(row["suggest_url"]))
                    output_file.write("Prepoulate ID               : {0}\r\n".format(row["prepopulate_id"]))
                    output_file.write("Created by Policy           : {0}\r\n".format(row["created_by_policy"]))
                    # output_file.write("Instant URL                 : {0}\r\n".format(row["instant_url"]))
                    output_file.write("Last Modified               : {0}\r\n".format(kw_modified))
                    output_file.write("Sync GUID                   : {0}\r\n".format(row["sync_guid"]))
                    output_file.write("Alternate URLs              : {0}\r\n".format(row["alternate_urls"]))
                    # output_file.write("Search Terms Replacement Key: {0}\r\n".
                    #          format(row["search_terms_replacement_key"]))
                    output_file.write("Image URL                   : {0}\r\n".format(row["image_url"]))
                    output_file.write("Search URL POST Params      : {0}\r\n".format(row["search_url_post_params"]))
                    output_file.write("Suggest URL POST Params     : {0}\r\n".format(row["suggest_url_post_params"]))
                    # output_file.write("Instant URL POST Params
                    # : {0}\r\n".format(row["instant_url_post_params"]))
                    output_file.write("Image URL POST Params       : {0}\r\n".format(row["image_url_post_params"]))
                    output_file.write("New Tab URL                 : {0}\r\n".format(row["new_tab_url"]))
                    output_file.write("\r\n")
            else:
                output_file.write("No data found in Keywords table.\r\n")
            if cur:
                cur.close()
            output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))


    @classmethod
    def _parse_service(cls, output_file, db_connection):
        """
        Collate data from token service table
        """
        try:
            query = "SELECT service FROM token_service"
            cur = db_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            output_file.write("="*10 + " Token Service " + "="*10 + "\r\n")
            output_file.write("N.B. Service tokens are encrypted. Not retrieved by this plugin\r\n\r\n")
            if len(rows) != 0:
                for row in rows:
                    output_file.write("Service: {0}\r\n".format(row["service"]))
            else:
                output_file.write("No data found in Token Service table.\r\n")
            if cur:
                cur.close()
            output_file.write("\r\n")
        except sqlite3.Error as error:
            logging.error("%s", error.args[0])
            print("[ERROR] {0}".format(error.args[0]))
