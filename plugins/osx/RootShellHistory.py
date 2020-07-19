""" Module to parse information from /private/var/root/.sh_history """
import codecs
import logging
import os
from riplib.plugin import Plugin


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
        self.set_name("Root Shell History")
        self.set_description("Parse information from /private/var/root/.sh_history")
        self.set_data_file(".sh_history")
        self.set_output_file("Root.txt")
        self.set_type("file")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        root_path = os.path.join(self._input_dir, "private", "var", "root")
        if os.path.isdir(root_path):
            with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
                output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                file = os.path.join(root_path, self._data_file)
                output_file.write("Source File: {0}\r\n\r\n".format(file))
                if os.path.isfile(file):
                    history_file = codecs.open(file, "r", encoding="utf-8")
                    for lines in history_file:
                        output_file.write(lines.replace("\n", "\r\n"))
                    history_file.close()
                else:
                    logging.warning("File: %s does not exist or cannot be found.", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
                output_file.write("="*40 + "\r\n\r\n")
            output_file.close()
        else:
            print("[WARNING] {0} does not exist.".format(root_path))
            logging.warning("%s does not exist.", root_path)
