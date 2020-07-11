from riplib.Plugin import Plugin
import riplib.ccl_bplist
import codecs
import logging
import os

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
        self._name = "User Tunnelbear VPN Configuration"
        self._description = "Parse information from " \
                            "/Users/{username}/Library/Preferences/com.tunnelbear.mac.TunnelBear.plist file"
        self._data_file = "com.tunnelbear.mac.TunnelBear.plist"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
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
                        logging.warning("{0} does not exist.".format(config))
                        print("[WARNING] {0} does not exist.".format(config))
        else:
            print("[WARNING] {0} does not exist.".format(users_path))
            
    def __parse_plist(self, file, username):
        """
        Parse /Users/{username}/Library/Preferences/com.tunnelbear.mac.TunnelBear.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_VPN_TunnelBear.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                pl = riplib.ccl_bplist.load(bplist)
                bplist.close()
                try:
                    if "username" in pl:
                        of.write("Username                            : {0}\r\n".format(pl["username"]))
                    if "previousUsername" in pl:
                        of.write("Previous Username                   : {0}\r\n".format(pl["previousUsername"]))
                    if "accountVerified" in pl:
                        of.write("Account Verified                    : {0}\r\n".format(pl["accountVerified"]))
                    if "paymentStatus" in pl:
                        of.write("Payment Status                      : {0}\r\n".format(pl["paymentStatus"]))
                    if "SULastCheckTime" in pl:
                        of.write("SU Last Check Time                  : {0}\r\n".format(pl["SULastCheckTime"]))
                    if "SUEnableAutomaticChecks" in pl:
                        of.write("SU Enable Automatic Checks          : {0}\r\n".format(pl["SUEnableAutomaticChecks"]))
                    if "uuid" in pl:
                        of.write("UUID                                : {0}\r\n".format(pl["uuid"]))
                    if "vpnToken" in pl:
                        of.write("VPN Token                           : {0}\r\n".format(pl["vpnToken"]))
                    if "grizzly" in pl:
                        of.write("Grizzly                             : {0}\r\n".format(pl["grizzly"]))
                    if "fullRemainingTime" in pl:
                        of.write("Full Remaining Time                 : {0}\r\n".format(pl["fullRemainingTime"]))
                    if "currentCountry" in pl:
                        of.write("Current Country                     : {0}\r\n".format(pl["currentCountry"]))
                    if "vpnNumSuccessfulTCPConnections" in pl:
                        of.write("VPN Num. Successful TCP Connections : {0}\r\n"
                                 .format(pl["vpnNumSuccessfulTCPConnections"]))
                    if "shouldReconnect" in pl:
                        of.write("Should Reconnect                    : {0}\r\n".format(pl["shouldReconnect"]))
                    if "vpnServers" in pl:
                        of.write("VPN Servers:\r\n")
                        vpn_servers = pl["vpnServers"]
                        for vpn_server in vpn_servers:
                            of.write("\tHost  : {0}\r\n".format(vpn_server["host"]))
                            of.write("\tPort  : {0}\r\n".format(vpn_server["port"]))
                            of.write("\tIs UDP: {0}\r\n".format(vpn_server["isUdp"]))
                            of.write("\r\n")
                    if "maxBandwidth" in pl:
                        of.write("Max Bandwidth                       : {0}\r\n".format(pl["maxBandwidth"]))
                    if "SUHasLaunchedBefore" in pl:
                        of.write("Has Launched Before                 : {0}\r\n".format(pl["SUHasLaunchedBefore"]))
                    if "countries" in pl:
                        of.write("Countries:\r\n")
                        countries = pl["countries"]
                        for country in countries:
                            of.write("\tID  : {0}\r\n".format(country["id"]))
                            of.write("\tCode: {0}\r\n".format(country["code"]))
                            of.write("\r\n")
                    if "lastVersionRun" in pl:
                        of.write("Last Version Run                    : {0}\r\n".format(pl["lastVersionRun"]))
                    if "fullVersion" in pl:
                        of.write("Full Version                        : {0}\r\n".format(pl["fullVersion"]))
                    if "vigilantMode" in pl:
                        of.write("Vigilant Mode                       : {0}\r\n".format(pl["vigilantMode"]))
                    if "privacyEnabled" in pl:
                        of.write("Privacy Enabled                     : {0}\r\n".format(pl["privacyEnabled"]))
                    if "notificationsEnabled" in pl:
                        of.write("Notifications Enabled               : {0}\r\n".format(pl["notificationsEnabled"]))
                    if "dockIconEnabled" in pl:
                        of.write("Dock Icon Enabled                   : {0}\r\n".format(pl["dockIconEnabled"]))
                    if "privacyFacebookEnabled" in pl:
                        of.write("Privacy Facebook Enabled            : {0}\r\n".format(pl["privacyFacebookEnabled"]))
                    if "privacyLinkedinEnabled" in pl:
                        of.write("Privacy Linkedin Enabled            : {0}\r\n".format(pl["privacyLinkedinEnabled"]))
                    if "privacyTwitterEnabled" in pl:
                        of.write("Privacy Twitter Enabled             : {0}\r\n".format(pl["privacyTwitterEnabled"]))
                except KeyError:
                    pass
            else:
                logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            of.write("="*40 + "\r\n\r\n")
        of.close()
