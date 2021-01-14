""" Module to parse Airport data """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class AirportPreferences(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Airport Preferences")
        self.set_description("Parse data from com.apple.airport.preferences.plist")
        self.set_data_file("com.apple.airport.preferences.plist")
        self.set_output_file("Networking.txt")
        self.set_type("plist")

    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist
        """
        with codecs.open(os.path.join(self.get_output_dir, self.get_output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self.get_name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self.get_input_dir, "Library", "Preferences", "SystemConfiguration", self.get_data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))
            if os.path.isfile(plist_file):
                with open(plist_file, "rb") as plist_to_load:
                    plist = plistlib.load(plist_to_load)
                plist_to_load.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.", plist_file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
                output_file.close()
                return

            if self._os_version in ["big_sur", "catalina"]:
                parse_macos = ParseVers1101015(output_file, plist)
                parse_macos.parse()
            elif self._os_version in ["mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                parse_macos = ParseVers10141010(output_file, plist)
                parse_macos.parse()
            elif self._os_version == "mavericks":
                parse_macos = ParseVers109(output_file, plist)
                parse_macos.parse()
            elif self._os_version in ["mountain_lion", "lion"]:
                parse_macos = ParseVers108107(output_file, plist)
                parse_macos.parse()
            elif self._os_version == "snow_leopard":
                parse_macos = ParseVers106(output_file, plist)
                parse_macos.parse()
            else:
                logging.warning("[WARNING] Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()

class ParseVers1101015():
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
            if "Counter" in self._data_file:
                self._output_file.write("Counter                  : {0}\r\n".format(self._data_file["Counter"]))
            if "DeviceUUID" in self._data_file:
                self._output_file.write("Device UUID:             : {}\r\n".format(self._data_file["DeviceUUID"]))
            if "KnownNetworks" in self._data_file:
                known_networks = self._data_file["KnownNetworks"]
                for network_key in known_networks:
                    self._output_file.write("Known Network            : {0}\r\n".format(network_key))
                    self._output_file.write("\tAdded By             : {0}\r\n".format(known_networks[network_key]["AddedBy"]))
                    self._output_file.write("\tLEAKY AP BSSID       : {0}\r\n".format(known_networks[network_key]["BSSIDList"][0]))
                    self._output_file.write("\tLEAKY AP BSSID       : {0}\r\n".format(known_networks[network_key]["BSSIDList"][1]))
                    self._output_file.write("\tCaptive Bypass       : {0}\r\n".format(known_networks[network_key]["CaptiveBypass"]))
                    channel_history = known_networks[network_key]["ChannelHistory"]
                    self._output_file.write("\tChannel History")
                    for channel in channel_history:
                        if "Timestamp" in channel:
                            self._output_file.write("\t\tTimestamp   : {0}\r\n".format(channel["Timestamp"]))
                        if "Channel" in channel:
                            self._output_file.write("\t\tChannel     : {0}\r\n".format(channel["Channel"]))

                    if "Closed" in known_networks[network_key]:
                        self._output_file.write("\tClosed               : {0}\r\n".format(known_networks[network_key]["Closed"]))
                    self._output_file.write("\tDisabled             : {0}\r\n".format(known_networks[network_key]["Disabled"]))
                    if "LastConnected" in known_networks[network_key]:
                        self._output_file.write("\tLast Connected  : {0}\r\n".format(known_networks[network_key]["LastConnected"]))
                    if "HiddenNetwork" in known_networks[network_key]:
                        self._output_file.write("\tHidden Network       : {0}\r\n".format(known_networks[network_key]["HiddenNetwork"]))
                    if "LastAutoJoinAt" in known_networks[network_key]:
                        self._output_file.write("\tLast Auto Join At    : {0}\r\n".format(known_networks[network_key]["LastAutoJoinAt"]))
                    self._output_file.write("\tNetwork Was Captive  : {0}\r\n".format(known_networks[network_key]["NetworkWasCaptive"]))
                    self._output_file.write("\tPasspoint            : {0}\r\n".format(known_networks[network_key]["Passpoint"]))
                    self._output_file.write("\tPersonal Hotspot     : {0}\r\n".format(known_networks[network_key]["PersonalHotspot"]))
                    self._output_file.write("\tPossibly Hidden Network : {0}\r\n".format(known_networks[network_key]["PossiblyHiddenNetwork"]))
                    self._output_file.write("\tRoaming Profile Type : {0}\r\n".format(known_networks[network_key]["RoamingProfileType"]))
                    self._output_file.write("\tSP Roaming           : {0}\r\n".format(known_networks[network_key]["SPRoaming"]))
                    self._output_file.write("\tSSID                 : {0}\r\n".format(known_networks[network_key]["SSID"]))
                    self._output_file.write("\tSSID String          : {0}\r\n".format(known_networks[network_key]["SSIDString"]))
                    self._output_file.write("\tSecurity Type        : {0}\r\n".format(known_networks[network_key]["SecurityType"]))
                    self._output_file.write("\tShare Mode           : {0}\r\n".format(known_networks[network_key]["ShareMode"]))
                    self._output_file.write("\tSystem Mode          : {0}\r\n".format(known_networks[network_key]["SystemMode"]))
                    self._output_file.write("\tTemporarily Disabled : {0}\r\n".format(known_networks[network_key]["TemporarilyDisabled"]))
                    self._output_file.write("\tUser Role            : {0}\r\n".format(known_networks[network_key]["UserRole"]))
            if "PreferredOrder" in self._data_file:
                self._output_file.write("Preferred Order\r\n")
                orders = self._data_file["PreferredOrder"]
                for order in orders:
                    self._output_file.write("\t{0}\r\n".format(order))
            # Parse UpdateHistory
            # if "UpdateHistory" in plist:
            #     self._output_file.write("Update History\r\n")
            #     updates = plist["UpdateHistory"]
            #     for update in updates:
            #         if "Previous" in update:
            #             if len(update["Previous"]) == 0:
            #                 self._output_file.write("\tNo data in Previous.\r\n")
            #             else:
            #                 self._output_file.write("\tPrevious: {0}\r\n".format(update["Previous"]))
            #         if "Timestamp" in update:
            #             self._output_file.write("\tTimestamp: {0}\r\n".format(update["Timestamp"]))

            if "Version" in self._data_file:
                self._output_file.write("Version: {0}\r\n".format(self._data_file["Version"]))
        except KeyError:
            pass

class ParseVers10141010():
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
            if "Counter" in self._data_file:
                self._output_file.write("Counter                  : {0}\r\n".format(self._data_file["Counter"]))
            if "KnownNetworks" in self._data_file:
                known_networks = self._data_file["KnownNetworks"]
                for network_key in known_networks:
                    self._output_file.write("Network Key              : {0}\r\n".format(network_key))
                    self._output_file.write("\tAuto Login             : {0}\r\n".format(known_networks[network_key]["AutoLogin"]))
                    self._output_file.write("\tCaptive                : {0}\r\n".format(known_networks[network_key]["Captive"]))
                    self._output_file.write("\tClosed                 : {0}\r\n".format(known_networks[network_key]["Closed"]))
                    self._output_file.write("\tDisabled               : {0}\r\n".format(known_networks[network_key]["Disabled"]))
                    self._output_file.write("\tLast Connected         : {0}\r\n".format(known_networks[network_key]["LastConnected"]))
                    self._output_file.write("\tPasspoint              : {0}\r\n".format(known_networks[network_key]["Passpoint"]))
                    self._output_file.write("\tPossibly Hidden Network: {0}\r\n".format(known_networks[network_key]["PossiblyHiddenNetwork"]))
                    self._output_file.write("\tRoaming Profile Type   : {0}\r\n".format(known_networks[network_key]["RoamingProfileType"]))
                    self._output_file.write("\tSP Roaming             : {0}\r\n".format(known_networks[network_key]["SPRoaming"]))
                    self._output_file.write("\tSSID                   : {0}\r\n".format(known_networks[network_key]["SSID"]))
                    self._output_file.write("\tSSID String            : {0}\r\n".format(known_networks[network_key]["SSIDString"]))
                    self._output_file.write("\tSecurity Type          : {0}\r\n".format(known_networks[network_key]["SecurityType"]))
                    self._output_file.write("\tSystem Mode            : {0}\r\n".format(known_networks[network_key]["SystemMode"]))
                    self._output_file.write("\tTemporarily Disabled   : {0}\r\n".format(known_networks[network_key]["TemporarilyDisabled"]))

                    channel_history = known_networks[network_key]["ChannelHistory"]
                    self._output_file.write("\tChannel History\r\n")
                    for channel in channel_history:
                        if "Timestamp" in channel:
                            self._output_file.write("\t\tTimestamp   : {0}\r\n".format(channel["Timestamp"]))
                        if "Channel" in channel:
                            self._output_file.write("\t\tChannel   : {0}\r\n".format(channel["Channel"]))

            if "PreferredOrder" in self._data_file:
                self._output_file.write("Preferred Order\r\n")
                orders = self._data_file["PreferredOrder"]
                for order in orders:
                    self._output_file.write("\t{0}\r\n".format(order))

            if "UpdateHistory" in self._data_file:
                self._output_file.write("Update History\r\n")
                updates = self._data_file["UpdateHistory"]
                for update in updates:
                    if "Previous" in update:
                        if len(update["Previous"]) == 0:
                            self._output_file.write("\tNo data in Previous.\r\n")
                        else:
                            self._output_file.write("\tPrevious: {0}\r\n".format(update["Previous"]))
                    if "Timestamp" in update:
                        self._output_file.write("\tTimestamp: {0}\r\n".format(update["Timestamp"]))

            if "Version" in self._data_file:
                self._output_file.write("Version: {0}\r\n".format(self._data_file["Version"]))
        except KeyError:
            pass

class ParseVers109():
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
            self._output_file.write("Remembered Networks\r\n\r\n")
            for remembered in self._data_file["RememberedNetworks"]:
                if "AutoLogin" in remembered:
                    self._output_file.write("\tAuto Login: {0}\r\n".format(remembered["AutoLogin"]))
                if "Captive" in remembered:
                    self._output_file.write("\tCaptive: {0}\r\n".format(remembered["Captive"]))
                if "Closed" in remembered:
                    self._output_file.write("\tClosed: {0}\r\n".format(remembered["Closed"]))
                if "Disabled" in remembered:
                    self._output_file.write("\tDisabled: {0}\r\n".format(remembered["Disabled"]))
                if "LastConnected" in remembered:
                    self._output_file.write("\tLast Connected: {0}\r\n".format(remembered["LastConnected"]))
                if "Passpoint" in remembered:
                    self._output_file.write("\tPasspoint: {0}\r\n".format(remembered["Passpoint"]))
                if "PossiblyHiddenNetwork" in remembered:
                    self._output_file.write("\tPossibly Hidden Network: {0}\r\n".format(remembered["PossiblyHiddenNetwork"]))
                if "SPRoaming" in remembered:
                    self._output_file.write("\tSPRoaming: {0}\r\n".format(remembered["SPRoaming"]))
                if "SSID" in remembered:
                    self._output_file.write("\tSSID: {0}\r\n".format(remembered["SSID"]))
                if "SSIDString" in remembered:
                    self._output_file.write("\tSSID String: {0}\r\n".format(remembered["SSIDString"]))
                if "SecurityType" in remembered:
                    self._output_file.write("\tSecurity Type: {0}\r\n".format(remembered["SecurityType"]))
                if "SystemMode" in remembered:
                    self._output_file.write("\tSystem Mode: {0}\r\n".format(remembered["SystemMode"]))
                if "TemporarilyDisabled" in remembered:
                    self._output_file.write("\tTemporarily Disabled: {0}\r\n".format(remembered["TemporarilyDisabled"]))
                self._output_file.write("\r\n")

            if "Version" in self._data_file:
                self._output_file.write("Version: {0}\r\n".format(self._data_file["Version"]))
            self._output_file.write("\r\n")
        except KeyError:
            pass

class ParseVers108107():
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
            self._output_file.write("Remembered Networks\r\n\r\n")
            remembered = None
            for remembered in self._data_file["RememberedNetworks"]:
                if "AutoLogin" in remembered:
                    self._output_file.write("\tAuto Login: {0}\r\n".format(remembered["AutoLogin"]))
                if "CachedScanRecord" in remembered:
                    self._output_file.write("\tCached Scan Record\r\n")
                    self._output_file.write("\t\tChannel: {0}\r\n".format(remembered["CachedScanRecord"]["BSSID"]))
                    self._output_file.write("\t\tChannel: {0}\r\n".format(remembered["CachedScanRecord"]["CHANNEL"]))
                    self._output_file.write("\t\tSSID: {0}\r\n".format(remembered["CachedScanRecord"]["SSID"]))
                    self._output_file.write("\t\tSSID String: {0}\r\n".format(remembered["CachedScanRecord"]["SSID_STR"]))
            if "Captive" in remembered:
                self._output_file.write("\tCaptive: {0}\r\n".format(remembered["Captive"]))
            if "Closed" in remembered:
                self._output_file.write("\tClosed: {0}\r\n".format(remembered["Closed"]))
            if "Disabled" in remembered:
                self._output_file.write("\tDisabled: {0}\r\n".format(remembered["Disabled"]))
            if "LastConnected" in remembered:
                self._output_file.write("\tLast Connected: {0}\r\n".format(remembered["LastConnected"]))
            if "SSID" in remembered:
                self._output_file.write("\tSSID: {0}\r\n".format(remembered["SSID"]))
            if "SSIDString" in remembered:
                self._output_file.write("\tSSID String: {0}\r\n".format(remembered["SSIDString"]))
            if "SecurityType" in remembered:
                self._output_file.write("\tSecurity Type: {0}\r\n".format(remembered["SecurityType"]))
            if "SystemMode" in remembered:
                self._output_file.write("\tSystem Mode: {0}\r\n".format(remembered["SystemMode"]))
            if "TemporarilyDisabled" in remembered:
                self._output_file.write("\tTemporarily Disabled: {0}\r\n".format(remembered["TemporarilyDisabled"]))
            self._output_file.write("\r\n")
            if "Version" in self._data_file:
                self._output_file.write("Version: {0}\r\n".format(self._data_file["Version"]))
            self._output_file.write("\r\n")
        except KeyError:
            pass

class ParseVers106():
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
            if "KnownNetworks" in self._data_file:
                for known_network in self._data_file["KnownNetworks"]:
                    self._output_file.write("Known Network: {0}\r\n".format(known_network))
                    for channel in self._data_file["KnownNetworks"][known_network]["Remembered channels"]:
                        self._output_file.write("\tChannel           : {0}\r\n".format(channel))
                    self._output_file.write("\tSSID              : {0}\r\n".format(self._data_file["KnownNetworks"][known_network]["SSID_STR"]))
                    self._output_file.write("\tSecurity Type     : {0}\r\n".format(self._data_file["KnownNetworks"][known_network]["SecurityType"]))
                    if "Unique Password ID" in self._data_file["KnownNetworks"][known_network]:
                        self._output_file.write("\tUnique Password ID: {0}\r\n"
                                                .format(self._data_file["KnownNetworks"][known_network]["Unique Password ID"]))
                    self._output_file.write("\tTimestamp         : {0}\r\n".format(self._data_file["KnownNetworks"][known_network]["_timeStamp"]))
                    self._output_file.write("\r\n")

            if "en1" in self._data_file:
                self._output_file.write("en1\r\n")
                if "RecentNetworks" in self._data_file["en1"]:
                    recent_networks = self._data_file["en1"]["RecentNetworks"]
                    self._output_file.write("Recent Networks:\r\n\r\n")
                    for recent_network in recent_networks:
                        if "SSID_STR" in recent_network:
                            self._output_file.write("\tSSID              : {0}\r\n".format(recent_network["SSID_STR"]))
                        if "SecurityType" in recent_network:
                            self._output_file.write("\tSecurity Type     : {0}\r\n".format(recent_network["SecurityType"]))
                        if "Unique Network ID" in recent_network:
                            self._output_file.write("\tUnique Network ID : {0}\r\n".format(recent_network["Unique Network ID"]))
                        if "Unique Password ID" in recent_network:
                            self._output_file.write("\tUnique Password ID: {0}\r\n".format(recent_network["Unique Password ID"]))
                        self._output_file.write("\r\n")
                else:
                    self._output_file.write("\tNo Recent Networks\r\n")
        except KeyError:
            pass
