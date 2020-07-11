from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.ccl_bplist

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersRecentApplications(Plugin):
    """
    Parse information from
    /Users/username/Library/Application Support/com.apple.sharedfilelist/
    com.apple.LSSharedFileList.RecentApplications.sfl
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Recent Hosts Shared File List"
        self._description = "Parse information from /Users/username/Library/" \
                            "Application Support/com.apple.sharedfilelist/" \
                            "com.apple.LSSharedFileList.RecentApplications.sfl"
        self._data_file = "com.apple.LSSharedFileList.RecentApplications.sfl"
        self._output_file = "_RecentApplications.txt"
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
                    plist = os.path\
                        .join(users_path, username, "Library", "Application Support",
                              "com.apple.sharedfilelist",  self._data_file)
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
        Parse com.apple.LSSharedFileList.RecentApplications.sfl
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + self._output_file), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra"]:
            if self._os_version in ["catalina", "mojave", "high_sierra"]:
                # Uses .sfl2 files
                pass
            elif self._os_version in ["sierra", "el_capitan"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "$objects" in plist:
                            for item in plist["$objects"]:
                                if type(item) == str:
                                    if "file://" in item:
                                        of.write("\t{0}\r\n".format(item))
                        of.write("\r\n")
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.info("This version of OSX is not supported by this plugin.")
                    print("[INFO] This version of OSX is not supported by this plugin.")
                    of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.warning("File: {0} does not exist or cannot be found.".format(file))
                of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
