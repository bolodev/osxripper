from riplib.Plugin import Plugin
import codecs
import datetime
import logging
import os
import riplib.ccl_bplist

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
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "private", "var", "db", "locationd", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan",
                if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan",
                                        "yosemite", "mavericks"]:
                    try:
                        bplist = open(file, "rb")
                        plist = riplib.ccl_bplist.load(bplist)
                        bplist.close()
                        for client_dict in plist:
                            of.write("{0}\r\n".format(client_dict))
                            if "Whitelisted" in plist[client_dict]:
                                of.write("\tWhitelisted          : {0}\r\n".format(plist[client_dict]["Whitelisted"]))
                            if "BundleId" in plist[client_dict]:
                                of.write("\tBundle ID            : {0}\r\n".format(plist[client_dict]["BundleId"]))
                            if "Hide" in plist[client_dict]:
                                of.write("\tHide                 : {0}\r\n".format(plist[client_dict]["Hide"]))
                            if "LocationTimeStopped" in plist[client_dict]:
                                of.write("\tLocation Time Stopped: {0}\r\n"
                                         .format(mac_absolute + datetime
                                                 .timedelta(0, float(plist[client_dict]["LocationTimeStopped"]))))
                            if "BundlePath" in plist[client_dict]:
                                of.write("\tBundle Path          : {0}\r\n".format(plist[client_dict]["BundlePath"]))
                            if "Registered" in plist[client_dict]:
                                of.write("\tRegistered           : {0}\r\n".format(plist[client_dict]["Registered"]))
                            if "Executable" in plist[client_dict]:
                                of.write("\tExecutable           : {0}\r\n".format(plist[client_dict]["Executable"]))
                            if "Requirement" in plist[client_dict]:
                                of.write("\tRequirement          : {0}\r\n".format(plist[client_dict]["Requirement"]))
                            if "Authorized" in plist[client_dict]:
                                of.write("\tAuthorized           : {0}\r\n".format(plist[client_dict]["Authorized"]))
                            of.write("\r\n")
                        of.write("\r\n")
                    except KeyError:
                        pass

                elif self._os_version == "mountain_lion":
                    try:
                        bplist = open(file, "rb")
                        plist = riplib.ccl_bplist.load(bplist)
                        bplist.close()
                        for client_dict in plist:
                            of.write("{0}\r\n".format(client_dict))
                            if "RequirementString" in plist[client_dict]:
                                of.write("\tRequirement String: {0}\r\n".format(plist[client_dict]["RequirementString"]))
                    except KeyError:
                        pass
                elif self._os_version in ["lion", "snow_leopard"]:
                    logging.info("This version of OSX is not supported by this plugin.")
                    print("[INFO] This version of OSX is not supported by this plugin.")
                    of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
                else:
                    logging.warning("Not a known OSX version.")
                    print("[WARNING] Not a known OSX version.")
            else:
                logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            of.write("="*40 + "\r\n\r\n")
        of.close()
