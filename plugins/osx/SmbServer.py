""" Module to get host shares history """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SmbServer(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/com.apple.smb.server.plist
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("SMB Server")
        self.set_description("Parse data from com.apple.smb.server.plist")
        self.set_type("plist")
        self.set_data_file("com.apple.smb.server.plist")
        self.set_output_file("Networking.txt")

    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/com.apple.smb.server.plist
        """
        with codecs.open(os.path.join(self.get_output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as plist_to_load:
                            plist = plistlib.load(plist_to_load)
                        if "ServerDescription" in plist:
                            output_file.write("Server Description  : {0}\r\n".format(plist["ServerDescription"]))
                        if "NetBIOSName" in plist:
                            output_file.write("Net BIOS Name       : {0}\r\n".format(plist["NetBIOSName"]))
                        if "DOSCodePage" in plist:
                            output_file.write("DOS Code Page       : {0}\r\n".format(plist["DOSCodePage"]))
                        if "LocalKerberosRealm" in plist:
                            output_file.write("Local Kerberos Realm: {0}\r\n".format(plist["LocalKerberosRealm"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", plist_file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
