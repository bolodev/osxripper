from riplib.Plugin import Plugin
import codecs
import logging
import os

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
        self._name = "Kernel Extensions"
        self._description = "List extensions in /System/Library/Extensions"
        self._data_file = ""  # listing directories so this is not needed
        self._output_file = "Kernel_Extensions.txt"
        self._type = "dir_list"
    
    def parse(self):
        """
        List contents of /System/Library/Extensions directory
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            extensions_dir = os.path.join(self._input_dir, "System", "Library", "Extensions")
            if os.path.isdir(extensions_dir):
                of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                of.write("Source Directory: {0}\r\n\r\n".format(extensions_dir))
                file_listing = os.listdir(extensions_dir)
                for f in file_listing:
                    if f.endswith(".kext") or f.endswith(".ppp") or f.endswith(".bundle") or f.endswith(".plugin"):
                        of.write("\t{0}\r\n".format(f))
            else:
                logging.warning("Directory {0} does not exist.".format(extensions_dir))
                of.write("[WARNING] Directory {0} does not exist or cannot be found.\r\n".format(extensions_dir))
                print("[WARNING] Directory {0} does not exist.".format(extensions_dir))

            of.write("="*40 + "\r\n\r\n")
        of.close()
