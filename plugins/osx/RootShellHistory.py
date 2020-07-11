from riplib.Plugin import Plugin
import codecs
import logging
import os

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class RootShellHistory(Plugin):
    """
    Parse information from /private/var/root/.sh_history
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Root Shell History"
        self._description = "Parse information from /private/var/root/.sh_history"
        self._data_file = ".sh_history"
        self._output_file = "Root.txt" 
        self._type = "file"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        root_path = os.path.join(self._input_dir, "private", "var", "root")
        if os.path.isdir(root_path):
            with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                file = os.path.join(root_path, self._data_file)
                of.write("Source File: {0}\r\n\r\n".format(file))
                if os.path.isfile(file):
                    history_file = codecs.open(file, "r", encoding="utf-8")
                    for lines in history_file:
                        of.write(lines.replace("\n", "\r\n"))
                    history_file.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
                of.write("="*40 + "\r\n\r\n")
            of.close()
        else:
            print("[WARNING] {0} does not exist.".format(root_path))
            logging.warning("{0} does not exist.".format(root_path))
