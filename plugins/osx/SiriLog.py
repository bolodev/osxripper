from riplib.plugin import Plugin
import codecs
import logging
import os

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SiriLog(Plugin):
    """
    Plugin to parse /private/var/db/diagnostics/logdata.statistics.[N].txt
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Siri Log"
        self._description = "Parse data from logdata.statistics.0.txt"
        self._data_file = "logdata.statistics.0.txt"
        self._output_file = "Siri.txt"
        self._type = "text"

    def parse(self):
        """
        Parse log file
        """
        date_line = "Statistics for persist stream"
        search_line = "com.apple.siri.embeddedspeech.xpc"
        header_line = "    Activities  Actions         Logs     Traces % Events  " \
                      "Public Data Private Data   % Data Description"

        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("=" * 10 + " " + self._name + " " + "=" * 10 + "\r\n")
            log_file = os.path.join(self._input_dir, "private", "var", "db", "diagnostics", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(log_file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra"]:
                if os.path.isfile(log_file):
                    with open(log_file, "r") as lf:
                        for log_line in lf:
                            if date_line in log_line:
                                of.write("{0}\r\n".format(log_line))
                            elif search_line in log_line:
                                of.write("{0}\r\n".format(header_line))
                                of.write("{0}\r\n".format(log_line))
                                of.write("\r\n")
                        of.write("="*30)
                    lf.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(log_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(log_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(log_file))
            elif self._os_version in ["el_capitan", "yosemite", "mavericks", "mountain_lion", "lion"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
                of.write("="*40 + "\r\n\r\n")
        of.close()
