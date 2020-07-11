from riplib.Plugin import Plugin
import codecs
import logging
import os

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class MobileBackupList(Plugin):
    """
    Plugin to list Kernel Extensions from /.MobileBackups
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Mobile Backups"
        self._description = "List extensions in /.MobileBackups"
        self._data_file = ""  # listing directories so this is not needed
        self._output_file = "MobileBackups.txt"
        self._type = "dir_list"
    
    def parse(self):
        """
        List contents of /.MobileBackups directory
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            mobilebackups_dir = os.path.join(self._input_dir, ".MobileBackups")
            if os.path.isdir(mobilebackups_dir):
                of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                of.write("Source Directory: {0}\r\n\r\n".format(mobilebackups_dir))
                file_listing = os.listdir(mobilebackups_dir)
                for f in file_listing:
                    of.write("\t{0}\r\n".format(f))
                    test_path = os.path.join(mobilebackups_dir, f)
                    if os.path.isdir(test_path):
                        test_path_file_list = os.listdir(test_path)
                        for test_path_file in test_path_file_list:
                            of.write("\t\t{0}\r\n".format(test_path_file))
            else:
                logging.warning("Directory {0} does not exist.".format(mobilebackups_dir))
                of.write("[WARNING] Directory {0} does not exist or cannot be found.\r\n".format(mobilebackups_dir))
                print("[WARNING] Directory {0} does not exist.".format(mobilebackups_dir))

            of.write("="*40 + "\r\n\r\n")
        of.close()