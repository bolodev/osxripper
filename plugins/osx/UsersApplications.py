from riplib.Plugin import Plugin
import codecs
import logging
import os

__author__ = 'bolodev'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersApplications(Plugin):
    """
    List .app folders in users' home folder
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Applications"
        self._description = "List applications in users' folders"
        self._data_file = ""
        self._output_file = ""
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
                    user_dir = os.path.join(users_path, username)
                    if os.path.isdir(user_dir):
                        self.__list_files(user_dir, username)
                    else:
                        logging.warning("{0} does not exist.".format(user_dir))
                        print("[WARNING] {0} does not exist.".format(user_dir))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))
            
    def __list_files(self, file, username):
        """
        List .app directories
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + '_Applications.txt'), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source Directory: {0}\r\n\r\n".format(file))
            for root, dirs, files in os.walk(file):
                for user_dir in dirs:
                    if user_dir.endswith(".app"):
                        of.write("{0}{1}{2}\r\n".format(root, os.path.sep, user_dir, sep=""))

            of.write("="*40 + "\r\n\r\n")
        of.close()
