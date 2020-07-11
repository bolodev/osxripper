from riplib.Plugin import Plugin
import codecs
import logging
import os

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemWidgets(Plugin):
    """
    Plugin to list .wdgt directories in /Library/Widgets"
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Widgets"
        self._description = "List .wdgt directories in /Library/Widgets"
        self._data_file = ""  # listing directories so this is not needed
        self._output_file = "SystemWidgets.txt"
        self._type = "dir_list"
    
    def parse(self):
        """
        List .wdgt files under /Library/Widgets
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            working_dir = os.path.join(self._input_dir, "Library", "Widgets")
            of.write("Source Directory: {0}\r\n\r\n".format(working_dir))
            # No widgets in Catalina
            # if self._os_version in ["big_sur", "catalina"]:
            if self._os_version in ["catalina"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            elif self._os_version in ["mojave", "sierra", "el_capitan", "yosemite", "mavericks",
                                      "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isdir(working_dir):
                    file_listing = os.listdir(working_dir)
                    for f in file_listing:
                        if f.endswith(".wdgt"):
                            of.write(f + "\r\n")
                    of.write("\r\n")
                else:
                    logging.warning("Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
                    of.write("[WARNING] Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
                    print("[WARNING] Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
            elif self._os_version in ["high_sierra"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()