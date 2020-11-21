""" Module to retrieve information from /private/var/db/com.apple.xpc.launchd/disabled.plist """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemLaunchdDisabled(Plugin):
    """
    Plugin to retrieve information from /private/var/db/com.apple.xpc.launchd/disabled.plist
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("System Launchd Disabled")
        self.set_description("Get the information from /private/var/db/com.apple.xpc.launchd/disabled.plist")
        self.set_data_file("disabled.plist")
        self.set_output_file("System_Launch.txt")
        self.set_type("plist")

    def parse(self):
        """
        Parse SystemVersion.plist and write version information to file
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "private", "var", "db", "com.apple.xpc.launchd", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as plist_to_load:
                            plist = plistlib.load(plist_to_load)
                        for launchd_item in plist:
                            output_file.write("{0}: {1}\r\n".format(launchd_item, plist[launchd_item]))
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
