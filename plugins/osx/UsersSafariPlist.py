from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.ccl_bplist

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
        self._name = "User Safari Plist"
        self._description = "Parse information from /Users/username/Library/Preferences/com.apple.Safari.plist"
        self._data_file = "com.apple.Safari.plist"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
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
                        logging.warning("{0} does not exist.".format(plist))
                        print("[WARNING] {0} does not exist.".format(plist))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))
            
    def __parse_bplist(self, file, username):
        """
        Parse /Users/username/Library/Preferences/com.apple.finder.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave"]:
            if self._os_version in ["catalina", "mojave"]:
                # Does not exist
                return
            elif self._os_version in ["high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "RecentWebSearches" in plist:
                            of.write("Recent Web Searches:\r\n")
                            for rws in plist["RecentWebSearches"]:
                                of.write("\tSearch String: {0}\r\n".format(rws["SearchString"]))
                                of.write("\tSearch Date  : {0}\r\n\r\n".format(rws["Date"]))
                                
                        if "LocalFileRestrictionsEnabled" in plist:
                            of.write("Local File Restrictions Enabled: {0}\r\n"
                                     .format(plist["LocalFileRestrictionsEnabled"]))
                        if "CachedBookmarksFileSize" in plist:
                            of.write("Cached Bookmarks File Size     : {0}\r\n".format(plist["CachedBookmarksFileSize"]))
                        if "ExtensionsEnabled" in plist:
                            of.write("Extensions Enabled             : {0}\r\n".format(plist["ExtensionsEnabled"]))
                        if "DownloadsPath" in plist:
                            of.write("Downloads Path                 : {0}\r\n".format(plist["DownloadsPath"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version in ["mavericks", "mountain_lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "RecentSearchStrings" in plist:
                            of.write("Recent Search Strings:\r\n")
                            for search_string in plist["RecentSearchStrings"]:
                                of.write("\t{0}\r\n".format(search_string))
                            of.write("\r\n")
                        if "DownloadsPath" in plist:
                            of.write("Downloads Path                 : {0}\r\n".format(plist["DownloadsPath"]))
                        if "LocalFileRestrictionsEnabled" in plist:
                            of.write("Local File Restrictions Enabled: {0}\r\n"
                                     .format(plist["LocalFileRestrictionsEnabled"]))
                        if "CachedBookmarksFileSize" in plist:
                            of.write("Cached Bookmarks File Size     : {0}\r\n"
                                     .format(plist["CachedBookmarksFileSize"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version in ["lion", "snow_leopard"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "RecentSearchStrings" in plist:
                            of.write("Recent Search Strings:\r\n")
                            for search_string in plist["RecentSearchStrings"]:
                                of.write("\t{0}\r\n".format(search_string))
                            of.write("\r\n")
                        if "DownloadsPath" in plist:
                            of.write("Downloads Path                 : {0}\r\n".format(plist["DownloadsPath"]))
                        if "CachedBookmarksFileSize" in plist:
                            of.write("Cached Bookmarks File Size     : {0}\r\n"
                                     .format(plist["CachedBookmarksFileSize"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
