""" Module to parse TrueCrypt configuration xml file """
import codecs
import logging
import os
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersTrueCrypt(Plugin):
    """
    Parse information from /Users/{username}/Library/Application Support/TrueCrypt/Configuration.xml
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("TrueCrypt Configuration File")
        self.set_description("Parse information from /Users/{username}/Library/Application Support/TrueCrypt/Configuration.xml file")
        self.set_data_file("Configuration.xml")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("text")

    def parse(self):
        """
        Find the xml file
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    config = os.path\
                        .join(users_path, username, "Library", "Application Support", "TrueCrypt", self._data_file)
                    if os.path.isfile(config):
                        self.__parse_config(config, username)
                    else:
                        logging.warning("%s does not exist.", config)
                        print("[WARNING] {0} does not exist.".format(config))
        else:
            print("[WARNING] {0} does not exist.".format(users_path))

    def __parse_config(self, file, username):
        """
        /Users/{username}/Library/Application Support/TrueCrypt/Configuration.xml
        N.B. OSX version checking removed as this is a common directory and file across versions
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_TrueCrypt_config.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                config_file = codecs.open(file, "r", encoding="utf-8")
                for lines in config_file:
                    output_file.write(lines.replace("\n", "\r\n"))
                config_file.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
