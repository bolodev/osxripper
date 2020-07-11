from riplib.Plugin import Plugin
import codecs
import logging
import os

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
        self._name = "User Cyber Ghost VPN Logs"
        self._description = "Parse information from /Users/{username}/Library/Application Support/CyberGhost {version}"
        self._data_file = ""
        self._output_file = ""  # this will have to be defined per user account
        self._type = "multiple"
    
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
                        logging.warning("{0} does not exist.".format(config))
                        print("[WARNING] {0} does not exist.".format(config))
        else:
            print("[WARNING] {0} does not exist.".format(users_path))
            
    def __read_logs(self, file, username):
        """
        Parse /Users/{username}/Library/Application Support/CyberGhost {version}
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_VPN_CyberGhost.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            app_support_dir = os.listdir(file)
            for directory in app_support_dir:
                if "CyberGhost" in directory:
                    ghost_dir = os.path.join(file, directory)
                    of.write("Source Directory: {0}\r\n\r\n".format(ghost_dir))
                    ghost_dir_list = os.listdir(ghost_dir)
                    for ghost_file in ghost_dir_list:
                        if ghost_file == "CyberGhostMacLog.log":
                            of.write("="*10 + " " + ghost_file + " " + "="*10 + "\r\n")
                            with open(os.path.join(ghost_dir, ghost_file), "r") as mac_log:
                                for line in mac_log.readlines():
                                    of.write("{0}\r\n".format(line))
                            mac_log.close()
                            of.write("\r\n")
                        if ghost_file == "CyberGhostMacLogScripts.log":
                            of.write("="*10 + " " + ghost_file + " " + "="*10 + "\r\n")
                            with open(os.path.join(ghost_dir, ghost_file), "r") as scripts_log:
                                for line in scripts_log.readlines():
                                    of.write("{0}\r\n".format(line))
                            scripts_log.close()
                            of.write("\r\n")
            of.write("="*40 + "\r\n\r\n")
        of.close()
