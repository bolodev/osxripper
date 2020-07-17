from riplib.plugin import Plugin
import codecs
import logging
import os

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class Autoruns(Plugin):
    """
    Plugin to list autoruns
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Autoruns"
        self._description = "List files in System amd Library Launch* directories "
        self._data_file = ""  # listing directories so this is not needed
        self._output_file = "Autoruns.txt"
        self._type = "dir_list"
    
    def parse(self):
        """
        List contents of known Launch* directories
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            #                         "mavericks", "mountain_lion", "lion", "snow_leopard"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                sys_lib_launch_agents = os.path.join(self._input_dir, "System", "Library", "LaunchAgents")
                sys_lib_launch_daemons = os.path.join(self._input_dir, "System", "Library", "LaunchDaemons")
                sys_lib_startup_items = os.path.join(self._input_dir, "System", "Library", "StartupItems")
                lib_launch_agents = os.path.join(self._input_dir, "Library", "LaunchAgents")
                lib_launch_daemons = os.path.join(self._input_dir, "Library", "LaunchDaemons")
                lib_startup_items = os.path.join(self._input_dir, "Library", "StartupItems")
                collected_directories = [sys_lib_launch_agents, sys_lib_launch_daemons, sys_lib_startup_items,
                                         lib_launch_agents, lib_launch_daemons, lib_startup_items]
                for doi in collected_directories:
                    if os.path.isdir(doi):
                        of.write("="*10 + " Autoruns: " + doi.replace(self._input_dir, "") + "="*10 + "\r\n")
                        of.write("Source Directory: {0}\r\n\r\n".format(doi))
                        file_listing = os.listdir(doi)
                        for f in file_listing:
                            of.write("\t{0}\r\n".format(f))
                    else:
                        logging.warning("Directory {0} does not exist.".format(doi))
                        of.write("[WARNING] Directory {0} does not exist or cannot be found.\r\n".format(doi))
                        print("[WARNING] Directory {0} does not exist.".format(doi))
            else:
                logging.warning("[WARNING] Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
