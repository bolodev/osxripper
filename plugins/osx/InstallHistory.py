""" Module to parse InstallHistory plist """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class InstallHistory(Plugin):
    """
    Plugin to list installed software from /Library/Receipts/InstallHistory.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Install History")
        self.set_description("Parse data from /Library/Receipts/InstallHistory.plist")
        self.set_data_file("InstallHistory.plist")
        self.set_output_file("InstallHistory.txt")
        self.set_type("plist")

    def parse(self):
        """
        Parse /Library/Receipts/InstallHistory.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Receipts", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))
            if os.path.isfile(plist_file):
                with open(plist_file, "rb") as plist_to_load:
                    plist = plistlib.load(plist_to_load)
                plist_to_load.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", plist_file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                parse_os = Parse01(output_file, plist)
                parse_os.parse()
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                parse_os = Parse02(output_file, plist)
                parse_os.parse()
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()

class Parse01():
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
            for item in self._data_file:
                if "displayName" in item:
                    self._output_file.write("Display Name       : {0}\r\n".format(item["displayName"]))
                if "displayVersion" in item:
                    self._output_file.write("Display Version    : {0}\r\n".format(item["displayVersion"]))
                if "date" in item:
                    self._output_file.write("Date               : {0}\r\n".format(item["date"]))
                if "processName" in item:
                    self._output_file.write("Process Name       : {0}\r\n".format(item["processName"]))
                if "packageIdentifiers" in item:
                    self._output_file.write("Package Identifiers:\r\n")
                    for package_item in item["packageIdentifiers"]:
                        self._output_file.write("\t{0}\r\n".format(package_item))
                self._output_file.write("\r\n")
        except KeyError:
            pass

class Parse02():
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
            for item in self._data_file:
                if "contentType" in item:
                    self._output_file.write("Content Type       : {0}\r\n".format(item["contentType"]))
                if "displayName" in item:
                    self._output_file.write("Display Name       : {0}\r\n".format(item["displayName"]))
                if "displayVersion" in item:
                    self._output_file.write("Display Version    : {0}\r\n".format(item["displayVersion"]))
                if "date" in item:
                    self._output_file.write("Date               : {0}\r\n".format(item["date"]))
                if "processName" in item:
                    self._output_file.write("Process Name       : {0}\r\n".format(item["processName"]))
                if "packageIdentifiers" in item:
                    self._output_file.write("Package Identifiers:\r\n")
                    for package_item in item["packageIdentifiers"]:
                        self._output_file.write("\t{0}\r\n".format(package_item))
                self._output_file.write("\r\n")
        except KeyError:
            pass
