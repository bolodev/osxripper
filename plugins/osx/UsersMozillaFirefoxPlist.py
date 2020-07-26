""" Module to parse Firefox plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersMozillaFirefoxPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/org.mozilla.firefox.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Mozilla Firefox")
        self.set_description("Parse information from /Users/username/Library/Preferences/org.mozilla.firefox.plist")
        self.set_data_file("org.mozilla.firefox.plist")
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
        Parse /Users/username/Library/Preferences/org.mozilla.firefox.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Firefox.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                plist = riplib.ccl_bplist.load(bplist)
                try:
                    if "NSTreatUnknownArgumentsAsOpen" in plist:
                        output_file.write("Treat Unknown Arguments As Open: {0}\r\n\r\n".format(plist["NSTreatUnknownArgumentsAsOpen"]))
                    if "NSNavLastRootDirectory" in plist:
                        output_file.write("Nav Last Root Directory        : {0}\r\n\r\n".format(plist["NSNavLastRootDirectory"]))
                    output_file.write("\r\n")
                except KeyError:
                    pass
                bplist.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
