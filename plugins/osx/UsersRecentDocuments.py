""" Module to extract informatio from Users RecentDocuments """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersRecentDocuments(Plugin):
    """
    Parse information from
    /Users/username/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.RecentDocuments.sfl
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Recent Hosts Shared File List")
        self.set_description("Parse information from /Users/username/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.RecentDocuments.sfl")
        self.set_data_file("com.apple.LSSharedFileList.RecentDocuments.sfl")
        self.set_output_file("_RecentDocuments.txt")
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
                    plist = os.path.join(users_path, username, "Library", "Application Support", "com.apple.sharedfilelist", self._data_file)
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
        Parse com.apple.LSSharedFileList.RecentDocuments.sfl
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra"]:
                # Uses .sfl2 files
                pass
            elif self._os_version in ["sierra", "el_capitan"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                else:
                    logging.info("This version of OSX is not supported by this plugin.")
                    print("[INFO] This version of OSX is not supported by this plugin.")
                    output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
                    output_file.close()
                    return
                try:
                    if "$objects" in plist:
                        for item in plist["$objects"]:
                            # if type(item) == str:
                            if isinstance(item, str):
                                if "file://" in item:
                                    output_file.write("\t{0}\r\n".format(item))
                    output_file.write("\r\n")
                except KeyError:
                    pass

            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.warning("File: %s does not exist or cannot be found.", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
