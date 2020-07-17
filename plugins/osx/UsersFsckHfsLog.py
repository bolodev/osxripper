from riplib.plugin import Plugin
import codecs
import logging
import os

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersFsckHfsLog(Plugin):
    """
    Plugin to read /Users/username/Library/Logs/fsck_hfs.log
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User FS Check HFS Log"
        self._description = "Read /Users/username/Library/Logs/fsck_hfs.log"
        self._data_file = "fsck_hfs.log"
        self._output_file = ""
        self._type = "text"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories and read /Users/username/Library/Logs/fsck_hfs.log
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    fsck_log = os.path.join(users_path, username, "Library", "Logs", self._data_file)
                    if os.path.isfile(fsck_log):
                        self.__read_fsck_hfs_log(fsck_log, username)
                    else:
                        logging.warning("{0} does not exist.".format(fsck_log))
                        print("[WARNING] {0} does not exist.".format(fsck_log))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))
        
    def __read_fsck_hfs_log(self, file, username):
        """
        Read the fsck_hfs.log file
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                with codecs.open(file, "r", encoding="utf-8") as fsck:
                    for line in fsck.readlines():
                        # fsck_hfs started
                        if "fsck_hfs started" in line:
                            of.write(line + "\r\n")
                        # The volume
                        if "The volume" in line:
                            of.write(line + "\r\n")
                        # fsck_hfs completed
                        if "fsck_hfs completed" in line:
                            of.write(line + "\r\n")
                fsck.close()
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n")
        of.close()
