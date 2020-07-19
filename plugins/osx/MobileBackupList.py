""" Module to list contents of /.MobileBackups """
import codecs
import logging
import os
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class MobileBackupList(Plugin):
    """
    Plugin to list contents of /.MobileBackups
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Mobile Backups")
        self.set_description("List extensions in /.MobileBackups")
        self.set_data_file("")  # listing directories so this is not needed
        self.set_output_file("MobileBackups.txt")
        self.set_type("dir_list")

    def parse(self):
        """
        List contents of /.MobileBackups directory
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            mobilebackups_dir = os.path.join(self._input_dir, ".MobileBackups")
            if os.path.isdir(mobilebackups_dir):
                output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                output_file.write("Source Directory: {0}\r\n\r\n".format(mobilebackups_dir))
                file_listing = os.listdir(mobilebackups_dir)
                for file_name in file_listing:
                    output_file.write("\t{0}\r\n".format(file_name))
                    test_path = os.path.join(mobilebackups_dir, file_name)
                    if os.path.isdir(test_path):
                        test_path_file_list = os.listdir(test_path)
                        for test_path_file in test_path_file_list:
                            output_file.write("\t\t{0}\r\n".format(test_path_file))
            else:
                logging.warning("Directory %s does not exist.", mobilebackups_dir)
                output_file.write("[WARNING] Directory {0} does not exist or cannot be found.\r\n".format(mobilebackups_dir))
                print("[WARNING] Directory {0} does not exist.".format(mobilebackups_dir))

            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
