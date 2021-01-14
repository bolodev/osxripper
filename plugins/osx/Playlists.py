""" Module to list playlist files under /private/var/db/BootCaches """
import codecs
import logging
import os
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class Playlists(Plugin):
    """
    Plugin to list playlist files under /private/var/db/BootCaches
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Playlists")
        self.set_description("List files in /private/var/db/BootCaches")
        self.set_data_file("")  # listing directories so this is not needed
        self.set_output_file("Playlists.txt")
        self.set_type("dir_list")

    def parse(self):
        """
        List .playlist files under /private/var/db/BootCaches
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion"]:
                working_dir = os.path.join(self._input_dir, "private", "var", "db", "BootCaches")
                output_file.write("Source Directory: {0}\r\n\r\n".format(working_dir))
                if os.path.isdir(working_dir):
                    file_listing = os.listdir(working_dir)
                    for file_name in file_listing:
                        test_file = os.path.join(working_dir, file_name)
                        if os.path.isdir(test_file):
                            output_file.write("Generated User ID: {0}\r\n".format(file_name))
                            user_playlists = os.listdir(test_file)
                            for user_file in user_playlists:
                                output_file.write("\t{0}\r\n".format(user_file))
                            output_file.write("\r\n")
                else:
                    logging.warning("Directory: %s does not exist or cannot be found.\r\n", working_dir)
                    output_file.write("[WARNING] Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
                    print("[WARNING] Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
