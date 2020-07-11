from riplib.Plugin import Plugin
import codecs
import logging
import os

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersDiskUtilityLog(Plugin):
    """
    Plugin to read /Users/username/Library/Logs/DiskUtility.log
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Disk Utility Log"
        self._description = "Read /Users/username/Library/Logs/DiskUtility.log"
        self._data_file = "DiskUtility.log"
        self._output_file = ""
        self._type = "text"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories and
        read /Users/username/Library/Logs/DiskUtility.log
        """
        users_path = os.path.join(self._input_dir, "Users")
        # username = None
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    du_log = os.path.join(users_path, username, "Library", "Logs", self._data_file)
                    if os.path.isfile(du_log):
                        self.__read_disk_util_log(du_log, username)
                    else:
                        logging.warning("{0} does not exist.".format(users_path))
                        print("[WARNING] {0} does not exist.".format(users_path))

    def __read_disk_util_log(self, file, username):
        """
        Read the DiskUtility.log
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                with codecs.open(file, "r", encoding="utf-8") as du:
                    for line in du.readlines():
                        if "**" not in line and len(line) != 0:
                            of.write(line.replace("\n", "\r\n"))
                du.close()
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
