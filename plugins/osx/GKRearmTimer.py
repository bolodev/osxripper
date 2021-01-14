""" Module to  parse .GKRearmTimer plist """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin


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
        self.set_name("GK Rearm Timer")
        self.set_description("Parse data from /private/var/db/.GKRearmTimer plist")
        self.set_data_file(".GKRearmTimer")
        self.set_output_file("System.txt")
        self.set_type("plist")

    def parse(self):
        """
        Parse /private/var/db/.GKRearmTimer plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "private", "var", "db", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as plist_to_load:
                            plist = plistlib.load(plist_to_load)
                        if "event" in plist:
                            output_file.write("Event    : {0}\r\n".format(plist["event"]))
                        if "timestamp" in plist:
                            output_file.write("Timestamp: {0}\r\n".format(plist["timestamp"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", plist_file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            elif self._os_version in ["mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
