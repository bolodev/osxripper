""" Module to parse commerce plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersCommercePlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.commerce.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Appstore")
        self.set_description("Parse information from /Users/username/Library/Preferences/com.apple.commerce.plist")
        self.set_data_file("com.apple.commerce.plist")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("bplist")

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
                    plist = os.path.join(users_path, username, "Library", "Preferences", self._data_file)
                    if os.path.isfile(plist):
                        self.__parse_bplist(plist, username)
                    else:
                        logging.warning("%s does not exist.", plist)
                        print("[WARNING] {0} does not exist.".format(plist))
        else:
            logging.warning("%s does not exist.", users_path)
            print("[WARNING] {0} does not exist.".format(users_path))

    def __parse_bplist(self, file, username):
        """
        Parse /Users/username/Library/Preferences/com.apple.commerce.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                bplist = open(file, "rb")
                plist = riplib.ccl_bplist.load(bplist)
                bplist.close()
                try:
                    if "AllowLegacyConversion" in plist:
                        output_file.write("Allow Legacy Conversion     : {0}\r\n".format(plist["AllowLegacyConversion"]))
                    if "LastAutoUpdateInvocation" in plist:
                        output_file.write("Last Auto Update Invocation : {0}\r\n".format(plist["LastAutoUpdateInvocation"]))
                    accounts = plist["KnownAccounts"]
                    output_file.write("Accounts:\r\n\r\n")
                    for account in accounts:
                        output_file.write("\tAccount:\r\n")
                        if "identifier" in account:
                            output_file.write("\t\tIdentifier: {0}\r\n".format(account["identifier"]))
                        if "dsid" in account:
                            output_file.write("\t\tDSID: {0}\r\n".format(account["dsid"]))
                        if "signedin" in account:
                            output_file.write("\t\tSigned In: {0}\r\n".format(account["signedin"]))
                        if "credit" in account:
                            if len(account["credit"]) == 0:
                                output_file.write("\t\tCredit: No credit.\r\n")
                            else:
                                output_file.write("\t\tCredit: {0}\r\n".format(account["credit"]))
                        if "kind" in account:
                            output_file.write("\t\tAcct. Kind: {0}\r\n".format(account["kind"]))
                        if "storefront" in account:
                            output_file.write("\t\tStorefront: {0}\r\n".format(account["storefront"]))
                        if "bagtype" in account:
                            output_file.write("\t\tBag Type: {0}\r\n".format(account["bagtype"]))
                        output_file.write("\r\n")

                    if "PurchasesInflight" in plist:
                        output_file.write("Purchases Inflight          : {0}\r\n".format(plist["PurchasesInflight"]))
                    if "PrimaryAccountMigrated" in plist:
                        output_file.write("Primary Account Migrated    : {0}\r\n".format(plist["PrimaryAccountMigrated"]))
                    if "NextClientIDPingDate" in plist:
                        output_file.write("Next Client ID Ping Date    : {0}\r\n".format(plist["NextClientIDPingDate"]))
                except KeyError:
                    pass
            elif self._os_version in ["mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
