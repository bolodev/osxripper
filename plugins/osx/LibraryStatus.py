from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class LibraryStatus(Plugin):
    """
    Plugin to parse /.DocumentRevisions-V100/LibraryStatus
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Document Revisions Library Status"
        self._description = "Parse data from /.DocumentRevisions-V100/LibraryStatus"
        self._data_file = "LibraryStatus"
        self._output_file = "DocumentRevisions.txt"
        self._type = "plist"
    
    def parse(self):
        """
        Parse /.DocumentRevisions-V100/LibraryStatus
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            # if self._os_version in ["big_sur", "catalina"]:
            if self._os_version in ["catalina"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            elif self._os_version in ["mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                plist_file = os.path.join(self._input_dir, ".DocumentRevisions-V100", self._data_file)
                of.write("Source File: {0}\r\n\r\n".format(plist_file))
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "databaseStateIsTrustable" in plist:
                            of.write("Database State Is Trustable: {0}\r\n".format(plist["databaseStateIsTrustable"]))
                            
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
