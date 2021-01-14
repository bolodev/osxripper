""" Module to parse DiskUtilit log """
import codecs
import logging
import os
from riplib.plugin import Plugin


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
        self.set_name("User Disk Utility Log")
        self.set_description("Read /Users/username/Library/Logs/DiskUtility.log")
        self.set_data_file("DiskUtility.log")
        self.set_output_file("")
        self.set_type("text")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories and
        read /Users/username/Library/Logs/DiskUtility.log
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    du_log = os.path.join(users_path, username, "Library", "Logs", self._data_file)
                    if os.path.isfile(du_log):
                        self.__read_disk_util_log(du_log, username)
                    else:
                        logging.warning("%s does not exist.", users_path)
                        print("[WARNING] {0} does not exist.".format(users_path))

    def __read_disk_util_log(self, file, username):
        """
        Read the DiskUtility.log
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                with codecs.open(file, "r", encoding="utf-8") as du_log:
                    for line in du_log.readlines():
                        if "**" not in line and len(line) != 0:
                            output_file.write(line.replace("\n", "\r\n"))
                du_log.close()
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
