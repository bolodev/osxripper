from riplib.Plugin import Plugin
import binascii
import codecs
import logging
import os
import plistlib

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
            for f in file_listing:
                self.__parse_plist(os.path.join(working_dir, f))
        else:
            with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(working_dir))
                of.write("="*40 + " " + "\r\n\r\n")
            of.close()
            logging.warning("File: {0} does not exist or cannot be found.".format(working_dir))
            print("[WARNING] File: {0} does not exist or cannot be found.".format(working_dir))
    
    def __parse_plist(self, file):
        """
        Parse the plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            # TODO investigate packet data bytes for useful information
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                try:
                    with open(file, "rb") as pl:
                        plist = plistlib.load(pl)
                    if "IPAddress" in plist:
                        of.write("IP Address             : {0}\r\n".format(plist["IPAddress"]))
                    if "LeaseLength" in plist:
                        of.write("Lease Length           : {0}\r\n".format(plist["LeaseLength"]))
                    if "LeaseStartDate" in plist:
                        of.write("Lease Start Date       : {0}\r\n".format(plist["LeaseStartDate"]))
                    if "RouterHardwareAddress" in plist:
                        # BASE64 is MAC in raw
                        of.write("Router Hardware Address: {0}\r\n"
                                 .format(binascii.hexlify(plist["RouterHardwareAddress"])))

                    if "RouterIPAddress" in plist:
                        of.write("Router IP Address      : {0}\r\n".format(plist["RouterIPAddress"]))
                    if "SSID" in plist:
                        of.write("Router SSID            : {0}\r\n".format(plist["SSID"]))
                except KeyError:
                    pass
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                try:
                    with open(file, "rb") as pl:
                        plist = plistlib.load(pl)
                    if "IPAddress" in plist:
                        of.write("IP Address: {0}\r\n".format(plist["IPAddress"]))
                    if "LeaseLength" in plist:
                        of.write("Lease Length: {0}\r\n".format(plist["LeaseLength"]))
                    if "LeaseStartDate" in plist:
                        of.write("Lease Start Date: {0}\r\n".format(plist["LeaseStartDate"]))
                    if "RouterHardwareAddress" in plist:
                        of.write("Router Hardware Address: {0}\r\n"
                                 .format(binascii.hexlify(plist["RouterHardwareAddress"])))
                    if "RouterIPAddress" in plist:
                        of.write("Router IP Address: {0}\r\n".format(plist["RouterIPAddress"]))
                except KeyError:
                    pass
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
