
""" Module to retrieve information from /private/etc/authorization """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemAuthPlist(Plugin):
    """
    Plugin to retrieve information from /private/etc/authorization
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("System Authorization Plist")
        self.set_description("Get the OSX version from /private/etc/authorization")
        self.set_data_file("authorization")
        self.set_output_file("System_Auth.txt")
        self.set_type("plist")

    def parse(self):
        """
        Parse authorization plist and write version information to file
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "private", "etc", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))
            if self._os_version in ["mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as plist_to_load:
                        plist = plistlib.load(plist_to_load)
                    parse_os = ParseVers108106(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", plist_file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))

            elif self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan",
                                      "yosemite", "mavericks"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()

class ParseVers108106():
    """
    Convenience class for parsing macOS data
    """
    def __init__(self, output_file, data_file):
        self._output_file = output_file
        self._data_file = data_file

    def parse(self):
        """
        Parse data
        """
        try:
            if "rights" in self._data_file:
                self._output_file.write("Rights\r\n")
                for right_item in self._data_file["rights"]:
                    self._output_file.write("\tRight: {0}\r\n".format(right_item))
                    if "class" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tClass            : {0}\r\n".format(self._data_file["rights"][right_item]["class"]))
                    if "comment" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tComment          : {0}\r\n".format(self._data_file["rights"][right_item]["comment"]))
                    if "k-of-n" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tK-of-N           : {0}\r\n".format(self._data_file["rights"][right_item]["k-of-n"]))
                    if "rule" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tRule             : {0}\r\n".format(self._data_file["rights"][right_item]["rule"]))
                    if "timeout" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tTimeout          : {0}\r\n".format(self._data_file["rights"][right_item]["timeout"]))
                    if "allow-root" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tAllow Root       : {0}\r\n".format(self._data_file["rights"][right_item]["allow-root"]))
                    if "shared" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tShared           : {0}\r\n".format(self._data_file["rights"][right_item]["shared"]))
                    if "tries" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tTries            : {0}\r\n".format(self._data_file["rights"][right_item]["tries"]))
                    if "session-owner" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tSession Owner    : {0}\r\n".format(self._data_file["rights"][right_item]["session-owner"]))
                    if "authenticate-user" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tAuthenticate User: {0}\r\n".format(self._data_file["rights"][right_item]["authenticate-user"]))
                    if "group" in self._data_file["rights"][right_item]:
                        self._output_file.write("\t\tGroup            : {0}\r\n".format(self._data_file["rights"][right_item]["group"]))
                    self._output_file.write("\r\n")
        except KeyError:
            pass
