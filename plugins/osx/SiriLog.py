""" Module to find Siri usage traces """
import codecs
import logging
import os
from riplib.plugin import Plugin


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
        self.set_name("Siri Log")
        self.set_description("Parse data from logdata.statistics.0.txt")
        self.set_data_file("logdata.statistics.0.txt")
        self.set_output_file("Siri.txt")
        self.set_type("text")

    def parse(self):
        """
        Parse log file
        """
        date_line = "Statistics for persist stream"
        search_line = "com.apple.siri.embeddedspeech.xpc"
        header_line = "    Activities  Actions         Logs     Traces % Events  Public Data Private Data   % Data Description"

        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("=" * 10 + " " + self._name + " " + "=" * 10 + "\r\n")
            log_file = os.path.join(self._input_dir, "private", "var", "db", "diagnostics", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(log_file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra"]:
                if os.path.isfile(log_file):
                    with open(log_file, "r") as lf_handle:
                        for log_line in lf_handle:
                            if date_line in log_line:
                                output_file.write("{0}\r\n".format(log_line))
                            elif search_line in log_line:
                                output_file.write("{0}\r\n".format(header_line))
                                output_file.write("{0}\r\n".format(log_line))
                                output_file.write("\r\n")
                        output_file.write("="*30)
                    lf_handle.close()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", log_file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(log_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(log_file))
            elif self._os_version in ["el_capitan", "yosemite", "mavericks", "mountain_lion", "lion"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
                output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
