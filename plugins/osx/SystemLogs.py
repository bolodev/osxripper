from riplib.Plugin import Plugin
import codecs
import logging
import os
import gzip

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemLogs(Plugin):
    """
    plugin to extract and decompress system logs
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Logs"
        self._description = "Locate and extract System.log and backups from /private/var/log"
        self._data_file = ""  # listing directories so this is not needed
        self._output_file = "System_Log_Completed.txt"
        self._type = "text"
    
    def parse(self):
        """
        Locate and extract System.log and backups from /private/var/log
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            working_dir = os.path.join(self._input_dir, "private", "var", "log")
            of.write("Source Directory: {0}\r\n\r\n".format(working_dir))

        # Get list of system logs as there many be many zipped up
        # Output log file names at the top of master output file so we know what we are working with

            if os.path.isdir(working_dir) and os.path.isfile(os.path.join(working_dir, "system.log")):
                file_listing = []
                file_listing_all = os.listdir(working_dir) 
                of.write("="*10 + " Log File Found: System Log " + "="*10 + "\r\n")
                for f in file_listing_all:
                    if f.startswith("system") and f.endswith(".gz"):
                        file_listing.append(os.path.join(working_dir, f))
                        of.write("="*10 + " Log File Found: " + os.path.join(working_dir, f) + " " + "="*10 + "\r\n")

        # Open first unzipped log and write this out to master output file

                of.write("\r\n")
                system_log_file = codecs.open(os.path.join(working_dir, "system.log"), "r", encoding="utf-8")
                of.write("\r\n")
                of.write("="*10 + " Current Live System Log file " + "="*10 + "\r\n")
                of.write("\r\n")
                for lines in system_log_file:
                    of.write(lines.replace("\n", "\r\n"))
                system_log_file.close()

        # Open the zipped log files and write the contents out appended to the master output file        

                for logs in file_listing:
                    of.write("\r\n")
                    of.write("="*10 + " Log file: " + logs + "="*10 + "\r\n")
                    of.write("\r\n")
                    running_file = gzip.open(logs, "rb")
                    dumped_file = running_file.read()
                    of.write(dumped_file.decode('utf-8'))    
                    running_file.close()
                of.write("\r\n")
                of.write("="*40 + "\r\n\r\n")
            else:
                logging.warning("Directory {0} or File {1} does not exist or cannot be found.\r\n"
                                .format(working_dir, "System Log"))
                of.write("[WARNING] Directory {0} or File {1} does not exist or cannot be found.\r\n"
                         .format(working_dir, "System Log"))
                print("[WARNING] Directory {0} or File {1} does not exist or cannot be found.\r\n"
                      .format(working_dir, "System Log"))
            of.close()
