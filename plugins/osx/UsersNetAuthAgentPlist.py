""" Module to parse information form NetAuthAgent plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersNetAuthAgentPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.NetAuthAgent.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Mounted Shares")
        self.set_description("Parse information from /Users/username/Library/Preferences/com.apple.NetAuthAgent.plist")
        self.set_data_file("com.apple.NetAuthAgent.plist")
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
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Shares.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                else:
                    logging.warning("File: %s does not exist or cannot be found.", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
                    return
                try:
                    if "PreviouslySelectedShares" in plist:
                        for key in plist["PreviouslySelectedShares"].keys():
                            output_file.write("Host: {0}\r\n".format(key))
                            for directory in plist["PreviouslySelectedShares"][key]:
                                output_file.write("\tShared Directory: {0}\r\n".format(directory))
                            output_file.write("\r\n")
                    output_file.write("\r\n")
                except KeyError:
                    pass
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.warning("File: %s does not exist on this version of OSX.", file)
                output_file.write("[WARNING] File: {0} does not exist on this version of OSX.\r\n".format(file))
                print("[WARNING] File: {0} does not exist on this version of OSX.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
