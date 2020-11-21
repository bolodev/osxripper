""" Module to parse message-tracer plist """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class WifiMessageTracer(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/com.apple.wifi.message-tracer.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Wifi Message Tracer")
        self.set_description("Parse data from com.apple.wifi.message-tracer.plist")
        self.set_data_file("com.apple.wifi.message-tracer.plist")
        self.set_output_file("Networking.txt")
        self.set_type("plist")

    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/com.apple.wifi.message-tracer.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as plist_to_load:
                        plist = plistlib.load(plist_to_load)
                    parse_os = Parse01(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", plist_file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            elif self._os_version == "mavericks":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as plist_to_load:
                        plist = plistlib.load(plist_to_load)
                    parse_os = Parse02(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", plist_file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            elif self._os_version in ["mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
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
            if "AssociationSSIDMap" in self._data_file:
                self._output_file.write("AssociationSSIDMap:\r\n")
                for asm_key in self._data_file["AssociationSSIDMap"]:
                    self._output_file.write("\t{0}: {1}\r\n".format(asm_key, self._data_file["AssociationSSIDMap"][asm_key]))
                self._output_file.write("\r\n")
            if "InternalAssociationSSIDMap" in self._data_file:
                self._output_file.write("InternalAssociationSSIDMap:\r\n")
                for iasm_key in self._data_file["InternalAssociationSSIDMap"]:
                    self._output_file.write("\t{0}: {1}\r\n".format(iasm_key, self._data_file["InternalAssociationSSIDMap"][iasm_key]))
                self._output_file.write("\r\n")
            if "LastSubmissionTimestamp" in self._data_file:
                self._output_file.write("Last Submission Timestamp: {0}\r\n".format(self._data_file["LastSubmissionTimestamp"]))
                self._output_file.write("\r\n")
            if "PendingList" in self._data_file:
                self._output_file.write("Pending List:\r\n")
                pending_list = self._data_file["PendingList"]  # list
                for pending_list_item in pending_list:
                    for item_key in pending_list_item:
                        if isinstance(pending_list_item[item_key], str):
                            self._output_file.write("\t{0}: {1}\r\n".format(item_key, pending_list_item[item_key]))
                        else:
                            self._output_file.write("\t{0}: {1}\r\n".format(item_key, pending_list_item[item_key]))
                    self._output_file.write("\r\n")
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
            if "LastSubmissionTimestamp" in self._data_file:
                self._output_file.write("Last Submission Timestamp: {0}\r\n".format(self._data_file["LastSubmissionTimestamp"]))
                self._output_file.write("\r\n")
            if "PendingList" in self._data_file:
                self._output_file.write("Pending List:\r\n")
                pending_list = self._data_file["PendingList"]  # list
                for pending_list_item in pending_list:
                    for item_key in pending_list_item:
                        if isinstance(pending_list_item[item_key], str):
                            self._output_file.write("\t{0}: {1}\r\n".format(item_key, pending_list_item[item_key]))
                        else:
                            self._output_file.write("\t{0}: {1}\r\n".format(item_key, pending_list_item[item_key]))
                    self._output_file.write("\r\n")
            self._output_file.write("\r\n")
        except KeyError:
            pass
