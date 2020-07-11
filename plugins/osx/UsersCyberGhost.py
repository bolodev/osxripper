from riplib.Plugin import Plugin
import riplib.ccl_bplist
import codecs
import datetime
import logging
import os

__author__ = 'bolodev'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersCyberGhost(Plugin):
    """
    Parse information from /Users/{username}/Library/Preferences/com.cyberghostsrl.cyberghostmac.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Cyber Ghost VPN Configuration"
        self._description = "Parse information from " \
                            "/Users/{username}/Library/Preferences/com.cyberghostsrl.cyberghostmac.plist"
        self._data_file = "com.cyberghostsrl.cyberghostmac.plist"
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
        Parse /Users/{username}/Library/Preferences/com.cyberghostsrl.cyberghostmac.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_VPN_CyberGhost.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                pl = riplib.ccl_bplist.load(bplist)
                bplist.close()
                try:
                    if "Cyberghost_GUID" in pl:
                        of.write("Cyberghost GUID      : {0}\r\n".format(pl["Cyberghost_GUID"]))
                    if "startAtSystemStart" in pl:
                        of.write("Start at System Start: {0}\r\n".format(pl["startAtSystemStart"]))
                    if "SULastCheckTime" in pl:
                        of.write("SU Last Check Time   : {0}\r\n".format(pl["SULastCheckTime"]))
                    if "RandomPort" in pl:
                        of.write("Random Port          : {0}\r\n".format(pl["RandomPort"]))
                    if "useOpenVpnOverTcp" in pl:
                        of.write("Use OpenVpn Over Tcp : {0}\r\n".format(pl["useOpenVpnOverTcp"]))
                    if "Cyberghost_RemoteSettings" in pl:
                        of.write("Cyberghost Remote Settings:\r\n")
                        remote_settings = pl["Cyberghost_RemoteSettings"]
                        # instdate -> Unix Millisecond
                        date_foo = remote_settings["instdate"]
                        date_foo = datetime.datetime.fromtimestamp(date_foo/1000.0)
                        of.write("\tInstall Date           : {0}\r\n".format(date_foo))
                        of.write("\tLast Country           : {0}\r\n".format(remote_settings["LastCountry"]))
                        of.write("\tLast Server            : {0}\r\n".format(remote_settings["LastServer"]))
                        of.write("\tLast Logged In         : {0}\r\n".format(remote_settings["LastLoggedIn"]))
                        of.write("\tLas tPlan ID           : {0}\r\n".format(remote_settings["LastPlanID"]))
                        of.write("\tENC Connected Server ID: {0}\r\n".format(remote_settings["ENC_ConnectedServerID"]))
                        of.write("\tLast Plan Name         : {0}\r\n".format(remote_settings["LastPlanName"]))
                        of.write("\tStart Counter          : {0}\r\n".format(remote_settings["startCounter"]))
                except KeyError:
                    pass
            else:
                logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            of.write("="*40 + "\r\n\r\n")
        of.close()
