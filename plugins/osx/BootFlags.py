from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class BootFlags(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/com.apple.Boot.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Boot Flags"
        self._description = "Parse data from com.apple.Boot.plist"
        self._data_file = "com.apple.Boot.plist"
        self._output_file = "System.txt"
        self._type = "plist"
    
    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/com.apple.Boot.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks",
            #                         "mountain_lion", "lion", "snow_leopard"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite", "mavericks",
                                    "mountain_lion", "lion", "snow_leopard"]:
                plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration",
                                          self._data_file)
                of.write("Source File: {0}\r\n\r\n".format(plist_file))
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                        try:
                            if "Kernel Flags" in plist:
                                of.write("Kernel Flags: {0}\r\n".format(plist["Kernel Flags"]))
                            of.write("\r\n")
                        except KeyError:
                            pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
