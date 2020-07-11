from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib

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
        self._name = "Cups Printers"
        self._description = "Parse data from org.cups.printers.plist"
        self._data_file = "org.cups.printers.plist"
        self._output_file = "Printers.txt"
        self._type = "plist"
    
    def parse(self):
        """
        Parse /Library/Preferences/org.cups.printers.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(plist_file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            #                         "mavericks", "mountain_lion", "lion", "snow_leopard"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        for printer in plist:
                            if "printer-name" in printer:
                                of.write("Printer Name          : {0}\r\n".format(printer["printer-name"]))
                            if "printer-info" in printer:
                                of.write("Printer Info          : {0}\r\n".format(printer["printer-info"]))
                            if "printer-is-accepting-jobs" in printer:
                                of.write("Printer Accepting Jobs: {0}\r\n".format(printer["printer-is-accepting-jobs"]))
                            if "printer-location" in printer:
                                of.write("Printer Location      : {0}\r\n".format(printer["printer-location"]))
                            if "printer-make-and-model" in printer:
                                of.write("Printer Make & Model  : {0}\r\n".format(printer["printer-make-and-model"]))
                            if "printer-state" in printer:
                                of.write("Printer State         : {0}\r\n".format(printer["printer-state"]))
                            if "printer-state-reasons" in printer:
                                of.write("Printer State Reasons:\r\n")
                                reasons = printer["printer-state-reasons"]
                                for reason in reasons:
                                    of.write("\t{0}\r\n".format(reason))
                            if "printer-type" in printer:
                                of.write("Printer Type          : {0}\r\n".format(printer["printer-type"]))
                            if "device-uri" in printer:
                                of.write("Device URI            : {0}\r\n".format(printer["device-uri"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
