from riplib.Plugin import Plugin
import logging
import os
import plistlib

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class OSXVersion(Plugin):
    """
    Plugin to retrieve OSX version
    """
    def __init__(self):
        """
        Initialise the class.
        :type self: object
        """
        super().__init__()
        self._name = "OSX Version"
        self._description = "Get the OSX version from /System/Library/CoreServices/SystemVersion.plist"
        self._data_file = "SystemVersion.plist"
        self._type = "plist"

    def parse(self):
        """
        Parse SystemVersion.plist and return ProductVersion
        """
        plist = os.path.join(self._input_dir, "System", "Library", "CoreServices", self._data_file)
        if os.path.isfile(plist):
            try:
                with open(plist, "rb") as pl:
                    plist_loaded = plistlib.load(pl)
                if "ProductVersion" in plist_loaded:
                    return "{0}".format(plist_loaded["ProductVersion"])
            except KeyError:
                pass
        else:
            logging.warning("{0} does not exist".format(self._data_file))
            return "[WARNING] {0} does not exist".format(self._data_file)
