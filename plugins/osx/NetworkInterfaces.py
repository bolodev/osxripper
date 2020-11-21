""" Module to parse /Library/Preferences/SystemConfiguration/NetworkInterfaces.plist """
import binascii
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class NetworkInterfaces(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/NetworkInterfaces.plist
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Network Interfaces"
        self._description = "Parse data from NetworkInterfaces.plist"
        self._data_file = "NetworkInterfaces.plist"
        self._output_file = "Networking.txt"
        self._type = "plist"

    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/NetworkInterfaces.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))

            if os.path.isfile(plist_file):
                with open(plist_file, "rb") as plist_to_load:
                    plist = plistlib.load(plist_to_load)
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", plist_file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
                output_file.close()
                return

            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            #                         "mavericks"]:
                parse_os = Parse01(output_file, plist)
                parse_os.parse()

            elif self._os_version in ["mountain_lion", "lion", "snow_leopard"]:
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
            if "Interfaces" in self._data_file:
                network_interfaces = self._data_file["Interfaces"]
                for network_interface in network_interfaces:
                    if "Active" in network_interface:
                        self._output_file.write("Active                   : {0}\r\n".format(network_interface["Active"]))
                    if "BSD Name" in network_interface:
                        self._output_file.write("BSD Name                 : {0}\r\n".format(network_interface["BSD Name"]))
                    if "IOBuiltin" in network_interface:
                        self._output_file.write("IOBuiltin                : {0}\r\n".format(network_interface["IOBuiltin"]))
                    if "IOInterfaceNamePrefix" in network_interface:
                        self._output_file.write("IO Interface Name Prefix : {0}\r\n".format(network_interface["IOInterfaceNamePrefix"]))
                    if "IOInterfaceType" in network_interface:
                        self._output_file.write("IO Interface Type        : {0}\r\n".format(network_interface["IOInterfaceType"]))
                    if "IOInterfaceUnit" in network_interface:
                        self._output_file.write("IO Interface Unit        : {0}\r\n".format(network_interface["IOInterfaceUnit"]))
                    if "IOMACAddress" in network_interface:
                        self._output_file.write("IO MAC Address           : {0}\r\n".format(binascii.hexlify(network_interface["IOMACAddress"])))
                    if "SCNetworkInterfaceInfo" in network_interface:
                        self._output_file.write("SC Network Interface Info: {0}\r\n".format(network_interface["SCNetworkInterfaceInfo"]["UserDefinedName"]))
                    if "SCNetworkInterfaceType" in network_interface:
                        self._output_file.write("SC Network Interface Type: {0}\r\n".format(network_interface["SCNetworkInterfaceType"]))
                    self._output_file.write("\r\n")
################################
# Move to own Plugin?
            if "Model" in self._data_file:
                self._output_file.write("Model: {0}\r\n".format(self._data_file["Model"]))
################################
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
            if "Interfaces" in self._data_file:
                network_interfaces = self._data_file["Interfaces"]
                for network_interface in network_interfaces:
                    if "Active" in network_interface:
                        self._output_file.write("Active                   : {0}\r\n".format(network_interface["Active"]))
                    if "BSD Name" in network_interface:
                        self._output_file.write("BSD Name                 : {0}\r\n".format(network_interface["BSD Name"]))
                    if "IOBuiltin" in network_interface:
                        self._output_file.write("IOBuiltin                : {0}\r\n".format(network_interface["IOBuiltin"]))
                    if "IOInterfaceType" in network_interface:
                        self._output_file.write("IO Interface Type        : {0}\r\n".format(network_interface["IOInterfaceType"]))
                    if "IOInterfaceUnit" in network_interface:
                        self._output_file.write("IO Interface Unit        : {0}\r\n".format(network_interface["IOInterfaceUnit"]))
                    if "IOMACAddress" in network_interface:
                        self._output_file.write("IO MAC Address           : {0}\r\n".format(binascii.hexlify(network_interface["IOMACAddress"])))
                    if "SCNetworkInterfaceInfo" in network_interface:
                        self._output_file.write("SC Network Interface Info: {0}\r\n".format(network_interface["SCNetworkInterfaceInfo"]["UserDefinedName"]))
                    if "SCNetworkInterfaceType" in network_interface:
                        self._output_file.write("SC Network Interface Type: {0}\r\n".format(network_interface["SCNetworkInterfaceType"]))
                    self._output_file.write("\r\n")
################################
# Move to own Plugin?
            if "Model" in self._data_file:
                self._output_file.write("Model: {0}\r\n".format(self._data_file["Model"]))
################################
        except KeyError:
            pass
