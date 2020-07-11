from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib

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
        self._name = "Airport Preferences"
        self._description = "Parse data from com.apple.airport.preferences.plist"
        self._data_file = "com.apple.airport.preferences.plist"
        self._output_file = "Networking.txt"
        self._type = "plist"
    
    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(plist_file))
            # if self._os_version in ["big_sur", "catalina"]:
            if self._os_version in ["catalina"]:
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "Counter" in plist:
                            of.write("Counter                  : {0}\r\n".format(plist["Counter"]))
                        if "DeviceUUID" in plist:
                            of.write("Device UUID:             : {}\r\n".format(plist["DeviceUUID"]))
                        if "KnownNetworks" in plist:
                            known_networks = plist["KnownNetworks"]
                            for network_key in known_networks:
                                of.write("Known Network            : {0}\r\n".format(network_key))
                                of.write("\tAdded By             : {0}\r\n".format(known_networks[network_key]["AddedBy"]))
                                of.write("\tLEAKY AP BSSID       : {0}\r\n".format(
                                    known_networks[network_key]["BSSIDList"][0]))
                                of.write("\tLEAKY AP BSSID       : {0}\r\n".format(
                                    known_networks[network_key]["BSSIDList"][1]))
                                of.write("\tCaptive Bypass       : {0}\r\n".format(
                                    known_networks[network_key]["CaptiveBypass"]))
                                channel_history = known_networks[network_key]["ChannelHistory"]
                                of.write("\tChannel History")
                                for channel in channel_history:
                                    if "Timestamp" in channel:
                                        of.write("\t\tTimestamp   : {0}\r\n".format(channel["Timestamp"]))
                                    if "Channel" in channel:
                                        of.write("\t\tChannel     : {0}\r\n".format(channel["Channel"]))

                                if "Closed" in known_networks[network_key]:
                                    of.write("\tClosed               : {0}\r\n".format(known_networks[network_key]["Closed"]))
                                of.write("\tDisabled             : {0}\r\n".format(known_networks[network_key]["Disabled"]))
                                if "LastConnected" in known_networks[network_key]:
                                    of.write("\tLast Connected  : {0}\r\n".format(
                                        known_networks[network_key]["LastConnected"]))
                                if "HiddenNetwork" in known_networks[network_key]:
                                    of.write("\tHidden Network       : {0}\r\n".format(
                                        known_networks[network_key]["HiddenNetwork"]))
                                if "LastAutoJoinAt" in known_networks[network_key]:
                                    of.write("\tLast Auto Join At    : {0}\r\n".format(
                                        known_networks[network_key]["LastAutoJoinAt"]))
                                of.write("\tNetwork Was Captive  : {0}\r\n".format(
                                    known_networks[network_key]["NetworkWasCaptive"]))
                                of.write("\tPasspoint            : {0}\r\n".format(known_networks[network_key]["Passpoint"]))
                                of.write("\tPersonal Hotspot     : {0}\r\n".format(
                                    known_networks[network_key]["PersonalHotspot"]))
                                of.write("\tPossibly Hidden Network : {0}\r\n".format(
                                    known_networks[network_key]["PossiblyHiddenNetwork"]))
                                of.write("\tRoaming Profile Type : {0}\r\n".format(
                                    known_networks[network_key]["RoamingProfileType"]))
                                of.write("\tSP Roaming           : {0}\r\n".format(known_networks[network_key]["SPRoaming"]))
                                of.write("\tSSID                 : {0}\r\n".format(known_networks[network_key]["SSID"]))
                                of.write(
                                    "\tSSID String          : {0}\r\n".format(known_networks[network_key]["SSIDString"]))
                                of.write("\tSecurity Type        : {0}\r\n".format(
                                    known_networks[network_key]["SecurityType"]))
                                of.write("\tShare Mode           : {0}\r\n".format(known_networks[network_key]["ShareMode"]))
                                of.write(
                                    "\tSystem Mode          : {0}\r\n".format(known_networks[network_key]["SystemMode"]))
                                of.write("\tTemporarily Disabled : {0}\r\n".format(
                                    known_networks[network_key]["TemporarilyDisabled"]))
                                of.write("\tUser Role            : {0}\r\n".format(known_networks[network_key]["UserRole"]))
                        if "PreferredOrder" in plist:
                            of.write("Preferred Order\r\n")
                            orders = plist["PreferredOrder"]
                            for order in orders:
                                of.write("\t{0}\r\n".format(order))
                        # TODO parse UpdateHistory
                        # if "UpdateHistory" in plist:
                        #     of.write("Update History\r\n")
                        #     updates = plist["UpdateHistory"]
                        #     for update in updates:
                        #         if "Previous" in update:
                        #             if len(update["Previous"]) == 0:
                        #                 of.write("\tNo data in Previous.\r\n")
                        #             else:
                        #                 of.write("\tPrevious: {0}\r\n".format(update["Previous"]))
                        #         if "Timestamp" in update:
                        #             of.write("\tTimestamp: {0}\r\n".format(update["Timestamp"]))

                        if "Version" in plist:
                            # of.write("Version: {0}\r\n".format(plist["Version"]))
                            print("Version: {0}\r\n".format(plist["Version"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            elif self._os_version in ["mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "Counter" in plist:
                            of.write("Counter                  : {0}\r\n".format(plist["Counter"]))
                        if "KnownNetworks" in plist:
                            known_networks = plist["KnownNetworks"]
                            for network_key in known_networks:
                                of.write("Network Key              : {0}\r\n".format(network_key))
                                of.write("\tAuto Login             : {0}\r\n"
                                         .format(known_networks[network_key]["AutoLogin"]))
                                of.write("\tCaptive                : {0}\r\n"
                                         .format(known_networks[network_key]["Captive"]))
                                of.write("\tClosed                 : {0}\r\n"
                                         .format(known_networks[network_key]["Closed"]))
                                of.write("\tDisabled               : {0}\r\n"
                                         .format(known_networks[network_key]["Disabled"]))
                                of.write("\tLast Connected         : {0}\r\n"
                                         .format(known_networks[network_key]["LastConnected"]))
                                of.write("\tPasspoint              : {0}\r\n"
                                         .format(known_networks[network_key]["Passpoint"]))
                                of.write("\tPossibly Hidden Network: {0}\r\n"
                                         .format(known_networks[network_key]["PossiblyHiddenNetwork"]))
                                of.write("\tRoaming Profile Type   : {0}\r\n"
                                         .format(known_networks[network_key]["RoamingProfileType"]))
                                of.write("\tSP Roaming             : {0}\r\n"
                                         .format(known_networks[network_key]["SPRoaming"]))
                                of.write("\tSSID                   : {0}\r\n"
                                         .format(known_networks[network_key]["SSID"]))
                                of.write("\tSSID String            : {0}\r\n"
                                         .format(known_networks[network_key]["SSIDString"]))
                                of.write("\tSecurity Type          : {0}\r\n"
                                         .format(known_networks[network_key]["SecurityType"]))
                                of.write("\tSystem Mode            : {0}\r\n"
                                         .format(known_networks[network_key]["SystemMode"]))
                                of.write("\tTemporarily Disabled   : {0}\r\n"
                                         .format(known_networks[network_key]["TemporarilyDisabled"]))
                                
                                channel_history = known_networks[network_key]["ChannelHistory"]
                                of.write("\tChannel History\r\n")
                                for channel in channel_history:
                                    if "Timestamp" in channel:
                                        of.write("\t\tTimestamp   : {0}\r\n".format(channel["Timestamp"]))
                                    if "Channel" in channel:
                                        of.write("\t\tChannel   : {0}\r\n".format(channel["Channel"]))

                        if "PreferredOrder" in plist:
                            of.write("Preferred Order\r\n")
                            orders = plist["PreferredOrder"]
                            for order in orders:
                                of.write("\t{0}\r\n".format(order))
                                
                        if "UpdateHistory" in plist:
                            of.write("Update History\r\n")
                            updates = plist["UpdateHistory"]
                            for update in updates:
                                if "Previous" in update:
                                    if len(update["Previous"]) == 0:
                                        of.write("\tNo data in Previous.\r\n")
                                    else:
                                        of.write("\tPrevious: {0}\r\n".format(update["Previous"]))
                                if "Timestamp" in update:
                                    of.write("\tTimestamp: {0}\r\n".format(update["Timestamp"]))
                                    
                        if "Version" in plist:
                            of.write("Version: {0}\r\n".format(plist["Version"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            
            elif self._os_version == "mavericks":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        of.write("Remembered Networks\r\n\r\n")
                        for remembered in plist["RememberedNetworks"]:
                            if "AutoLogin" in remembered:
                                of.write("\tAuto Login: {0}\r\n".format(remembered["AutoLogin"]))
                            if "Captive" in remembered:
                                of.write("\tCaptive: {0}\r\n".format(remembered["Captive"]))
                            if "Closed" in remembered:
                                of.write("\tClosed: {0}\r\n".format(remembered["Closed"]))
                            if "Disabled" in remembered:
                                of.write("\tDisabled: {0}\r\n".format(remembered["Disabled"]))
                            if "LastConnected" in remembered:
                                of.write("\tLast Connected: {0}\r\n".format(remembered["LastConnected"]))
                            if "Passpoint" in remembered:
                                of.write("\tPasspoint: {0}\r\n".format(remembered["Passpoint"]))
                            if "PossiblyHiddenNetwork" in remembered:
                                of.write("\tPossibly Hidden Network: {0}\r\n"
                                         .format(remembered["PossiblyHiddenNetwork"]))
                            if "SPRoaming" in remembered:
                                of.write("\tSPRoaming: {0}\r\n".format(remembered["SPRoaming"]))
                            if "SSID" in remembered:
                                of.write("\tSSID: {0}\r\n".format(remembered["SSID"]))
                            if "SSIDString" in remembered:
                                of.write("\tSSID String: {0}\r\n".format(remembered["SSIDString"]))
                            if "SecurityType" in remembered:
                                of.write("\tSecurity Type: {0}\r\n".format(remembered["SecurityType"]))
                            if "SystemMode" in remembered:
                                of.write("\tSystem Mode: {0}\r\n".format(remembered["SystemMode"]))
                            if "TemporarilyDisabled" in remembered:
                                of.write("\tTemporarily Disabled: {0}\r\n".format(remembered["TemporarilyDisabled"]))
                            of.write("\r\n")
                            
                        if "Version" in plist:
                            of.write("Version: {0}\r\n".format(plist["Version"]))
                        of.write("\r\n")
                    except KeyError:
                        pass
                        
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            elif self._os_version in ["mountain_lion", "lion"]:
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        of.write("Remembered Networks\r\n\r\n")
                        remembered = None
                        for remembered in plist["RememberedNetworks"]:
                            if "AutoLogin" in remembered:
                                of.write("\tAuto Login: {0}\r\n".format(remembered["AutoLogin"]))
                            if "CachedScanRecord" in remembered:
                                of.write("\tCached Scan Record\r\n")
                                of.write("\t\tChannel: {0}\r\n".format(remembered["CachedScanRecord"]["BSSID"]))
                                of.write("\t\tChannel: {0}\r\n".format(remembered["CachedScanRecord"]["CHANNEL"]))
                                of.write("\t\tSSID: {0}\r\n".format(remembered["CachedScanRecord"]["SSID"]))
                                of.write("\t\tSSID String: {0}\r\n".format(remembered["CachedScanRecord"]["SSID_STR"]))
                        if "Captive" in remembered:
                            of.write("\tCaptive: {0}\r\n".format(remembered["Captive"]))
                        if "Closed" in remembered:
                            of.write("\tClosed: {0}\r\n".format(remembered["Closed"]))
                        if "Disabled" in remembered:
                            of.write("\tDisabled: {0}\r\n".format(remembered["Disabled"]))
                        if "LastConnected" in remembered:
                            of.write("\tLast Connected: {0}\r\n".format(remembered["LastConnected"]))
                        if "SSID" in remembered:
                            of.write("\tSSID: {0}\r\n".format(remembered["SSID"]))
                        if "SSIDString" in remembered:
                            of.write("\tSSID String: {0}\r\n".format(remembered["SSIDString"]))
                        if "SecurityType" in remembered:
                            of.write("\tSecurity Type: {0}\r\n".format(remembered["SecurityType"]))
                        if "SystemMode" in remembered:
                            of.write("\tSystem Mode: {0}\r\n".format(remembered["SystemMode"]))
                        if "TemporarilyDisabled" in remembered:
                            of.write("\tTemporarily Disabled: {0}\r\n".format(remembered["TemporarilyDisabled"]))
                        of.write("\r\n")
                        if "Version" in plist:
                            of.write("Version: {0}\r\n".format(plist["Version"]))
                        of.write("\r\n")
                    except KeyError:
                            pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "KnownNetworks" in plist:
                            for known_network in plist["KnownNetworks"]:
                                of.write("Known Network: {0}\r\n".format(known_network))
                                for channel in plist["KnownNetworks"][known_network]["Remembered channels"]:
                                    of.write("\tChannel           : {0}\r\n".format(channel))
                                of.write("\tSSID              : {0}\r\n"
                                         .format(plist["KnownNetworks"][known_network]["SSID_STR"]))
                                of.write("\tSecurity Type     : {0}\r\n"
                                         .format(plist["KnownNetworks"][known_network]["SecurityType"]))
                                if "Unique Password ID" in plist["KnownNetworks"][known_network]:
                                    of.write("\tUnique Password ID: {0}\r\n"
                                             .format(plist["KnownNetworks"][known_network]["Unique Password ID"]))
                                of.write("\tTimestamp         : {0}\r\n"
                                         .format(plist["KnownNetworks"][known_network]["_timeStamp"]))
                                of.write("\r\n")

                        if "en1" in plist:
                            of.write("en1\r\n")
                            if "RecentNetworks" in plist["en1"]:
                                recent_networks = plist["en1"]["RecentNetworks"]
                                of.write("Recent Networks:\r\n\r\n")
                                for recent_network in recent_networks:
                                    if "SSID_STR" in recent_network:
                                        of.write("\tSSID              : {0}\r\n"
                                                 .format(recent_network["SSID_STR"]))
                                    if "SecurityType" in recent_network:
                                        of.write("\tSecurity Type     : {0}\r\n"
                                                 .format(recent_network["SecurityType"]))
                                    if "Unique Network ID" in recent_network:
                                        of.write("\tUnique Network ID : {0}\r\n"
                                                 .format(recent_network["Unique Network ID"]))
                                    if "Unique Password ID" in recent_network:
                                        of.write("\tUnique Password ID: {0}\r\n"
                                                 .format(recent_network["Unique Password ID"]))
                                    of.write("\r\n")
                            else:
                                of.write("\tNo Recent Networks\r\n")
                    except KeyError:
                        pass
            else:
                logging.warning("[WARNING] Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
