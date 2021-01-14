""" Module to parse DiagnosticReporting data """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class DiagnosticReportingNetworks(Plugin):
    """
    Plugin to parse /Library/Caches/com.apple.DiagnosticReporting.Networks.plist
    """
    def __init__(self):
        """
        Initialise plugins
        """
        super().__init__()
        self.set_name("DiagnosticReporting.Networks")
        self.set_description("Parse DHCP Lease plists from /Library/Caches/com.apple.DiagnosticReporting.Networks.plist")
        self.set_data_file("com.apple.DiagnosticReporting.Networks.plist")
        self.set_output_file("Networking.txt")
        self.set_type("bplist")

    def parse(self):
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Caches", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "ExternalSignatures" in plist:
                            for ext_sig in plist["ExternalSignatures"]:
                                output_file.write("Network Data: {0}\r\n".format(ext_sig))
                                output_file.write("Timestamp: {0}\r\n".format(plist["ExternalSignatures"][ext_sig]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("[WARNING] File: {0} does not exist or cannot be found.")
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                output_file.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
