""" Module to parse /Library/Preferences/SystemConfiguration/preferences.plist """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class NetworkPreferences(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/preferences.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Network Preferences")
        self.set_description("Parse data from preferences.plist")
        self.set_data_file("preferences.plist")
        self.set_output_file("Networking.txt")
        self.set_type("plist")

    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/preferences.plist
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
                                    "mavericks", "mountain_lion", "lion"]:
                parse_os = ParseVers110107(output_file, plist)
                parse_os.parse()
            elif self._os_version == "snow_leopard":
                parse_os = ParseVers106(output_file, plist)
                parse_os.parse()
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()

class ParseVers110107():
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
            if "CurrentSet" in self._data_file:
                self._output_file.write("Current Set: {0}\r\n".format(self._data_file["CurrentSet"]))
            if "Model" in self._data_file:
                self._output_file.write("Model: {0}\r\n".format(self._data_file["Model"]))
            if "NetworkServices" in self._data_file:
                self._output_file.write("NetworkServices:\r\n")
                network_services = self._data_file["NetworkServices"].keys()
                for service_key in network_services:
                    self._output_file.write("\tService Key: {0}\r\n".format(service_key))

                    if "DNS" in self._data_file["NetworkServices"][service_key]:
                        if len(self._data_file["NetworkServices"][service_key]["DNS"]) == 0:
                            self._output_file.write("\t\tDNS: No DNS data.\r\n")
                        else:
                            self._output_file.write("\t\tDNS: {0}\r\n".format(self._data_file["NetworkServices"][service_key]["DNS"]))

                    if "IPv4" in self._data_file["NetworkServices"][service_key]:
                        if len(self._data_file["NetworkServices"][service_key]["IPv4"]) == 0:
                            self._output_file.write("\t\tIPv4: No IPv4 data.\r\n")
                        else:
                            self._output_file.write("\t\tIPv4: {0}\r\n".format(self._data_file["NetworkServices"][service_key]["IPv4"]["ConfigMethod"]))

                    if "IPv6" in self._data_file["NetworkServices"][service_key]:
                        if len(self._data_file["NetworkServices"][service_key]["IPv6"]) == 0:
                            self._output_file.write("\t\tIPv6: No IPv6 data.\r\n")
                        else:
                            self._output_file.write("\t\tIPv6: {0}\r\n".format(self._data_file["NetworkServices"][service_key]["IPv6"]["ConfigMethod"]))

                    if "Interface" in self._data_file["NetworkServices"][service_key]:
                        if len(self._data_file["NetworkServices"][service_key]["Interface"]) == 0:
                            self._output_file.write("\t\tInterface: No Interface data.\r\n")
                        else:
                            self._output_file.write("\t\tInterface:\r\n")
                            self._output_file.write("\t\t\tDeviceName       : {0}\r\n".format(self._data_file["NetworkServices"][service_key]["Interface"]["DeviceName"]))
                            self._output_file.write("\t\t\tHardware         : {0}\r\n".format(self._data_file["NetworkServices"][service_key]["Interface"]["Hardware"]))
                            self._output_file.write("\t\t\tType             : {0}\r\n".format(self._data_file["NetworkServices"][service_key]["Interface"]["Type"]))
                            self._output_file.write("\t\t\tUser Defined Name: {0}\r\n".format(self._data_file["NetworkServices"][service_key]["Interface"]["UserDefinedName"]))

                    if "Proxies" in self._data_file["NetworkServices"][service_key]:
                        if len(self._data_file["NetworkServices"][service_key]["Proxies"]) == 0:
                            self._output_file.write("\t\tProxies: No Proxies data.\r\n")
                        else:
                            self._output_file.write("\t\tProxies:\r\n")
                            if "ExceptionsList" in self._data_file["NetworkServices"][service_key]["Proxies"]:
                                for proxy_exception in \
                                        self._data_file["NetworkServices"][service_key]["Proxies"]["ExceptionsList"]:
                                    self._output_file.write("\t\t\tException: {0}\r\n".format(proxy_exception))
                            self._output_file.write("\t\t\tFTP Passive: {0}\r\n".format(self._data_file["NetworkServices"][service_key]["Proxies"]["FTPPassive"]))

                    if "SMB" in self._data_file["NetworkServices"][service_key]:
                        if len(self._data_file["NetworkServices"][service_key]["SMB"]) == 0:
                            self._output_file.write("\t\tSMB: No SMB data.\r\n")
                        else:
                            self._output_file.write("\t\tSMB: {0}\r\n".format(self._data_file["NetworkServices"][service_key]["SMB"]))

                    if "UserDefinedName" in self._data_file["NetworkServices"][service_key]:
                        self._output_file.write("\t\t\tUserDefinedName: {0}\r\n".format(self._data_file["NetworkServices"][service_key]["UserDefinedName"]))

                    self._output_file.write("\r\n")
                # END SERVICES LOOP

            if "Sets" in self._data_file:
                self._output_file.write("Sets:\r\n")
                network_sets = self._data_file["Sets"]
                for network_set in network_sets:
                    if "Network" in self._data_file["Sets"][network_set]:
                        self._output_file.write("\tGlobal:\r\n")
                        if "IPv4" in self._data_file["Sets"][network_set]["Network"]["Global"]:
                            self._output_file.write("\t\tIPv4 Service Order:\r\n")
                            for item in self._data_file["Sets"][network_set]["Network"]["Global"]["IPv4"]["ServiceOrder"]:
                                self._output_file.write("\t\t\tService: {0}\r\n".format(item))
                        if "Interface" in self._data_file["Sets"][network_set]["Network"]:
                            keys = self._data_file["Sets"][network_set]["Network"].keys()
                            for key in keys:
                                if key == "Interface":
                                    interface_dict = self._data_file["Sets"][network_set]["Network"][key]
                                    self._output_file.write("\tInterface:\r\n")
                                    for interface_key in interface_dict:
                                        self._output_file.write("\t\tInterface Name: {0}\r\n".format(interface_key))
                                        ik_dict = interface_dict[interface_key]
                                        for ik_key in ik_dict:
                                            self._output_file.write("\t\tType: {0}\r\n".format(ik_key))
                                            join_mode = ik_dict.get(ik_key).get("JoinModeFallback")
                                            for item in join_mode:
                                                self._output_file.write("\t\t\tJoin Mode Fallback      : {0}\r\n".format(item))
                                            self._output_file.write("\t\t\tPower Enabled           : {0}\r\n".format(ik_dict.get(ik_key).get("PowerEnabled")))
                                            self._output_file.write("\t\t\tRemember Joined Networks: {0}\r\n".format(ik_dict.get(ik_key).get("RememberJoinedNetworks")))
                                            self._output_file.write("\t\t\tVersion                 : {0}\r\n".format(ik_dict.get(ik_key).get("Version")))
                                            self._output_file.write("\r\n")
                                if key == "Service":
                                    self._output_file.write("\tService:\r\n")
                                    for service_key in self._data_file["Sets"][network_set]["Network"][key]:
                                        self._output_file.write("\t\t{0}\r\n".format(service_key))
                                        self._output_file.write("\t\t\tLink: {0}\r\n".format(self._data_file["Sets"][network_set]["Network"][key].get(service_key).get("__LINK__")))
                                    self._output_file.write("\r\n")
                    if "UserDefinedName" in self._data_file["Sets"][network_set]:
                        self._output_file.write("\tUserDefinedName: {0}\r\n".format(self._data_file["Sets"][network_set]["UserDefinedName"]))
                        self._output_file.write("\r\n")

            if "System" in self._data_file:
                self._output_file.write("System:\r\n")
                self._output_file.write("\tLocal Host Name: {0}\r\n".format(self._data_file["System"]["Network"]["HostNames"]["LocalHostName"]))
                self._output_file.write("\tComputer Name: {0}\r\n".format(self._data_file["System"]["System"]["ComputerName"]))
                self._output_file.write("\tComputer Name: {0}\r\n".format(self._data_file["System"]["System"]["ComputerNameEncoding"]))
                self._output_file.write("\r\n")

            if "VirtualNetworkInterfaces" in self._data_file:
                self._output_file.write("Virtual Network Interfaces:\r\n")
                for vni_key in self._data_file["VirtualNetworkInterfaces"]:
                    self._output_file.write("\t{0}\r\n".format(vni_key))  # Bridge
                    vni_dict = self._data_file["VirtualNetworkInterfaces"][vni_key]
                    self._output_file.write("\t\t{0}\r\n".format(vni_dict))

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
            if "CurrentSet" in self._data_file:
                self._output_file.write("Current Set: {0}\r\n".format(self._data_file["CurrentSet"]))
            self._output_file.write("Network Services:\r\n")
            network_services = self._data_file["NetworkServices"]
            for network_service_name in network_services:
                self._output_file.write("Network Service Name: {0}\r\n".format(network_service_name))
                network_service = network_services[network_service_name]
                if "DNS" in network_service:
                    self._output_file.write("\tDNS              : {0}\r\n".format(str(network_service["DNS"])))
                if "IPv4" in network_service:
                    self._output_file.write("\tIPv4             : {0}\r\n".format(network_service["IPv4"]["ConfigMethod"]))
                if "IPv6" in network_service:
                    self._output_file.write("\tIPv6             : {0}\r\n".format(network_service["IPv6"]["ConfigMethod"]))
                if "Interface" in network_service:
                    self._output_file.write("\tInterface:\r\n")
                    self._output_file.write("\t\tDevice Name      : {0}\r\n".format(network_service["Interface"]["DeviceName"]))
                    self._output_file.write("\t\tHardware         : {0}\r\n".format(network_service["Interface"]["Hardware"]))
                    self._output_file.write("\t\tType             : {0}\r\n".format(network_service["Interface"]["Type"]))
                    self._output_file.write("\t\tUser Defined Name: {0}\r\n".format(network_service["Interface"]["UserDefinedName"]))
                if "Proxies" in network_service:
                    proxies = network_service["Proxies"]
                    if "ExceptionsList" in proxies:
                        self._output_file.write("\tExceptions List:\r\n")
                        for proxy_exception in proxies["ExceptionsList"]:
                            self._output_file.write("\t\t{0}\r\n".format(proxy_exception))
                    if "FTPPassive" in proxies:
                        self._output_file.write("\tFTP Passive: {0}\r\n".format(proxies["FTPPassive"]))
                if "SMB" in network_service:
                    self._output_file.write("\tSMB              : {0}\r\n".format(str(network_service["SMB"])))
                if "AppleTalk" in network_service:
                    self._output_file.write("\tApple Talk       : {0}\r\n".format(str(network_service["AppleTalk"])))
                if "UserDefinedName" in network_service:
                    self._output_file.write("\tUser Defined Name: {0}\r\n".format(network_service["UserDefinedName"]))
                if "Modem" in network_service:
                    modem = network_service["Modem"]
                    self._output_file.write("\tModem\r\n")
                    if "ConnectionPersonality" in modem:
                        self._output_file.write("\t\tConnection Personality : {0}\r\n".format(modem["ConnectionPersonality"]))
                    if "ConnectionScript" in modem:
                        self._output_file.write("\t\tConnection Script      : {0}\r\n".format(modem["ConnectionScript"]))
                    if "DataCompression" in modem:
                        self._output_file.write("\t\tData Compression       : {0}\r\n".format(modem["DataCompression"]))
                    if "DeviceModel" in modem:
                        self._output_file.write("\t\tDevice Model           : {0}\r\n".format(modem["DeviceModel"]))
                    if "DeviceVendor" in modem:
                        self._output_file.write("\t\tDevice Vendor          : {0}\r\n".format(modem["DeviceVendor"]))
                    if "DialMode" in modem:
                        self._output_file.write("\t\tDial Mode              : {0}\r\n".format(modem["DialMode"]))
                    if "ErrorCorrection" in modem:
                        self._output_file.write("\t\tError Correction       : {0}\r\n".format(modem["ErrorCorrection"]))
                    if "PulseDial" in modem:
                        self._output_file.write("\t\tPulse Dial             : {0}\r\n".format(modem["PulseDial"]))
                    if "Speaker" in modem:
                        self._output_file.write("\t\tSpeaker                : {0}\r\n".format(modem["Speaker"]))
                if "PPP" in network_service:
                    ppp = network_service["PPP"]
                    self._output_file.write("\tPPP\r\n")
                    if "ACSPEnabled" in ppp:
                        self._output_file.write("\t\tACSP Enabled                  : {0}\r\n".format(ppp["ACSPEnabled"]))
                    if "CommDisplayTerminalWindow" in ppp:
                        self._output_file.write("\t\tComm Display Terminal Window  : {0}\r\n".format(ppp["CommDisplayTerminalWindow"]))
                    if "CommRedialCount" in ppp:
                        self._output_file.write("\t\tComm Redial Count             : {0}\r\n".format(ppp["CommRedialCount"]))
                    if "CommRedialEnabled" in ppp:
                        self._output_file.write("\t\tComm Redial Enabled           : {0}\r\n".format(ppp["CommRedialEnabled"]))
                    if "CommRedialInterval" in ppp:
                        self._output_file.write("\t\tComm Redial Interval          : {0}\r\n".format(ppp["CommRedialInterval"]))
                    if "CommUseTerminalScript" in ppp:
                        self._output_file.write("\t\tComm Use Terminal Script      : {0}\r\n".format(ppp["CommUseTerminalScript"]))
                    if "DialOnDemand" in ppp:
                        self._output_file.write("\t\tDial On Demand                : {0}\r\n".format(ppp["DialOnDemand"]))
                    if "DisconnectOnFastUserSwitch" in ppp:
                        self._output_file.write("\t\tDisconnect On Fast User Switch: {0}\r\n".format(ppp["DisconnectOnFastUserSwitch"]))
                    if "DisconnectOnIdle" in ppp:
                        self._output_file.write("\t\tDisconnect On Idle            : {0}\r\n".format(ppp["DisconnectOnIdle"]))
                    if "DisconnectOnIdleTimer" in ppp:
                        self._output_file.write("\t\tDisconnect On Idle Timer      : {0}\r\n".format(ppp["DisconnectOnIdleTimer"]))
                    if "DisconnectOnLogout" in ppp:
                        self._output_file.write("\t\tDisconnect On Logout          : {0}\r\n".format(ppp["DisconnectOnLogout"]))
                    if "DisconnectOnSleep" in ppp:
                        self._output_file.write("\t\tDisconnect On Sleep           : {0}\r\n".format(ppp["DisconnectOnSleep"]))
                    if "IPCPCompressionVJ" in ppp:
                        self._output_file.write("\t\tIPCP Compression VJ           : {0}\r\n".format(ppp["IPCPCompressionVJ"]))
                    if "IdleReminder" in ppp:
                        self._output_file.write("\t\tIdle Reminder                 : {0}\r\n".format(ppp["IdleReminder"]))
                    if "IdleReminderTimer" in ppp:
                        self._output_file.write("\t\tIdle Reminder Timer           : {0}\r\n".format(ppp["IdleReminderTimer"]))
                    if "LCPEchoEnabled" in ppp:
                        self._output_file.write("\t\tLCP Echo Enabled              : {0}\r\n".format(ppp["LCPEchoEnabled"]))
                    if "LCPEchoFailure" in ppp:
                        self._output_file.write("\t\tLCP Echo Failure              : {0}\r\n".format(ppp["LCPEchoFailure"]))
                    if "LCPEchoInterval" in ppp:
                        self._output_file.write("\t\tLCP Echo Interval             : {0}\r\n".format(ppp["LCPEchoInterval"]))
                    if "Logfile" in ppp:
                        self._output_file.write("\t\tLogfile                       : {0}\r\n".format(ppp["Logfile"]))
                    if "VerboseLogging" in ppp:
                        self._output_file.write("\t\tVerbose Logging               : {0}\r\n".format(ppp["VerboseLogging"]))
                self._output_file.write("\r\n")
            self._output_file.write("Sets:\r\n")
            for network_set_name in self._data_file["Sets"]:
                self._output_file.write("\tNetwork Set: {0}\r\n".format(network_set_name))
                network_set = self._data_file["Sets"][network_set_name]
                if "Network" in network_set:
                    network = network_set["Network"]
                    if "Global" in network:
                        self._output_file.write("\t\tGlobal   : {0}\r\n".format(network["Global"]))
                    if "Interface" in network:
                        self._output_file.write("\t\tInterface: {0}\r\n".format(network["Interface"]))
                    if "Service" in network:
                        self._output_file.write("\t\tService  : {0}\r\n".format(network["Service"]))
                if "UserDefinedName" in network_set:
                    self._output_file.write("\t\tUser Defined Name : {0}\r\n".format(network_set["UserDefinedName"]))
                self._output_file.write("\r\n")
            self._output_file.write("System:\r\n")
            if "System" in self._data_file["System"]:
                if "ComputerName" in self._data_file["System"]["System"]:
                    self._output_file.write("\tComputer Name          : {0}\r\n".format(self._data_file["System"]["System"]["ComputerName"]))
                if "ComputerNameEncoding" in self._data_file["System"]["System"]:
                    self._output_file.write("\tComputer Name Encoding : {0}\r\n".format(self._data_file["System"]["System"]["ComputerNameEncoding"]))
            if "Network" in self._data_file["System"]:
                if "HostNames" in self._data_file["System"]["Network"]:
                    self._output_file.write("\tLocalhost Name         : {0}\r\n".format(self._data_file["System"]["Network"]["HostNames"]["LocalHostName"]))

            self._output_file.write("\r\n")

        except KeyError:
            pass
