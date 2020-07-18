""" Module for parsing CUPS plist """
import codecs
import logging
import os
import plistlib
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class CupsPrintersPlist(Plugin):
    """
    Plugin to parse /Library/Preferences/org.cups.printers.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Cups Printers")
        self.set_description("Parse data from org.cups.printers.plist")
        self.set_data_file("org.cups.printers.plist")
        self.set_output_file("Printers.txt")
        self.set_type("plist")

    def parse(self):
        """
        Parse /Library/Preferences/org.cups.printers.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(plist_file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            #                         "mavericks", "mountain_lion", "lion", "snow_leopard"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as plist_to_load:
                        plist = plistlib.load(plist_to_load)
                    plist_to_load.close()
                    try:
                        for printer in plist:
                            if "printer-name" in printer:
                                output_file.write("Printer Name          : {0}\r\n".format(printer["printer-name"]))
                            if "printer-info" in printer:
                                output_file.write("Printer Info          : {0}\r\n".format(printer["printer-info"]))
                            if "printer-is-accepting-jobs" in printer:
                                output_file.write("Printer Accepting Jobs: {0}\r\n".format(printer["printer-is-accepting-jobs"]))
                            if "printer-location" in printer:
                                output_file.write("Printer Location      : {0}\r\n".format(printer["printer-location"]))
                            if "printer-make-and-model" in printer:
                                output_file.write("Printer Make & Model  : {0}\r\n".format(printer["printer-make-and-model"]))
                            if "printer-state" in printer:
                                output_file.write("Printer State         : {0}\r\n".format(printer["printer-state"]))
                            if "printer-state-reasons" in printer:
                                output_file.write("Printer State Reasons:\r\n")
                                reasons = printer["printer-state-reasons"]
                                for reason in reasons:
                                    output_file.write("\t{0}\r\n".format(reason))
                            if "printer-type" in printer:
                                output_file.write("Printer Type          : {0}\r\n".format(printer["printer-type"]))
                            if "device-uri" in printer:
                                output_file.write("Device URI            : {0}\r\n".format(printer["device-uri"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", plist_file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
