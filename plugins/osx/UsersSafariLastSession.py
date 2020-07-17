from riplib.plugin import Plugin
import codecs
import logging
import os
import riplib.ccl_bplist

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersSafariLastSession(Plugin):
    """
    Parse information from /Users/username/Library/Safari/LastSession.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Safari Last Session"
        self._description = "Parse information from /Users/username/Library/Safari/LastSession.plist"
        self._data_file = "LastSession.plist"
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
                    plist = os.path.join(users_path, username, "Library", "Safari", self._data_file)
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
        Parse /Users/username/Library/Safari/LastSession.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Last_Session.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "SessionWindows" in plist:
                            for session_window in plist["SessionWindows"]:
                                if "TabStates" in session_window:
                                    of.write("Tabs:\r\n")
                                    for tab_state in session_window["TabStates"]:
                                        if "TabURL" in tab_state:
                                            of.write("\tTab URL  : {0}\r\n".format(tab_state["TabURL"]))
                                        if "TabTitle" in tab_state:
                                            of.write("\tTab Title: {0}\r\n".format(tab_state["TabTitle"]))
                                        of.write("\r\n")
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "SessionWindows" in plist:
                            for session_window in plist["SessionWindows"]:
                                if "TabStates" in session_window:
                                    of.write("Tabs:\r\n")
                                    for tab_state in session_window["TabStates"]:
                                        if "BackForwardList" in tab_state:
                                            for back_forward_list in tab_state["BackForwardList"]:
                                                if "URL" in back_forward_list:
                                                    of.write("\tTab URL  : {0}\r\n".format(back_forward_list["URL"]))
                                                if "Title" in back_forward_list:
                                                    of.write("\tTab Title: {0}\r\n".format(back_forward_list["Title"]))
                                        of.write("\r\n")
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
