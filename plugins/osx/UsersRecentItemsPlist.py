from riplib.plugin import Plugin
import codecs
import logging
import os
import riplib.ccl_bplist

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
        self._name = "User Recent Items"
        self._description = "Parse information from /Users/username/Library/Preferences/com.apple.recentitems.plist"
        self._data_file = "com.apple.recentitems.plist"
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
                    # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra"]:
                    if self._os_version in ["catalina", "mojave", "high_sierra"]:
                        # File does not exist in these versions
                        return
                    elif self._os_version in ["sierra", "el_capitan"]:
                        self._data_file = os.path.join(users_path, username, "Library", "Application Support",
                                                       "com.apple.sharedfilelist",
                                                       "com.apple.LSSharedFileList.RecentHosts.sfl")
                        plist = self._data_file
                    else:
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
        Parse /Users/username/Library/Preferences/com.apple.recentitems.plist or in El Capitan
        /Users/<username>/Library/Application Support/
        com.apple.sharedfilelist/com.apple.LSSharedFileList.RecentHosts.sfl
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if self._os_version in ["high_sierra", "sierra", "el_capitan"]:
                if os.path.isfile(file):
                    of.write("Source File: {0}\r\n\r\n".format(file))
                    bplist = open(file, "rb")
                    pl = riplib.ccl_bplist.load(bplist)
                    try:
                        if "$objects" in pl:
                            for objects in pl["$objects"]:
                                if isinstance(objects, str):
                                    if "smb://" in objects:
                                        of.write("Name     : {0}\r\n".format(objects))
                    except KeyError:
                        pass
                    bplist.close()
                pass
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(file):
                    of.write("Source File: {0}\r\n\r\n".format(file))
                    bplist = open(file, "rb")
                    pl = riplib.ccl_bplist.load(bplist)
                    try:
                        if "Hosts" in pl:
                            custom_list_items = pl["Hosts"]["CustomListItems"]
                            for custom_list_item in custom_list_items:
                                of.write("Name     : {0}\r\n".format(custom_list_item["Name"]))
                                of.write("URL      : {0}\r\n".format(custom_list_item["URL"]))
                                of.write("\r\n")
                        if "RecentDocuments" in pl:
                            pass
                        if "RecentApplications" in pl:
                            pass
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
