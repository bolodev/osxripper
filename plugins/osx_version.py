""" Module for the OSXVersion plugin """
import logging
import os
import plistlib
from riplib.plugin import Plugin

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
        self._description = "Get the OSX version from" \
                            "/System/Library/CoreServices/SystemVersion.plist"
        self._data_file = "SystemVersion.plist"
        self._type = "plist"

    def parse(self):
        """
        Parse SystemVersion.plist and return ProductVersion
        """
        plist_file = os.path.join(self._input_dir,
                                  "System", "Library", "CoreServices", self._data_file)
        if not os.path.isfile(plist_file):
            logging.warning("%s does not exist", self._data_file)
            print("[WARNING] {0} does not exist".format(self._data_file))
            return "NONE"

        with open(plist_file, "rb") as plist:
            plist_loaded = plistlib.load(plist)
        plist.close()

        try:
            if "ProductVersion" in plist_loaded:
                product_version = "{0}".format(plist_loaded["ProductVersion"])
                return product_version
        except KeyError:
            logging.warning("[ERROR] ProductVersion key does not exist in %s", self._data_file)
            return "NONE"
