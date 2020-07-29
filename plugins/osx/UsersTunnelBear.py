""" Module to parse TunnelBear plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'bolodev'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersTunnelBear(Plugin):
    """
    Parse information from /Users/{username}/Library/Preferences/com.tunnelbear.mac.TunnelBear.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Tunnelbear VPN Configuration")
        self.set_description("Parse information from /Users/{username}/Library/Preferences/com.tunnelbear.mac.TunnelBear.plist file")
        self.set_data_file("com.tunnelbear.mac.TunnelBear.plist")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("bplist")

    def parse(self):
        """
        Scan for the plist
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    config = os.path.join(users_path, username, "Library", "Preferences", self._data_file)
                    if os.path.isfile(config):
                        self.__parse_plist(config, username)
                    else:
                        logging.warning("%s does not exist.", config)
                        print("[WARNING] {0} does not exist.".format(config))
        else:
            print("[WARNING] {0} does not exist.".format(users_path))

    def __parse_plist(self, file, username):
        """
        Parse /Users/{username}/Library/Preferences/com.tunnelbear.mac.TunnelBear.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_VPN_TunnelBear.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                plist = riplib.ccl_bplist.load(bplist)
                bplist.close()
                try:
                    if "username" in plist:
                        output_file.write("Username                            : {0}\r\n".format(plist["username"]))
                    if "previousUsername" in plist:
                        output_file.write("Previous Username                   : {0}\r\n".format(plist["previousUsername"]))
                    if "accountVerified" in plist:
                        output_file.write("Account Verified                    : {0}\r\n".format(plist["accountVerified"]))
                    if "paymentStatus" in plist:
                        output_file.write("Payment Status                      : {0}\r\n".format(plist["paymentStatus"]))
                    if "SULastCheckTime" in plist:
                        output_file.write("SU Last Check Time                  : {0}\r\n".format(plist["SULastCheckTime"]))
                    if "SUEnableAutomaticChecks" in plist:
                        output_file.write("SU Enable Automatic Checks          : {0}\r\n".format(plist["SUEnableAutomaticChecks"]))
                    if "uuid" in plist:
                        output_file.write("UUID                                : {0}\r\n".format(plist["uuid"]))
                    if "vpnToken" in plist:
                        output_file.write("VPN Token                           : {0}\r\n".format(plist["vpnToken"]))
                    if "grizzly" in plist:
                        output_file.write("Grizzly                             : {0}\r\n".format(plist["grizzly"]))
                    if "fullRemainingTime" in plist:
                        output_file.write("Full Remaining Time                 : {0}\r\n".format(plist["fullRemainingTime"]))
                    if "currentCountry" in plist:
                        output_file.write("Current Country                     : {0}\r\n".format(plist["currentCountry"]))
                    if "vpnNumSuccessfulTCPConnections" in plist:
                        output_file.write("VPN Num. Successful TCP Connections : {0}\r\n".format(plist["vpnNumSuccessfulTCPConnections"]))
                    if "shouldReconnect" in plist:
                        output_file.write("Should Reconnect                    : {0}\r\n".format(plist["shouldReconnect"]))
                    if "vpnServers" in plist:
                        output_file.write("VPN Servers:\r\n")
                        vpn_servers = plist["vpnServers"]
                        for vpn_server in vpn_servers:
                            output_file.write("\tHost  : {0}\r\n".format(vpn_server["host"]))
                            output_file.write("\tPort  : {0}\r\n".format(vpn_server["port"]))
                            output_file.write("\tIs UDP: {0}\r\n".format(vpn_server["isUdp"]))
                            output_file.write("\r\n")
                    if "maxBandwidth" in plist:
                        output_file.write("Max Bandwidth                       : {0}\r\n".format(plist["maxBandwidth"]))
                    if "SUHasLaunchedBefore" in plist:
                        output_file.write("Has Launched Before                 : {0}\r\n".format(plist["SUHasLaunchedBefore"]))
                    if "countries" in plist:
                        output_file.write("Countries:\r\n")
                        countries = plist["countries"]
                        for country in countries:
                            output_file.write("\tID  : {0}\r\n".format(country["id"]))
                            output_file.write("\tCode: {0}\r\n".format(country["code"]))
                            output_file.write("\r\n")
                    if "lastVersionRun" in plist:
                        output_file.write("Last Version Run                    : {0}\r\n".format(plist["lastVersionRun"]))
                    if "fullVersion" in plist:
                        output_file.write("Full Version                        : {0}\r\n".format(plist["fullVersion"]))
                    if "vigilantMode" in plist:
                        output_file.write("Vigilant Mode                       : {0}\r\n".format(plist["vigilantMode"]))
                    if "privacyEnabled" in plist:
                        output_file.write("Privacy Enabled                     : {0}\r\n".format(plist["privacyEnabled"]))
                    if "notificationsEnabled" in plist:
                        output_file.write("Notifications Enabled               : {0}\r\n".format(plist["notificationsEnabled"]))
                    if "dockIconEnabled" in plist:
                        output_file.write("Dock Icon Enabled                   : {0}\r\n".format(plist["dockIconEnabled"]))
                    if "privacyFacebookEnabled" in plist:
                        output_file.write("Privacy Facebook Enabled            : {0}\r\n".format(plist["privacyFacebookEnabled"]))
                    if "privacyLinkedinEnabled" in plist:
                        output_file.write("Privacy Linkedin Enabled            : {0}\r\n".format(plist["privacyLinkedinEnabled"]))
                    if "privacyTwitterEnabled" in plist:
                        output_file.write("Privacy Twitter Enabled             : {0}\r\n".format(plist["privacyTwitterEnabled"]))
                except KeyError:
                    pass
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
