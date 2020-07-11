from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class GKRearmTimer(Plugin):
    """
    Plugin to parse /private/var/db/.GKRearmTimer plist
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "GK Rearm Timer"
        self._description = "Parse data from /private/var/db/.GKRearmTimer plist"
        self._data_file = ".GKRearmTimer"
        self._output_file = "System.txt"
        self._type = "plist"
        
    def parse(self):
        """
        Parse /private/var/db/.GKRearmTimer plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "private", "var", "db", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(plist_file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        if "event" in plist:
                            of.write("Event    : {0}\r\n".format(plist["event"]))
                        if "timestamp" in plist:
                            of.write("Timestamp: {0}\r\n".format(plist["timestamp"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            elif self._os_version in ["mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
