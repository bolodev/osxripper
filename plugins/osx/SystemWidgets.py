""" Module to list .wdgt directories in /Library/Widgets """
import codecs
import logging
import os
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemWidgets(Plugin):
    """
    Plugin to list .wdgt directories in /Library/Widgets
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("System Widgets")
        self.set_description("List .wdgt directories in /Library/Widgets")
        self.set_data_file("")  # listing directories so this is not needed
        self.set_output_file("SystemWidgets.txt")
        self.set_type("dir_list")

    def parse(self):
        """
        List .wdgt files under /Library/Widgets
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            working_dir = os.path.join(self._input_dir, "Library", "Widgets")
            output_file.write("Source Directory: {0}\r\n\r\n".format(working_dir))
            # No widgets in Catalina
            if self._os_version in ["big_sur", "catalina"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                output_file.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            elif self._os_version in ["mojave", "sierra", "el_capitan", "yosemite", "mavericks",
                                      "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isdir(working_dir):
                    file_listing = os.listdir(working_dir)
                    for file_name in file_listing:
                        if file_name.endswith(".wdgt"):
                            output_file.write(file_name + "\r\n")
                    output_file.write("\r\n")
                else:
                    logging.warning("Directory: %s does not exist or cannot be found.\r\n", working_dir)
                    output_file.write("[WARNING] Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
                    print("[WARNING] Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
            elif self._os_version in ["high_sierra"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                output_file.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
