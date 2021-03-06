""" Module to parse dock plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersDockPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.dock.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Dock Plist")
        self.set_description("Parse information from /Users/username/Library/Preferences/com.apple.dock.plist")
        self.set_data_file("com.apple.dock.plist")
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
        Parse /Users/username/Library/Preferences/com.apple.dock.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Dock.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                plist = riplib.ccl_bplist.load(bplist)
                bplist.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
                output_file.close()
                return

            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks",
                                    "mountain_lion", "lion", "snow_leopard"]:
                try:
                    if "trash-full" in plist:
                        output_file.write("Trash Full: {0}\r\n\r\n".format(plist["trash-full"]))
                    if "persistent-apps" in plist:
                        output_file.write("Applications:\r\n")
                        persist_apps = plist["persistent-apps"]
                        for persist_app in persist_apps:
                            if "file-data" in persist_app["tile-data"]:
                                output_file.write("\t{0}\r\n".format(persist_app["tile-data"]["file-data"]["_CFURLString"]))
                        output_file.write("\r\n")
                    if "persistent-others" in plist:
                        persist_others = plist["persistent-others"]
                        output_file.write("Other:\r\n")
                        for persist_other in persist_others:
                            if "file-data" in persist_other["tile-data"]:
                                output_file.write("\t{0}\r\n".format(persist_other["tile-data"]["file-data"]["_CFURLString"]))
                        # pass
                    output_file.write("\r\n")
                except KeyError as _:
                    pass
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
