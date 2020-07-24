""" Mdule to parse CyberGhost plist """
import codecs
import datetime
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


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
        self.set_name("User Cyber Ghost VPN Configuration")
        self.set_description("Parse information from /Users/{username}/Library/Preferences/com.cyberghostsrl.cyberghostmac.plist")
        self.set_data_file("com.cyberghostsrl.cyberghostmac.plist")
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
        Parse /Users/{username}/Library/Preferences/com.cyberghostsrl.cyberghostmac.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_VPN_CyberGhost.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                plist = riplib.ccl_bplist.load(bplist)
                bplist.close()
                try:
                    if "Cyberghost_GUID" in plist:
                        output_file.write("Cyberghost GUID      : {0}\r\n".format(plist["Cyberghost_GUID"]))
                    if "startAtSystemStart" in plist:
                        output_file.write("Start at System Start: {0}\r\n".format(plist["startAtSystemStart"]))
                    if "SULastCheckTime" in plist:
                        output_file.write("SU Last Check Time   : {0}\r\n".format(plist["SULastCheckTime"]))
                    if "RandomPort" in plist:
                        output_file.write("Random Port          : {0}\r\n".format(plist["RandomPort"]))
                    if "useOpenVpnOverTcp" in plist:
                        output_file.write("Use OpenVpn Over Tcp : {0}\r\n".format(plist["useOpenVpnOverTcp"]))
                    if "Cyberghost_RemoteSettings" in plist:
                        output_file.write("Cyberghost Remote Settings:\r\n")
                        remote_settings = plist["Cyberghost_RemoteSettings"]
                        # instdate -> Unix Millisecond
                        date_foo = remote_settings["instdate"]
                        date_foo = datetime.datetime.fromtimestamp(date_foo/1000.0)
                        output_file.write("\tInstall Date           : {0}\r\n".format(date_foo))
                        output_file.write("\tLast Country           : {0}\r\n".format(remote_settings["LastCountry"]))
                        output_file.write("\tLast Server            : {0}\r\n".format(remote_settings["LastServer"]))
                        output_file.write("\tLast Logged In         : {0}\r\n".format(remote_settings["LastLoggedIn"]))
                        output_file.write("\tLas tPlan ID           : {0}\r\n".format(remote_settings["LastPlanID"]))
                        output_file.write("\tENC Connected Server ID: {0}\r\n".format(remote_settings["ENC_ConnectedServerID"]))
                        output_file.write("\tLast Plan Name         : {0}\r\n".format(remote_settings["LastPlanName"]))
                        output_file.write("\tStart Counter          : {0}\r\n".format(remote_settings["startCounter"]))
                except KeyError:
                    pass
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
