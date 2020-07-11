from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.ccl_bplist

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
        self._name = "User Mozilla Firefox"
        self._description = "Parse information from /Users/username/Library/Preferences/org.mozilla.firefox.plist"
        self._data_file = "org.mozilla.firefox.plist"
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
        Parse /Users/username/Library/Preferences/org.mozilla.firefox.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Firefox.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                plist = riplib.ccl_bplist.load(bplist)
                try:
                    if "NSTreatUnknownArgumentsAsOpen" in plist:
                        of.write("Treat Unknown Arguments As Open: {0}\r\n\r\n"
                                 .format(plist["NSTreatUnknownArgumentsAsOpen"]))
                    if "NSNavLastRootDirectory" in plist:
                        of.write("Nav Last Root Directory        : {0}\r\n\r\n".format(plist["NSNavLastRootDirectory"]))
                    of.write("\r\n")
                except KeyError:
                    pass
                bplist.close()
            else:
                logging.warning("File: {0} does not exist or cannot be found.".format(file))
                of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            of.write("="*40 + "\r\n\r\n")
        of.close()
