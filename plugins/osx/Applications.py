""" Module for listing applications """
import codecs
import logging
import os
from riplib.plugin import Plugin

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class Applications(Plugin):
    """
    Plugin to list /Applications
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Applications")
        self.set_description("List files in System amd Library Launch* directories")
        self.set_data_file("")  # listing directories so this is not needed
        self.set_output_file("Applications.txt")
        self.set_type("dir_list")

    def parse(self):
        """
        List contents of /Applications directory
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            # N.B. Not testing OS version as /Applications is common to recent OSX versions
            applications_dir = os.path.join(self._input_dir, "Applications")
            if os.path.isdir(applications_dir):
                output_file.write("="*10 + " " + self.get_name + " " + "="*10 + "\r\n")
                output_file.write("Source Directory: {0}\r\n\r\n".format(applications_dir))
                file_listing = os.listdir(applications_dir)
                for file_name in file_listing:
                    if not file_name.endswith(".app") and os.path.isdir(os.path.join(applications_dir, file_name)):
                        output_file.write("\t{0}\r\n".format(file_name))
                        sub_dir = os.path.join(applications_dir, file_name)
                        sub_dir_list = os.listdir(sub_dir)
                        for file_name1 in sub_dir_list:
                            output_file.write("\t\t{0}\r\n".format(file_name1))
                    else:
                        output_file.write("\t{0}\r\n".format(file_name))
            else:
                logging.warning("Directory %s does not exist.", applications_dir)
                output_file.write("[WARNING] Directory {0} does not exist or cannot be found.\r\n".format(applications_dir))
                print("[WARNING] Directory {0} does not exist.".format(applications_dir))

            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
