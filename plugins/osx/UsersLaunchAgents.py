""" Module to parse LaunchAgents """
import codecs
import logging
import os
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersLaunchAgents(Plugin):
    """
    List information from /Users/username/Library/LaunchAgents
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User LaunchAgents")
        self.set_description("List launchagents in /Users/username/Library/LaunchAgents")
        self.set_data_file("")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("dir_list")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    launchagents_dir = os.path.join(users_path, username, "Library", "LaunchAgents")
                    if os.path.isdir(launchagents_dir):
                        self.__list_files(launchagents_dir, username)
                    else:
                        logging.warning("%s does not exist.", launchagents_dir)
                        print("[WARNING] {0} does not exist.".format(launchagents_dir))
        else:
            logging.warning("%s does not exist.", users_path)
            print("[WARNING] {0} does not exist.".format(users_path))

    def __list_files(self, file, username):
        """
        List information from /Users/username/Library/LaunchAgents
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source Directory: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                dir_listing = os.listdir(file)
                for launch_agent in dir_listing:
                    output_file.write("\t{0}\r\n".format(launch_agent))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
