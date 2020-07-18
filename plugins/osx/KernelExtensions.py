""" Module to list Kernel Extensions """
import codecs
import logging
import os
from riplib.plugin import Plugin

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class KernelExtensions(Plugin):
    """
    Plugin to list Kernel Extensions from /System/Library/Extensions
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Kernel Extensions")
        self.set_description("List extensions in /System/Library/Extensions")
        self.set_data_file("")  # listing directories so this is not needed
        self.set_output_file("Kernel_Extensions.txt")
        self.set_type("dir_list")

    def parse(self):
        """
        List contents of /System/Library/Extensions directory
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            extensions_dir = os.path.join(self._input_dir, "System", "Library", "Extensions")
            if os.path.isdir(extensions_dir):
                output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                output_file.write("Source Directory: {0}\r\n\r\n".format(extensions_dir))
                file_listing = os.listdir(extensions_dir)
                for file_name in file_listing:
                    if file_name.endswith(".kext") or file_name.endswith(".ppp") or file_name.endswith(".bundle") or file_name.endswith(".plugin"):
                        output_file.write("\t{0}\r\n".format(file_name))
            else:
                logging.warning("Directory %s does not exist.", extensions_dir)
                output_file.write("[WARNING] Directory {0} does not exist or cannot be found.\r\n".format(extensions_dir))
                print("[WARNING] Directory {0} does not exist.".format(extensions_dir))

            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
