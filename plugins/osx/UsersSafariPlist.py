""" Module to parse Safari plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersSafariPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.Safari.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Safari Plist")
        self.set_description("Parse information from /Users/username/Library/Preferences/com.apple.Safari.plist")
        self.set_data_file("com.apple.Safari.plist")
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
        Parse /Users/username/Library/Preferences/com.apple.finder.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["big_sur", "catalina", "mojave"]:
            # if self._os_version in ["catalina", "mojave"]:
                # Does not exist
                pass
            elif self._os_version in ["high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    parse_os = Parse01(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version in ["mavericks", "mountain_lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    parse_os = Parse02(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version in ["lion", "snow_leopard"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    parse_os = Parse03(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
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
            if "RecentWebSearches" in self._data_file:
                self._output_file.write("Recent Web Searches:\r\n")
                for rws in self._data_file["RecentWebSearches"]:
                    self._output_file.write("\tSearch String: {0}\r\n".format(rws["SearchString"]))
                    self._output_file.write("\tSearch Date  : {0}\r\n\r\n".format(rws["Date"]))

            if "LocalFileRestrictionsEnabled" in self._data_file:
                self._output_file.write("Local File Restrictions Enabled: {0}\r\n".format(self._data_file["LocalFileRestrictionsEnabled"]))
            if "CachedBookmarksFileSize" in self._data_file:
                self._output_file.write("Cached Bookmarks File Size     : {0}\r\n".format(self._data_file["CachedBookmarksFileSize"]))
            if "ExtensionsEnabled" in self._data_file:
                self._output_file.write("Extensions Enabled             : {0}\r\n".format(self._data_file["ExtensionsEnabled"]))
            if "DownloadsPath" in self._data_file:
                self._output_file.write("Downloads Path                 : {0}\r\n".format(self._data_file["DownloadsPath"]))
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
            if "RecentSearchStrings" in self._data_file:
                self._output_file.write("Recent Search Strings:\r\n")
                for search_string in self._data_file["RecentSearchStrings"]:
                    self._output_file.write("\t{0}\r\n".format(search_string))
                self._output_file.write("\r\n")
            if "DownloadsPath" in self._data_file:
                self._output_file.write("Downloads Path                 : {0}\r\n".format(self._data_file["DownloadsPath"]))
            if "LocalFileRestrictionsEnabled" in self._data_file:
                self._output_file.write("Local File Restrictions Enabled: {0}\r\n".format(self._data_file["LocalFileRestrictionsEnabled"]))
            if "CachedBookmarksFileSize" in self._data_file:
                self._output_file.write("Cached Bookmarks File Size     : {0}\r\n".format(self._data_file["CachedBookmarksFileSize"]))
        except KeyError:
            pass

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
        try:
            if "RecentSearchStrings" in self._data_file:
                self._output_file.write("Recent Search Strings:\r\n")
                for search_string in self._data_file["RecentSearchStrings"]:
                    self._output_file.write("\t{0}\r\n".format(search_string))
                self._output_file.write("\r\n")
            if "DownloadsPath" in self._data_file:
                self._output_file.write("Downloads Path                 : {0}\r\n".format(self._data_file["DownloadsPath"]))
            if "CachedBookmarksFileSize" in self._data_file:
                self._output_file.write("Cached Bookmarks File Size     : {0}\r\n".format(self._data_file["CachedBookmarksFileSize"]))
        except KeyError:
            pass
