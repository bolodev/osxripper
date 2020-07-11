from riplib.Plugin import Plugin
import codecs
import logging
import os

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersIosBackupList(Plugin):
    """
    List information from /Users/username/Library/Application Support/MobileSync/Backup
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User iOS Backup List"
        self._description = "List of iOS backups present /Users/username/Library/Application Support/MobileSync/Backup"
        self._data_file = ""
        self._output_file = ""  # this will have to be defined per user account
        self._type = "dir_list"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    ios_backup_dir = os.path\
                        .join(users_path, username, "Library", "Application Support", "MobileSync", "Backup")
                    if os.path.isdir(ios_backup_dir):
                        self.__list_files(ios_backup_dir, username)
                    else:
                        logging.info("{0} does not exist.".format(ios_backup_dir))
                        print("[INFO] {0} does not exist.".format(ios_backup_dir))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))
            
    def __list_files(self, file, username):
        """
        List information from /Users/username/Library/Application Support/MobileSync/Backup
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_ios_backup_list.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source Directory: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                dir_listing = os.listdir(file)
                for file_item in dir_listing:
                    of.write("iOS Backup: {0}\r\n".format(file_item))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
