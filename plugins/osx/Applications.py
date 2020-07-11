from riplib.Plugin import Plugin
import codecs
import logging
import os

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
        self._name = "Applications"
        self._description = "List files in System amd Library Launch* directories "
        self._data_file = ""  # listing directories so this is not needed
        self._output_file = "Applications.txt"
        self._type = "dir_list"
    
    def parse(self):
        """
        List contents of /Applications directory
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            # N.B. Not testing OS version as /Applications is common to recent OSX versions
            applications_dir = os.path.join(self._input_dir, "Applications")
            if os.path.isdir(applications_dir):
                of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                of.write("Source Directory: {0}\r\n\r\n".format(applications_dir))
                file_listing = os.listdir(applications_dir)
                for f in file_listing:
                    if not f.endswith(".app") and os.path.isdir(os.path.join(applications_dir, f)):
                        of.write("\t{0}\r\n".format(f))
                        sub_dir = os.path.join(applications_dir, f)
                        sub_dir_list = os.listdir(sub_dir)
                        for file_name in sub_dir_list:
                            of.write("\t\t{0}\r\n".format(file_name))
                    else:
                        of.write("\t{0}\r\n".format(f))
            else:
                logging.warning("Directory {0} does not exist.".format(applications_dir))
                of.write("[WARNING] Directory {0} does not exist or cannot be found.\r\n".format(applications_dir))
                print("[WARNING] Directory {0} does not exist.".format(applications_dir))

            of.write("="*40 + "\r\n\r\n")
        of.close()
