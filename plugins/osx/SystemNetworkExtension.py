""" Module to parse Airport data """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemNetworkExtension(Plugin):
    """
    Plugin to parse /System/Library/Frameworks/NetworkExtension.framework/Resources/Info.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("System Network Extension")
        self.set_description("Parse data from Info.plist to ascertain Apple Firewall exclusions")
        self.set_data_file("Info.plist")
        self.set_output_file("Apple_Firewall.txt")
        self.set_type("plist")

    def parse(self):
        """
        Parse /System/Library/Frameworks/NetworkExtension.framework/Resources/Info.plist
        """
        with codecs.open(os.path.join(self.get_output_dir, self.get_output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self.get_name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self.get_input_dir, "System", "Library", "Frameworks", "NetworkExtension.framework", "Resources", self.get_data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))
            if os.path.isfile(plist_file):
                with open(plist_file, "rb") as plist_to_load:
                    plist = plistlib.load(plist_to_load)
                plist_to_load.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.", plist_file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
                output_file.close()
                return

            if self._os_version in ["big_sur", "catalina"]:
                output_file.write("Apple Firewall Trusted/Content Filter Exclusion Lists\r\n")
                output_file.write("{0}\r\n".format("="*10))
                try:
                    if "TrustedExecutables" in plist:
                        for trusted_item in plist["TrustedExecutables"]:
                            output_file.write("\t{0}\r\n".format(trusted_item))

                    output_file.write("\r\n")
                    output_file.write("{0}\r\n".format("="*10))
                    output_file.write("\r\n")

                    if "ContentFilterExclusionList" in plist:
                        for cfel_item in plist["ContentFilterExclusionList"]:
                            output_file.write("\t{0}\r\n".format(cfel_item))
                    output_file.write("\r\n")
                except KeyError as error:
                    print("[ERROR]: Key {0} does not exist".format(error))
            elif self._os_version in ["mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("[WARNING] Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
