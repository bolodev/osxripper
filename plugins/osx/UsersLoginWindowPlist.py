""" Module to parse LoginWindow plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersLoginWindowPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.loginwindow.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Login Window")
        self.set_description("Parse information from /Users/username/Library/Preferences/com.apple.loginwindow.plist")
        self.set_data_file("com.apple.loginwindow.plist")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("bplist")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
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
        Parse /Users/username/Library/Preferences/com.apple.loginwindow.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                parse_os = Parse01(output_file, file)
                parse_os.parse()
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion"]:
                parse_os = Parse02(output_file, file)
                parse_os.parse()
            elif self._os_version == "lion":
                parse_os = Parse03(output_file, file)
                parse_os.parse()
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()

class Parse01():
    """
    Convenience class for parsing macOS data
    """
    def __init__(self, output_file, data_file):
        self._output_file = output_file
        self._data_file = data_file

    def parse(self):
        """
        Parse data
        """
        if os.path.isfile(self._data_file):
            bplist = open(self._data_file, "rb")
            plist = riplib.ccl_bplist.load(bplist)
            try:
                if "TALLogoutReason" in plist:
                    self._output_file.write("Logout Reason     : {0}\r\n".format(plist["TALLogoutReason"]))
            except KeyError:
                pass
            bplist.close()
        else:
            logging.warning("File: %s does not exist or cannot be found.\r\n", self._data_file)
            self._output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
            print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))

class Parse02():
    """
    Convenience class for parsing macOS data
    """
    def __init__(self, output_file, data_file):
        self._output_file = output_file
        self._data_file = data_file

    def parse(self):
        """
        Parse data
        """
        if os.path.isfile(self._data_file):
            bplist = open(self._data_file, "rb")
            plist = riplib.ccl_bplist.load(bplist)
            try:
                if "TALLogoutReason" in plist:
                    self._output_file.write("Logout Reason     : {0}\r\n".format(plist["TALLogoutReason"]))
                if "TALLogoutSavesState" in plist:
                    self._output_file.write("Save State        : {0}\r\n".format(plist["TALLogoutSavesState"]))
            except KeyError:
                pass
            bplist.close()
        else:
            logging.warning("File: %s does not exist or cannot be found.\r\n", self._data_file)
            self._output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
            print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))

class Parse03():
    """
    Convenience class for parsing macOS data
    """
    def __init__(self, output_file, data_file):
        self._output_file = output_file
        self._data_file = data_file

    def parse(self):
        """
        Parse data
        """
        if os.path.isfile(self._data_file):
            bplist = open(self._data_file, "rb")
            plist = riplib.ccl_bplist.load(bplist)
            try:
                if "TALLogoutReason" in plist:
                    self._output_file.write("Logout Reason        : {0}\r\n".format(plist["TALLogoutReason"]))
                if "AutoOpenedWindowDictionary" in plist:
                    auto_open = plist["AutoOpenedWindowDictionary"]
                    if "CurrentSpaceID" in auto_open:
                        self._output_file.write("Current Space ID     : {0}\r\n".format(auto_open["CurrentSpaceID"]))
                    if "NumberOfSpaces" in auto_open:
                        self._output_file.write("Number Of Spaces     : {0}\r\n".format(auto_open["NumberOfSpaces"]))
            except KeyError:
                pass
            bplist.close()
        else:
            logging.warning("File: %s does not exist or cannot be found.\r\n", self._data_file)
            self._output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
            print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
