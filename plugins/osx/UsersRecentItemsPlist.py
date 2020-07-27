""" Module to extract information from recentitems plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersRecentItemsPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.recentitems.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Recent Items")
        self.set_description("Parse information from /Users/username/Library/Preferences/com.apple.recentitems.plist")
        self.set_data_file("com.apple.recentitems.plist")
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
                    # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra"]:
                    if self._os_version in ["catalina", "mojave", "high_sierra"]:
                        # File does not exist in these versions
                        # return
                        pass
                    elif self._os_version in ["sierra", "el_capitan"]:
                        self._data_file = os.path.join(users_path, username, "Library", "Application Support", "com.apple.sharedfilelist", "com.apple.LSSharedFileList.RecentHosts.sfl")
                        plist = self._data_file
                    else:
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
        Parse /Users/username/Library/Preferences/com.apple.recentitems.plist or in El Capitan
        /Users/<username>/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.RecentHosts.sfl
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if self._os_version in ["high_sierra", "sierra", "el_capitan"]:
                if os.path.isfile(file):
                    output_file.write("Source File: {0}\r\n\r\n".format(file))
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    parse_os = Parse01(output_file, plist)
                    parse_os.parse()
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(file):
                    output_file.write("Source File: {0}\r\n\r\n".format(file))
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    parse_os = Parse02(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
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
        try:
            if "$objects" in self._data_file:
                for objects in self._data_file["$objects"]:
                    if isinstance(objects, str):
                        if "smb://" in objects:
                            self._output_file.write("Name     : {0}\r\n".format(objects))
        except KeyError:
            pass

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
        try:
            if "Hosts" in self._data_file:
                custom_list_items = self._data_file["Hosts"]["CustomListItems"]
                for custom_list_item in custom_list_items:
                    self._output_file.write("Name     : {0}\r\n".format(custom_list_item["Name"]))
                    self._output_file.write("URL      : {0}\r\n".format(custom_list_item["URL"]))
                    self._output_file.write("\r\n")
            if "RecentDocuments" in self._data_file:
                pass
            if "RecentApplications" in self._data_file:
                pass
        except KeyError:
            pass
