from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemVersionPlist(Plugin):
    """
    Plugin to retrieve OSX version information
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Version"
        self._description = "Get the OSX version from /System/Library/CoreServices/SystemVersion.plist"
        self._data_file = "SystemVersion.plist"
        self._output_file = "SystemVersion.txt"
        self._type = "plist"
        
    def parse(self): 
        """
        Parse SystemVersion.plist and write version information to file
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "System", "Library", "CoreServices", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(plist_file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan",
                                    "yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        if "ProductBuildVersion" in plist:
                            of.write("Product Build Version       : {0}\r\n".format(plist["ProductBuildVersion"]))
                        if "ProductCopyright" in plist:
                            of.write("Product Copyright           : {0}\r\n".format(plist["ProductCopyright"]))
                        if "ProductName" in plist:
                            of.write("Product Name                : {0}\r\n".format(plist["ProductName"]))
                        if "ProductUserVisibleVersion" in plist:
                            of.write("Product User Visible Version: {0}\r\n".format(plist["ProductUserVisibleVersion"]))
                        if "ProductVersion" in plist:
                            of.write("Product Version             : {0}\r\n".format(plist["ProductVersion"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
