from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib

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
        self._name = "Network Preferences"
        self._description = "Parse data from preferences.plist"
        self._data_file = "preferences.plist"
        self._output_file = "Networking.txt"
        self._type = "plist"
    
    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/preferences.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(plist_file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion"]:
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "CurrentSet" in plist:
                            of.write("Current Set: {0}\r\n".format(plist["CurrentSet"]))
                        if "Model" in plist:
                            of.write("Model: {0}\r\n".format(plist["Model"]))
                        if "NetworkServices" in plist:
                            of.write("NetworkServices:\r\n")
                            network_services = plist["NetworkServices"].keys()
                            for service_key in network_services:
                                of.write("\tService Key: {0}\r\n".format(service_key))
                                
                                if "DNS" in plist["NetworkServices"][service_key]:
                                    if len(plist["NetworkServices"][service_key]["DNS"]) == 0:
                                        of.write("\t\tDNS: No DNS data.\r\n")
                                    else:
                                        of.write("\t\tDNS: {0}\r\n"
                                                 .format(plist["NetworkServices"][service_key]["DNS"]))
                                
                                if "IPv4" in plist["NetworkServices"][service_key]:
                                    if len(plist["NetworkServices"][service_key]["IPv4"]) == 0:
                                        of.write("\t\tIPv4: No IPv4 data.\r\n")
                                    else:
                                        of.write("\t\tIPv4: {0}\r\n"
                                                 .format(plist["NetworkServices"][service_key]["IPv4"]["ConfigMethod"]))

                                if "IPv6" in plist["NetworkServices"][service_key]:
                                    if len(plist["NetworkServices"][service_key]["IPv6"]) == 0:
                                        of.write("\t\tIPv6: No IPv6 data.\r\n")
                                    else:
                                        of.write("\t\tIPv6: {0}\r\n"
                                                 .format(plist["NetworkServices"][service_key]["IPv6"]["ConfigMethod"]))
                                        
                                if "Interface" in plist["NetworkServices"][service_key]:
                                    if len(plist["NetworkServices"][service_key]["Interface"]) == 0:
                                        of.write("\t\tInterface: No Interface data.\r\n")
                                    else:
                                        of.write("\t\tInterface:\r\n")
                                        of.write("\t\t\tDeviceName       : {0}\r\n"
                                                 .format(
                                                     plist["NetworkServices"][service_key]["Interface"]["DeviceName"]))
                                        of.write("\t\t\tHardware         : {0}\r\n"
                                                 .format(
                                                     plist["NetworkServices"][service_key]["Interface"]["Hardware"]))
                                        of.write("\t\t\tType             : {0}\r\n"
                                                 .format(plist["NetworkServices"][service_key]["Interface"]["Type"]))
                                        of.write("\t\t\tUser Defined Name: {0}\r\n"
                                                 .format(
                                                    plist["NetworkServices"][service_key]
                                                    ["Interface"]["UserDefinedName"]))
                                        
                                if "Proxies" in plist["NetworkServices"][service_key]:
                                    if len(plist["NetworkServices"][service_key]["Proxies"]) == 0:
                                        of.write("\t\tProxies: No Proxies data.\r\n")
                                    else:
                                        of.write("\t\tProxies:\r\n")
                                        if "ExceptionsList" in plist["NetworkServices"][service_key]["Proxies"]:
                                            for proxy_exception in \
                                                    plist["NetworkServices"][service_key]["Proxies"]["ExceptionsList"]:
                                                of.write("\t\t\tException: {0}\r\n".format(proxy_exception))
                                        of.write("\t\t\tFTP Passive: {0}\r\n"
                                                 .format(
                                                     plist["NetworkServices"][service_key]["Proxies"]["FTPPassive"]))
                                        
                                if "SMB" in plist["NetworkServices"][service_key]:
                                    if len(plist["NetworkServices"][service_key]["SMB"]) == 0:
                                        of.write("\t\tSMB: No SMB data.\r\n")
                                    else:
                                        of.write("\t\tSMB: {0}\r\n"
                                                 .format(plist["NetworkServices"][service_key]["SMB"]))
                                
                                if "UserDefinedName" in plist["NetworkServices"][service_key]:
                                    of.write("\t\t\tUserDefinedName: {0}\r\n"
                                             .format(plist["NetworkServices"][service_key]["UserDefinedName"]))
                                
                                of.write("\r\n")
                            # END SERVICES LOOP
                            
                        if "Sets" in plist:
                            of.write("Sets:\r\n")
                            network_sets = plist["Sets"]
                            for network_set in network_sets:
                                if "Network" in plist["Sets"][network_set]:
                                    of.write("\tGlobal:\r\n")
                                    if "IPv4" in plist["Sets"][network_set]["Network"]["Global"]:
                                        of.write("\t\tIPv4 Service Order:\r\n")
                                        for item in \
                                                plist["Sets"][network_set]["Network"]["Global"]["IPv4"]["ServiceOrder"]:
                                            of.write("\t\t\tService: {0}\r\n".format(item))
                                    if "Interface" in plist["Sets"][network_set]["Network"]:
                                        keys = plist["Sets"][network_set]["Network"].keys()
                                        for key in keys:
                                            if key == "Interface":
                                                interface_dict = plist["Sets"][network_set]["Network"][key]
                                                of.write("\tInterface:\r\n")
                                                for interface_key in interface_dict:
                                                    of.write("\t\tInterface Name: {0}\r\n".format(interface_key))
                                                    ik_dict = interface_dict[interface_key]
                                                    for ik_key in ik_dict:
                                                        of.write("\t\tType: {0}\r\n".format(ik_key))
                                                        join_mode = ik_dict.get(ik_key).get("JoinModeFallback")
                                                        for item in join_mode:
                                                            of.write("\t\t\tJoin Mode Fallback      : {0}\r\n"
                                                                     .format(item))
                                                        of.write("\t\t\tPower Enabled           : {0}\r\n"
                                                                 .format(ik_dict.get(ik_key).get("PowerEnabled")))
                                                        of.write("\t\t\tRemember Joined Networks: {0}\r\n"
                                                                 .format(ik_dict.get(ik_key)
                                                                         .get("RememberJoinedNetworks")))
                                                        of.write("\t\t\tVersion                 : {0}\r\n"
                                                                 .format(ik_dict.get(ik_key).get("Version")))
                                                        of.write("\r\n")
                                            if key == "Service":
                                                of.write("\tService:\r\n")
                                                for service_key in plist["Sets"][network_set]["Network"][key]:
                                                    of.write("\t\t{0}\r\n".format(service_key))
                                                    of.write("\t\t\tLink: {0}\r\n"
                                                             .format(
                                                                plist["Sets"][network_set]["Network"][key]
                                                                .get(service_key).get("__LINK__")))
                                                of.write("\r\n")
                                if "UserDefinedName" in plist["Sets"][network_set]:
                                    of.write("\tUserDefinedName: {0}\r\n"
                                             .format(plist["Sets"][network_set]["UserDefinedName"]))
                                    of.write("\r\n")
                        
                        if "System" in plist:
                            of.write("System:\r\n")
                            of.write("\tLocal Host Name: {0}\r\n"
                                     .format(plist["System"]["Network"]["HostNames"]["LocalHostName"]))
                            of.write("\tComputer Name: {0}\r\n"
                                     .format(plist["System"]["System"]["ComputerName"]))
                            of.write("\tComputer Name: {0}\r\n"
                                     .format(plist["System"]["System"]["ComputerNameEncoding"]))
                            of.write("\r\n")
                            
                        if "VirtualNetworkInterfaces" in plist:
                            of.write("Virtual Network Interfaces:\r\n")
                            for vni_key in plist["VirtualNetworkInterfaces"]:
                                of.write("\t{0}\r\n".format(vni_key))  # Bridge
                                vni_dict = plist["VirtualNetworkInterfaces"][vni_key]
                                of.write("\t\t{0}\r\n".format(vni_dict))
                                    
                        of.write("\r\n")
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))

            elif self._os_version == "snow_leopard":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "CurrentSet" in plist:
                            of.write("Current Set: {0}\r\n".format(plist["CurrentSet"]))
                        of.write("Network Services:\r\n")
                        network_services = plist["NetworkServices"]
                        for network_service_name in network_services:
                            of.write("Network Service Name: {0}\r\n".format(network_service_name))
                            network_service = network_services[network_service_name]
                            if "DNS" in network_service:
                                of.write("\tDNS              : {0}\r\n".format(str(network_service["DNS"])))
                            if "IPv4" in network_service:
                                of.write("\tIPv4             : {0}\r\n".format(network_service["IPv4"]["ConfigMethod"]))
                            if "IPv6" in network_service:
                                of.write("\tIPv6             : {0}\r\n".format(network_service["IPv6"]["ConfigMethod"]))
                            if "Interface" in network_service:
                                of.write("\tInterface:\r\n")
                                of.write("\t\tDevice Name      : {0}\r\n"
                                         .format(network_service["Interface"]["DeviceName"]))
                                of.write("\t\tHardware         : {0}\r\n"
                                         .format(network_service["Interface"]["Hardware"]))
                                of.write("\t\tType             : {0}\r\n".format(network_service["Interface"]["Type"]))
                                of.write("\t\tUser Defined Name: {0}\r\n"
                                         .format(network_service["Interface"]["UserDefinedName"]))
                            if "Proxies" in network_service:
                                proxies = network_service["Proxies"]
                                if "ExceptionsList" in proxies:
                                    of.write("\tExceptions List:\r\n")
                                    for proxy_exception in proxies["ExceptionsList"]:
                                        of.write("\t\t{0}\r\n".format(proxy_exception))
                                if "FTPPassive" in proxies:
                                    of.write("\tFTP Passive: {0}\r\n".format(proxies["FTPPassive"]))
                            if "SMB" in network_service:
                                of.write("\tSMB              : {0}\r\n".format(str(network_service["SMB"])))
                            if "AppleTalk" in network_service:
                                of.write("\tApple Talk       : {0}\r\n".format(str(network_service["AppleTalk"])))
                            if "UserDefinedName" in network_service:
                                of.write("\tUser Defined Name: {0}\r\n".format(network_service["UserDefinedName"]))
                            if "Modem" in network_service:
                                modem = network_service["Modem"]
                                of.write("\tModem\r\n")
                                if "ConnectionPersonality" in modem:
                                    of.write("\t\tConnection Personality : {0}\r\n"
                                             .format(modem["ConnectionPersonality"]))
                                if "ConnectionScript" in modem:
                                    of.write("\t\tConnection Script      : {0}\r\n".format(modem["ConnectionScript"]))
                                if "DataCompression" in modem:
                                    of.write("\t\tData Compression       : {0}\r\n".format(modem["DataCompression"]))
                                if "DeviceModel" in modem:
                                    of.write("\t\tDevice Model           : {0}\r\n".format(modem["DeviceModel"]))
                                if "DeviceVendor" in modem:
                                    of.write("\t\tDevice Vendor          : {0}\r\n".format(modem["DeviceVendor"]))
                                if "DialMode" in modem:
                                    of.write("\t\tDial Mode              : {0}\r\n".format(modem["DialMode"]))
                                if "ErrorCorrection" in modem:
                                    of.write("\t\tError Correction       : {0}\r\n".format(modem["ErrorCorrection"]))
                                if "PulseDial" in modem:
                                    of.write("\t\tPulse Dial             : {0}\r\n".format(modem["PulseDial"]))
                                if "Speaker" in modem:
                                    of.write("\t\tSpeaker                : {0}\r\n".format(modem["Speaker"]))
                            if "PPP" in network_service:
                                ppp = network_service["PPP"]
                                of.write("\tPPP\r\n")
                                if "ACSPEnabled" in ppp:
                                    of.write("\t\tACSP Enabled                  : {0}\r\n".format(ppp["ACSPEnabled"]))
                                if "CommDisplayTerminalWindow" in ppp:
                                    of.write("\t\tComm Display Terminal Window  : {0}\r\n"
                                             .format(ppp["CommDisplayTerminalWindow"]))
                                if "CommRedialCount" in ppp:
                                    of.write("\t\tComm Redial Count             : {0}\r\n"
                                             .format(ppp["CommRedialCount"]))
                                if "CommRedialEnabled" in ppp:
                                    of.write("\t\tComm Redial Enabled           : {0}\r\n"
                                             .format(ppp["CommRedialEnabled"]))
                                if "CommRedialInterval" in ppp:
                                    of.write("\t\tComm Redial Interval          : {0}\r\n"
                                             .format(ppp["CommRedialInterval"]))
                                if "CommUseTerminalScript" in ppp:
                                    of.write("\t\tComm Use Terminal Script      : {0}\r\n"
                                             .format(ppp["CommUseTerminalScript"]))
                                if "DialOnDemand" in ppp:
                                    of.write("\t\tDial On Demand                : {0}\r\n"
                                             .format(ppp["DialOnDemand"]))
                                if "DisconnectOnFastUserSwitch" in ppp:
                                    of.write("\t\tDisconnect On Fast User Switch: {0}\r\n"
                                             .format(ppp["DisconnectOnFastUserSwitch"]))
                                if "DisconnectOnIdle" in ppp:
                                    of.write("\t\tDisconnect On Idle            : {0}\r\n"
                                             .format(ppp["DisconnectOnIdle"]))
                                if "DisconnectOnIdleTimer" in ppp:
                                    of.write("\t\tDisconnect On Idle Timer      : {0}\r\n"
                                             .format(ppp["DisconnectOnIdleTimer"]))
                                if "DisconnectOnLogout" in ppp:
                                    of.write("\t\tDisconnect On Logout          : {0}\r\n"
                                             .format(ppp["DisconnectOnLogout"]))
                                if "DisconnectOnSleep" in ppp:
                                    of.write("\t\tDisconnect On Sleep           : {0}\r\n"
                                             .format(ppp["DisconnectOnSleep"]))
                                if "IPCPCompressionVJ" in ppp:
                                    of.write("\t\tIPCP Compression VJ           : {0}\r\n"
                                             .format(ppp["IPCPCompressionVJ"]))
                                if "IdleReminder" in ppp:
                                    of.write("\t\tIdle Reminder                 : {0}\r\n"
                                             .format(ppp["IdleReminder"]))
                                if "IdleReminderTimer" in ppp:
                                    of.write("\t\tIdle Reminder Timer           : {0}\r\n"
                                             .format(ppp["IdleReminderTimer"]))
                                if "LCPEchoEnabled" in ppp:
                                    of.write("\t\tLCP Echo Enabled              : {0}\r\n"
                                             .format(ppp["LCPEchoEnabled"]))
                                if "LCPEchoFailure" in ppp:
                                    of.write("\t\tLCP Echo Failure              : {0}\r\n"
                                             .format(ppp["LCPEchoFailure"]))
                                if "LCPEchoInterval" in ppp:
                                    of.write("\t\tLCP Echo Interval             : {0}\r\n"
                                             .format(ppp["LCPEchoInterval"]))
                                if "Logfile" in ppp:
                                    of.write("\t\tLogfile                       : {0}\r\n"
                                             .format(ppp["Logfile"]))
                                if "VerboseLogging" in ppp:
                                    of.write("\t\tVerbose Logging               : {0}\r\n"
                                             .format(ppp["VerboseLogging"]))
                            of.write("\r\n")
                        of.write("Sets:\r\n")
                        for network_set_name in plist["Sets"]:
                            of.write("\tNetwork Set: {0}\r\n".format(network_set_name))
                            network_set = plist["Sets"][network_set_name]
                            if "Network" in network_set:
                                network = network_set["Network"]
                                if "Global" in network:
                                    of.write("\t\tGlobal   : {0}\r\n".format(network["Global"]))
                                if "Interface" in network:
                                    of.write("\t\tInterface: {0}\r\n".format(network["Interface"]))
                                if "Service" in network:
                                    of.write("\t\tService  : {0}\r\n".format(network["Service"]))
                            if "UserDefinedName" in network_set:
                                of.write("\t\tUser Defined Name : {0}\r\n".format(network_set["UserDefinedName"]))
                            of.write("\r\n")
                        of.write("System:\r\n")
                        if "System" in plist["System"]:
                            if "ComputerName" in plist["System"]["System"]:
                                of.write("\tComputer Name          : {0}\r\n"
                                         .format(plist["System"]["System"]["ComputerName"]))
                            if "ComputerNameEncoding" in plist["System"]["System"]:
                                of.write("\tComputer Name Encoding : {0}\r\n"
                                         .format(plist["System"]["System"]["ComputerNameEncoding"]))
                        if "Network" in plist["System"]:
                            if "HostNames" in plist["System"]["Network"]:
                                of.write("\tLocalhost Name         : {0}\r\n"
                                         .format(plist["System"]["Network"]["HostNames"]["LocalHostName"]))

                        of.write("\r\n")
                        pass

                    except KeyError:
                        pass
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
