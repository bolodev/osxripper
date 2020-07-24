""" Module to parse information from CyberGhost log """
import codecs
import logging
import os
from riplib.plugin import Plugin

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersCyberGhostLogs(Plugin):
    """
    Parse information from /Users/{username}/Library/Application Support/CyberGhost {version}
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Cyber Ghost VPN Logs")
        self.set_description("Parse information from /Users/{username}/Library/Application Support/CyberGhost {version}")
        self.set_data_file("")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("multiple")

    def parse(self):
        """
        Scan for the plist
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    config = os.path.join(users_path, username, "Library", "Application Support")
                    if os.path.isdir(config):
                        self.__read_logs(config, username)
                    else:
                        logging.warning("%s does not exist.", config)
                        print("[WARNING] {0} does not exist.".format(config))
        else:
            print("[WARNING] {0} does not exist.".format(users_path))

    def __read_logs(self, file, username):
        """
        Parse /Users/{username}/Library/Application Support/CyberGhost {version}
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_VPN_CyberGhost.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            app_support_dir = os.listdir(file)
            for directory in app_support_dir:
                if "CyberGhost" in directory:
                    ghost_dir = os.path.join(file, directory)
                    output_file.write("Source Directory: {0}\r\n\r\n".format(ghost_dir))
                    ghost_dir_list = os.listdir(ghost_dir)
                    for ghost_file in ghost_dir_list:
                        if ghost_file == "CyberGhostMacLog.log":
                            output_file.write("="*10 + " " + ghost_file + " " + "="*10 + "\r\n")
                            with open(os.path.join(ghost_dir, ghost_file), "r") as mac_log:
                                for line in mac_log.readlines():
                                    output_file.write("{0}\r\n".format(line))
                            mac_log.close()
                            output_file.write("\r\n")
                        if ghost_file == "CyberGhostMacLogScripts.log":
                            output_file.write("="*10 + " " + ghost_file + " " + "="*10 + "\r\n")
                            with open(os.path.join(ghost_dir, ghost_file), "r") as scripts_log:
                                for line in scripts_log.readlines():
                                    output_file.write("{0}\r\n".format(line))
                            scripts_log.close()
                            output_file.write("\r\n")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
