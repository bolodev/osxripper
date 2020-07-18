""" Module to parse clients.plist """
import codecs
import datetime
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class LocationdClientsPlist(Plugin):
    """
    Plugin to parse /private/var/db/locationd/clients.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Location Clients"
        self._description = "Parse data from /private/var/db/locationd/clients.plist"
        self._data_file = "clients.plist"
        self._output_file = "Location.txt"
        self._type = "bplist"

    def parse(self):
        """
        Parse /private/var/db/locationd/clients.plist
        """
        mac_absolute = datetime.datetime(2001, 1, 1, 0, 0, 0)
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "private", "var", "db", "locationd", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan",
                if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan",
                                        "yosemite", "mavericks"]:
                    try:
                        bplist = open(file, "rb")
                        plist = riplib.ccl_bplist.load(bplist)
                        bplist.close()
                        for client_dict in plist:
                            output_file.write("{0}\r\n".format(client_dict))
                            if "Whitelisted" in plist[client_dict]:
                                output_file.write("\tWhitelisted          : {0}\r\n".format(plist[client_dict]["Whitelisted"]))
                            if "BundleId" in plist[client_dict]:
                                output_file.write("\tBundle ID            : {0}\r\n".format(plist[client_dict]["BundleId"]))
                            if "Hide" in plist[client_dict]:
                                output_file.write("\tHide                 : {0}\r\n".format(plist[client_dict]["Hide"]))
                            if "LocationTimeStopped" in plist[client_dict]:
                                output_file.write("\tLocation Time Stopped: {0}\r\n".format(mac_absolute + datetime.timedelta(0, float(plist[client_dict]["LocationTimeStopped"]))))
                            if "BundlePath" in plist[client_dict]:
                                output_file.write("\tBundle Path          : {0}\r\n".format(plist[client_dict]["BundlePath"]))
                            if "Registered" in plist[client_dict]:
                                output_file.write("\tRegistered           : {0}\r\n".format(plist[client_dict]["Registered"]))
                            if "Executable" in plist[client_dict]:
                                output_file.write("\tExecutable           : {0}\r\n".format(plist[client_dict]["Executable"]))
                            if "Requirement" in plist[client_dict]:
                                output_file.write("\tRequirement          : {0}\r\n".format(plist[client_dict]["Requirement"]))
                            if "Authorized" in plist[client_dict]:
                                output_file.write("\tAuthorized           : {0}\r\n".format(plist[client_dict]["Authorized"]))
                            output_file.write("\r\n")
                        output_file.write("\r\n")
                    except KeyError:
                        pass

                elif self._os_version == "mountain_lion":
                    try:
                        bplist = open(file, "rb")
                        plist = riplib.ccl_bplist.load(bplist)
                        bplist.close()
                        for client_dict in plist:
                            output_file.write("{0}\r\n".format(client_dict))
                            if "RequirementString" in plist[client_dict]:
                                output_file.write("\tRequirement String: {0}\r\n".format(plist[client_dict]["RequirementString"]))
                    except KeyError:
                        pass
                elif self._os_version in ["lion", "snow_leopard"]:
                    logging.info("This version of OSX is not supported by this plugin.")
                    print("[INFO] This version of OSX is not supported by this plugin.")
                    output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
                else:
                    logging.warning("Not a known OSX version.")
                    print("[WARNING] Not a known OSX version.")
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
