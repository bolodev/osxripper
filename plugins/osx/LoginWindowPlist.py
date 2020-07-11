from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.ccl_bplist

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class LoginWindowPlist(Plugin):
    """
    Plugin to parse /Library/Preferences/com.apple.loginwindow.plist
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Login Window"
        self._description = "Parse data from /Library/Preferences/com.apple.loginwindow.plist"
        self._data_file = "com.apple.loginwindow.plist"
        self._output_file = "LoginWindow.txt"
        self._type = "bplist"
        
    def parse(self):
        """
        Parse /Library/Preferences/com.apple.loginwindow.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(file):
                    try:
                        bplist = open(file, "rb")
                        pl = riplib.ccl_bplist.load(bplist)
                        if "lastUserName" in pl:
                            of.write("Last User       : {0}\r\n".format(pl["lastUserName"]))
                        if "lastUser" in pl:
                            of.write("Last User Action: {0}\r\n".format(pl["lastUser"]))
                        bplist.close()
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
