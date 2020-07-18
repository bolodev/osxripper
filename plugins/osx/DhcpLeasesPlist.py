""" Module to parse DHCP leases """
import binascii
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class DhcpLeasesPlist(Plugin):
    """
    Plugin to parse DHCP plists in /private/var/db/dhcpclient/leases/en
    """

    def __init__(self):
        """
        Initialise plugins
        """
        super().__init__()
        self._name = "DHCP Leases"
        self._description = "Parse DHCP Lease plists from /private/var/db/dhcpclient/leases/en"
        self._data_file = ""  # Empty as parsing multiple files
        self._output_file = "Networking.txt"
        self._type = "plist"

    def parse(self):
        """
        Parse DHCP plists in /private/var/db/dhcpclient/leases/en
        """
        working_dir = os.path.join(self._input_dir, "private", "var", "db", "dhcpclient", "leases")
        if os.path.isdir(working_dir):
            file_listing = os.listdir(working_dir)
            for file_name in file_listing:
                self.__parse_plist(os.path.join(working_dir, file_name))
        else:
            with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
                output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(working_dir))
                output_file.write("="*40 + " " + "\r\n\r\n")
            output_file.close()
            logging.warning("File: %s does not exist or cannot be found.", working_dir)
            print("[WARNING] File: {0} does not exist or cannot be found.".format(working_dir))

    def __parse_plist(self, file):
        """
        Parse the plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            with open(file, "rb") as plist_to_load:
                plist = plistlib.load(plist_to_load)
            plist_to_load.close()
            # Investigate packet data bytes for useful information
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
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
            if "IPAddress" in self._data_file:
                self._output_file.write("IP Address             : {0}\r\n".format(self._data_file["IPAddress"]))
            if "LeaseLength" in self._data_file:
                self._output_file.write("Lease Length           : {0}\r\n".format(self._data_file["LeaseLength"]))
            if "LeaseStartDate" in self._data_file:
                self._output_file.write("Lease Start Date       : {0}\r\n".format(self._data_file["LeaseStartDate"]))
            if "RouterHardwareAddress" in self._data_file:
                # BASE64 is MAC in raw
                self._output_file.write("Router Hardware Address: {0}\r\n".format(binascii.hexlify(self._data_file["RouterHardwareAddress"])))
            if "RouterIPAddress" in self._data_file:
                self._output_file.write("Router IP Address      : {0}\r\n".format(self._data_file["RouterIPAddress"]))
            if "SSID" in self._data_file:
                self._output_file.write("Router SSID            : {0}\r\n".format(self._data_file["SSID"]))
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
            if "IPAddress" in self._data_file:
                self._output_file.write("IP Address: {0}\r\n".format(self._data_file["IPAddress"]))
            if "LeaseLength" in self._data_file:
                self._output_file.write("Lease Length: {0}\r\n".format(self._data_file["LeaseLength"]))
            if "LeaseStartDate" in self._data_file:
                self._output_file.write("Lease Start Date: {0}\r\n".format(self._data_file["LeaseStartDate"]))
            if "RouterHardwareAddress" in self._data_file:
                self._output_file.write("Router Hardware Address: {0}\r\n".format(binascii.hexlify(self._data_file["RouterHardwareAddress"])))
            if "RouterIPAddress" in self._data_file:
                self._output_file.write("Router IP Address: {0}\r\n".format(self._data_file["RouterIPAddress"]))
        except KeyError:
            pass
