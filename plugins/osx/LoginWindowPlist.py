""" Module to parse loginwindow.plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


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
        self.set_name("Login Window")
        self.set_description("Parse data from /Library/Preferences/com.apple.loginwindow.plist")
        self.set_data_file("com.apple.loginwindow.plist")
        self.set_output_file("LoginWindow.txt")
        self.set_type("bplist")

    def parse(self):
        """
        Parse /Library/Preferences/com.apple.loginwindow.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(file):
                    try:
                        bplist = open(file, "rb")
                        plist = riplib.ccl_bplist.load(bplist)
                        if "lastUserName" in plist:
                            output_file.write("Last User       : {0}\r\n".format(plist["lastUserName"]))
                        if "lastUser" in plist:
                            output_file.write("Last User Action: {0}\r\n".format(plist["lastUser"]))
                        bplist.close()
                    except KeyError:
                        pass
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
