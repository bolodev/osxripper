from riplib.plugin import Plugin
import codecs
import logging
import os
import plistlib

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
        self._name = "System Authorization Plist"
        self._description = "Get the OSX version from /private/etc/authorization"
        self._data_file = "authorization"
        self._output_file = "System_Auth.txt"
        self._type = "plist"
        
    def parse(self): 
        """
        Parse authorization plist and write version information to file
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "private", "etc", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(plist_file))
            if self._os_version in ["mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        if "rights" in plist:
                            of.write("Rights\r\n")
                            for right_item in plist["rights"]:
                                of.write("\tRight: {0}\r\n".format(right_item))
                                if "class" in plist["rights"][right_item]:
                                    of.write("\t\tClass            : {0}\r\n"
                                             .format(plist["rights"][right_item]["class"]))
                                if "comment" in plist["rights"][right_item]:
                                    of.write("\t\tComment          : {0}\r\n"
                                             .format(plist["rights"][right_item]["comment"]))
                                if "k-of-n" in plist["rights"][right_item]:
                                    of.write("\t\tK-of-N           : {0}\r\n"
                                             .format(plist["rights"][right_item]["k-of-n"]))
                                if "rule" in plist["rights"][right_item]:
                                    of.write("\t\tRule             : {0}\r\n"
                                             .format(plist["rights"][right_item]["rule"]))
                                if "timeout" in plist["rights"][right_item]:
                                    of.write("\t\tTimeout          : {0}\r\n"
                                             .format(plist["rights"][right_item]["timeout"]))
                                if "allow-root" in plist["rights"][right_item]:
                                    of.write("\t\tAllow Root       : {0}\r\n"
                                             .format(plist["rights"][right_item]["allow-root"]))
                                if "shared" in plist["rights"][right_item]:
                                    of.write("\t\tShared           : {0}\r\n"
                                             .format(plist["rights"][right_item]["shared"]))
                                if "tries" in plist["rights"][right_item]:
                                    of.write("\t\tTries            : {0}\r\n"
                                             .format(plist["rights"][right_item]["tries"]))
                                if "session-owner" in plist["rights"][right_item]:
                                    of.write("\t\tSession Owner    : {0}\r\n"
                                             .format(plist["rights"][right_item]["session-owner"]))
                                if "authenticate-user" in plist["rights"][right_item]:
                                    of.write("\t\tAuthenticate User: {0}\r\n"
                                             .format(plist["rights"][right_item]["authenticate-user"]))
                                if "group" in plist["rights"][right_item]:
                                    of.write("\t\tGroup            : {0}\r\n"
                                             .format(plist["rights"][right_item]["group"]))
                                of.write("\r\n")
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))

            # elif self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan",
            elif self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan",
                                      "yosemite", "mavericks"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
