from riplib.plugin import Plugin
import codecs
import logging
import os
import riplib.ccl_bplist

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersFinderPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.finder.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Mounted Volumes"
        self._description = "Parse information from /Users/username/Library/Preferences/com.apple.finder.plist"
        self._data_file = "com.apple.finder.plist"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
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
                        logging.warning("{0} does not exist.".format(plist))
                        print("[WARNING] {0} does not exist.".format(plist))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))
            
    def __parse_bplist(self, file, username):
        """
        Parse /Users/username/Library/Preferences/com.apple.finder.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = riplib.ccl_bplist.load(bplist)
                    try:
                        if "FXDesktopVolumePositions" in pl: 
                            for key in pl["FXDesktopVolumePositions"].keys():
                                of.write("Volume     : {0}\r\n".format(key))
                        of.write("\r\n")
                        if "FXConnectToLastURL" in pl:
                            of.write("Connect to Last URL: {0}\r\n".format(pl["FXConnectToLastURL"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            
            elif self._os_version in ["lion", "snow_leopard"]:
                #  This needs double checking, none of the DVD, or DMGs mounted are recorded...
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = riplib.ccl_bplist.load(bplist)
                    try:
                        if "FXConnectToLastURL" in pl:
                            of.write("Connect to Last URL: {0}\r\n".format(pl["FXConnectToLastURL"]))
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
