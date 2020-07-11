from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.ccl_bplist

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class AlfPlist(Plugin):
    """
    Plugin to parse /Library/Preferences/com.apple.alf.plist
    """
    def __init__(self):
        """
        Initialise plugins
        """
        super().__init__()
        self._name = "Firewall Settings"
        self._description = "Parse Firewall settings from /Library/Preferences/com.apple.alf.plist"
        self._data_file = "com.apple.alf.plist"
        self._output_file = "Networking.txt"
        self._type = "bplist"
        
    def parse(self):
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(file))
            #if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            #                        "mavericks"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "allowsignedenabled" in plist:
                            of.write("Allow Signed: {0}\r\n".format(plist["allowsignedenabled"]))
                        if "globalstate" in plist:
                            of.write("Global State: {0}\r\n".format(plist["globalstate"]))
                        if "loggingoption" in plist:
                            of.write("Global State: {0}\r\n".format(plist["loggingoption"]))
                        if "stealthenabled" in plist:
                            of.write("Stealth Enabled: {0}\r\n".format(plist["stealthenabled"]))
                        if "version" in plist:
                            of.write("Version: {0}\r\n".format(plist["version"]))
                        if "loggingenabled" in plist:
                            of.write("Logging Enabled: {0}\r\n".format(plist["loggingenabled"]))
                        if "firewallunload" in plist:
                            of.write("Firewall Unload: {0}\r\n".format(plist["firewallunload"]))

                        if "exceptions" in plist:
                            of.write("Exceptions:\r\n")
                            exps = plist["exceptions"]
                            for exp in exps:
                                of.write("\tPath: {0}\r\n".format(exp["path"]))
                                of.write("\tState: {0}\r\n".format(exp["state"]))

                        if "firewall" in plist:
                            firewall_dict = plist["firewall"]
                            of.write("Firewall:\r\n")
                            for fw_dict in firewall_dict:
                                of.write("\t{0}:\r\n".format(fw_dict))
                                of.write("\t\tState: {0}\r\n".format(firewall_dict[fw_dict]["state"]))
                                of.write("\t\tProc: {0}\r\n".format(firewall_dict[fw_dict]["proc"]))

                        if "explicitauths" in plist:
                            explicit_auths = plist["explicitauths"]
                            of.write("Explicit Auths:\r\n")
                            for explicit_auth in explicit_auths:
                                of.write("\t{0}\r\n".format(explicit_auth["id"]))
                            
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
                    
            elif self._os_version in ["mountain_lion", "lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "allowsignedenabled" in plist:
                            of.write("Allow Signed: {0}\r\n".format(plist["allowsignedenabled"]))
                        if "globalstate" in plist:
                            of.write("Global State: {0}\r\n".format(plist["globalstate"]))
                        if "loggingoption" in plist:
                            of.write("Global State: {0}\r\n".format(plist["loggingoption"]))
                        if "stealthenabled" in plist:
                            of.write("Stealth Enabled: {0}\r\n".format(plist["stealthenabled"]))
                        if "version" in plist:
                            of.write("Version: {0}\r\n".format(plist["version"]))
                        if "loggingenabled" in plist:
                            of.write("Logging Enabled: {0}\r\n".format(plist["loggingenabled"]))
                        if "firewallunload" in plist:
                            of.write("Firewall Unload: {0}\r\n".format(plist["firewallunload"]))
                        if "previousonstate" in plist:
                            of.write("Previous On State: {0}\r\n".format(plist["previousonstate"]))

                        if "exceptions" in plist:
                            of.write("Exceptions:\r\n")
                            exps = plist["exceptions"]
                            for exp in exps:
                                of.write("\tPath: {0}\r\n".format(exp["path"]))
                                of.write("\tState: {0}\r\n".format(exp["state"]))

                        if "firewall" in plist:
                            firewall_dict = plist["firewall"]
                            of.write("Firewall:\r\n")
                            for fw_dict in firewall_dict:
                                of.write("\t{0}:\r\n".format(fw_dict))
                                of.write("\t\tState: {0}\r\n".format(firewall_dict[fw_dict]["state"]))
                                of.write("\t\tProc: {0}\r\n".format(firewall_dict[fw_dict]["proc"]))

                        if "explicitauths" in plist:
                            explicit_auths = plist["explicitauths"]
                            of.write("Explicit Auths:\r\n")
                            for explicit_auth in explicit_auths:
                                of.write("\t{0}\r\n".format(explicit_auth["id"]))
                            
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(file) and os.path.getsize(file) != 0:
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "allowsignedenabled" in plist:
                            of.write("Allow Signed: {0}\r\n".format(plist["allowsignedenabled"]))
                        if "globalstate" in plist:
                            of.write("Global State: {0}\r\n".format(plist["globalstate"]))
                        if "loggingoption" in plist:
                            of.write("Global State: {0}\r\n".format(plist["loggingoption"]))
                        if "stealthenabled" in plist:
                            of.write("Stealth Enabled: {0}\r\n".format(plist["stealthenabled"]))
                        if "version" in plist:
                            of.write("Version: {0}\r\n".format(plist["version"]))
                        if "loggingenabled" in plist:
                            of.write("Logging Enabled: {0}\r\n".format(plist["loggingenabled"]))
                        if "firewallunload" in plist:
                            of.write("Firewall Unload: {0}\r\n".format(plist["firewallunload"]))

                        if "exceptions" in plist:
                            of.write("Exceptions:\r\n")
                            exps = plist["exceptions"]
                            for exp in exps:
                                of.write("\tPath: {0}\r\n".format(exp["path"]))
                                of.write("\tState: {0}\r\n".format(exp["state"]))

                        if "firewall" in plist:
                            firewall_dict = plist["firewall"]
                            of.write("Firewall:\r\n")
                            for fw_dict in firewall_dict:
                                of.write("\t{0}:\r\n".format(fw_dict))
                                of.write("\t\tState: {0}\r\n".format(firewall_dict[fw_dict]["state"]))
                                of.write("\t\tProc: {0}\r\n".format(firewall_dict[fw_dict]["proc"]))

                        if "explicitauths" in plist:
                            explicit_auths = plist["explicitauths"]
                            of.write("Explicit Auths:\r\n")
                            for explicit_auth in explicit_auths:
                                of.write("\t{0}\r\n".format(explicit_auth["path"]))

                        if "signexceptions" in plist:
                            signed_exceptions = plist["signexceptions"]
                            of.write("Signed Exceptions:\r\n")
                            for signed_exception in signed_exceptions:
                                proc_name = signed_exception["procname"]
                                if proc_name == "":
                                    proc_name = "NO_PROC_NAME"
                                of.write("\tProc Name: {0}\r\n".format(proc_name))
                                if "bundleid" in signed_exception:
                                    of.write("\tBundle ID : {0}\r\n".format(signed_exception["bundleid"]))
                                if "creator" in signed_exception:
                                    of.write("\tCreator   : {0}\r\n".format(signed_exception["creator"]))

                        if "applications" in plist:
                            applications = plist["applications"]
                            of.write("Applications:\r\n")
                            for application in applications:
                                of.write("\tBundle ID: {0}\r\n".format(application["bundleid"]))
                                of.write("\tState    : {0}\r\n".format(application["state"]))

                    except KeyError:
                        pass
                    bplist.close()
                pass
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
