""" Module to parse information from /Users/username/.bash_history """
import codecs
import logging
import os
from riplib.plugin import Plugin


__author__ = 'osxripper - mykulh'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersBashHistory(Plugin):
    """
    Parse information from /Users/username/.bash_history
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Console History")
        self.set_description("Parse information from /Users/username/.bash_history file")
        self.set_data_file(".bash_history")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("file")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
        else:
            print("[WARNING] {0} does not exist.".format(users_path))
            return
        for username in user_list:
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                if os.path.isdir(users_path):
                    # user_list = os.listdir(users_path)
                    if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                        sessions = os.path.join(users_path, username, ".bash_sessions")
                        if os.path.isdir(sessions):
                            self.__parse_bash_sessions(username, sessions)
            if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                history = os.path.join(users_path, username, self._data_file)
                if os.path.isfile(history):
                    self.__parse_history(history, username)
                else:
                    logging.warning("%s does not exist.", history)
                    print("[WARNING] {0} does not exist.".format(history))

    def __parse_bash_sessions(self, username, sessions_dir):
        """
        Read /Users/username/.bash_sessions/*
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as output_file:
            output_file.write("=" * 10 + " " + self._name + " " + "=" * 10 + "\r\n")
            output_file.write("Bash Sessions\r\n")
            sessions_files = os.listdir(sessions_dir)
            for session_file in sessions_files:
                if ".session" in session_file:
                    s_file = codecs.open(os.path.join(sessions_dir, session_file), "r", encoding="utf-8")
                    for lines in s_file:
                        output_file.write(lines.replace("\n", "\r\n"))
                    s_file.close()
                if ".historynew" in session_file:
                    s_file = codecs.open(os.path.join(sessions_dir, session_file), "r", encoding="utf-8")
                    for lines in s_file:
                        output_file.write(lines.replace("\n", "\r\n"))
                    s_file.close()
                output_file.write("=" * 10 + "\r\n")

    def __parse_history(self, file, username):
        """
        Parse /Users/username/.bash_history
        N.B. OSX version checking removed as this is a common directory and file across versions
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as output_file:
            output_file.write("=" * 10 + " " + self._name + " " + "=" * 10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                history_file = codecs.open(file, "r", encoding="utf-8")
                for lines in history_file:
                    output_file.write(lines.replace("\n", "\r\n"))
                history_file.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            output_file.write("=" * 40 + "\r\n\r\n")
        output_file.close()
