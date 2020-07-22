""" Module to extract and decompress system logs """
import codecs
import logging
import os
import gzip
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemLogs(Plugin):
    """
    Plugin to extract and decompress system logs
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("System Logs")
        self.set_description("Locate and extract System.log and backups from /private/var/log")
        self.set_data_file("")  # listing directories so this is not needed
        self.set_output_file("System_Log_Completed.txt")
        self.set_type("text")

    def parse(self):
        """
        Locate and extract System.log and backups from /private/var/log
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            working_dir = os.path.join(self._input_dir, "private", "var", "log")
            output_file.write("Source Directory: {0}\r\n\r\n".format(working_dir))

        # Get list of system logs as there many be many zipped up
        # Output log file names at the top of master output file so we know what we are working with

            if os.path.isdir(working_dir) and os.path.isfile(os.path.join(working_dir, "system.log")):
                file_listing = []
                file_listing_all = os.listdir(working_dir)
                output_file.write("="*10 + " Log File Found: System Log " + "="*10 + "\r\n")
                for file_name in file_listing_all:
                    if file_name.startswith("system") and file_name.endswith(".gz"):
                        file_listing.append(os.path.join(working_dir, file_name))
                        output_file.write("="*10 + " Log File Found: " + os.path.join(working_dir, file_name) + " " + "="*10 + "\r\n")

        # Open first unzipped log and write this out to master output file

                output_file.write("\r\n")
                system_log_file = codecs.open(os.path.join(working_dir, "system.log"), "r", encoding="utf-8")
                output_file.write("\r\n")
                output_file.write("="*10 + " Current Live System Log file " + "="*10 + "\r\n")
                output_file.write("\r\n")
                for lines in system_log_file:
                    output_file.write(lines.replace("\n", "\r\n"))
                system_log_file.close()

        # Open the zipped log files and write the contents out appended to the master output file

                for logs in file_listing:
                    output_file.write("\r\n")
                    output_file.write("="*10 + " Log file: " + logs + "="*10 + "\r\n")
                    output_file.write("\r\n")
                    running_file = gzip.open(logs, "rb")
                    dumped_file = running_file.read()
                    output_file.write(dumped_file.decode('utf-8'))
                    running_file.close()
                output_file.write("\r\n")
                output_file.write("="*40 + "\r\n\r\n")
            else:
                logging.warning("Directory %s or File %s does not exist or cannot be found.\r\n", working_dir, "System Log")
                output_file.write("[WARNING] Directory {0} or File {1} does not exist or cannot be found.\r\n".format(working_dir, "System Log"))
                print("[WARNING] Directory {0} or File {1} does not exist or cannot be found.\r\n".format(working_dir, "System Log"))
            output_file.close()
