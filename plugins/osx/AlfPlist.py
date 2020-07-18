""" Module for parsing firewall plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


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
        self.set_name("Firewall Settings")
        self.set_description("Parse Firewall settings from /Library/Preferences/com.apple.alf.plist")
        self.set_data_file("com.apple.alf.plist")
        self.set_output_file("Networking.txt")
        self.set_type("bplist")

    def parse(self):
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(file))

            if os.path.isfile(file):
                bplist = open(file, "rb")
                plist = riplib.ccl_bplist.load(bplist)
                bplist.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
                output_file.close()
                return

            #if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            #                        "mavericks"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks"]:
                parse_osx = Parse01(output_file, plist)
                parse_osx.parse()
            elif self._os_version in ["mountain_lion", "lion"]:
                parse_osx = Parse02(output_file, plist)
                parse_osx.parse()
            elif self._os_version == "snow_leopard":
                parse_osx = Parse03(output_file, plist)
                parse_osx.parse()
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()


class Parse01():
    """
    Convenience class for parsing macOS data
    """
    def __init__(self, output_file, data_file):
        self._output_file = output_file
        self._data_file = data_file

    def parse(self):
        """
        Parse data
        """
        try:
            if "allowsignedenabled" in self._data_file:
                self._output_file.write("Allow Signed: {0}\r\n".format(self._data_file["allowsignedenabled"]))
            if "globalstate" in self._data_file:
                self._output_file.write("Global State: {0}\r\n".format(self._data_file["globalstate"]))
            if "loggingoption" in self._data_file:
                self._output_file.write("Global State: {0}\r\n".format(self._data_file["loggingoption"]))
            if "stealthenabled" in self._data_file:
                self._output_file.write("Stealth Enabled: {0}\r\n".format(self._data_file["stealthenabled"]))
            if "version" in self._data_file:
                self._output_file.write("Version: {0}\r\n".format(self._data_file["version"]))
            if "loggingenabled" in self._data_file:
                self._output_file.write("Logging Enabled: {0}\r\n".format(self._data_file["loggingenabled"]))
            if "firewallunload" in self._data_file:
                self._output_file.write("Firewall Unload: {0}\r\n".format(self._data_file["firewallunload"]))

            if "exceptions" in self._data_file:
                self._output_file.write("Exceptions:\r\n")
                exps = self._data_file["exceptions"]
                for exp in exps:
                    self._output_file.write("\tPath: {0}\r\n".format(exp["path"]))
                    self._output_file.write("\tState: {0}\r\n".format(exp["state"]))

            if "firewall" in self._data_file:
                firewall_dict = self._data_file["firewall"]
                self._output_file.write("Firewall:\r\n")
                for fw_dict in firewall_dict:
                    self._output_file.write("\t{0}:\r\n".format(fw_dict))
                    self._output_file.write("\t\tState: {0}\r\n".format(firewall_dict[fw_dict]["state"]))
                    self._output_file.write("\t\tProc: {0}\r\n".format(firewall_dict[fw_dict]["proc"]))

            if "explicitauths" in self._data_file:
                explicit_auths = self._data_file["explicitauths"]
                self._output_file.write("Explicit Auths:\r\n")
                for explicit_auth in explicit_auths:
                    self._output_file.write("\t{0}\r\n".format(explicit_auth["id"]))
        except KeyError:
            pass

class Parse02():
    """
    Convenience class for parsing macOS data
    """
    def __init__(self, output_file, data_file):
        self._output_file = output_file
        self._data_file = data_file

    def parse(self):
        """
        Parse data
        """
        try:
            if "allowsignedenabled" in self._data_file:
                self._output_file.write("Allow Signed: {0}\r\n".format(self._data_file["allowsignedenabled"]))
            if "globalstate" in self._data_file:
                self._output_file.write("Global State: {0}\r\n".format(self._data_file["globalstate"]))
            if "loggingoption" in self._data_file:
                self._output_file.write("Global State: {0}\r\n".format(self._data_file["loggingoption"]))
            if "stealthenabled" in self._data_file:
                self._output_file.write("Stealth Enabled: {0}\r\n".format(self._data_file["stealthenabled"]))
            if "version" in self._data_file:
                self._output_file.write("Version: {0}\r\n".format(self._data_file["version"]))
            if "loggingenabled" in self._data_file:
                self._output_file.write("Logging Enabled: {0}\r\n".format(self._data_file["loggingenabled"]))
            if "firewallunload" in self._data_file:
                self._output_file.write("Firewall Unload: {0}\r\n".format(self._data_file["firewallunload"]))
            if "previousonstate" in self._data_file:
                self._output_file.write("Previous On State: {0}\r\n".format(self._data_file["previousonstate"]))

            if "exceptions" in self._data_file:
                self._output_file.write("Exceptions:\r\n")
                exps = self._data_file["exceptions"]
                for exp in exps:
                    self._output_file.write("\tPath: {0}\r\n".format(exp["path"]))
                    self._output_file.write("\tState: {0}\r\n".format(exp["state"]))

            if "firewall" in self._data_file:
                firewall_dict = self._data_file["firewall"]
                self._output_file.write("Firewall:\r\n")
                for fw_dict in firewall_dict:
                    self._output_file.write("\t{0}:\r\n".format(fw_dict))
                    self._output_file.write("\t\tState: {0}\r\n".format(firewall_dict[fw_dict]["state"]))
                    self._output_file.write("\t\tProc: {0}\r\n".format(firewall_dict[fw_dict]["proc"]))

            if "explicitauths" in self._data_file:
                explicit_auths = self._data_file["explicitauths"]
                self._output_file.write("Explicit Auths:\r\n")
                for explicit_auth in explicit_auths:
                    self._output_file.write("\t{0}\r\n".format(explicit_auth["id"]))

        except KeyError:
            pass

class Parse03():
    """
    Convenience class for parsing macOS data
    """
    def __init__(self, output_file, data_file):
        self._output_file = output_file
        self._data_file = data_file

    def parse(self):
        """
        Parse data
        """
        try:
            if "allowsignedenabled" in self._data_file:
                self._output_file.write("Allow Signed: {0}\r\n".format(self._data_file["allowsignedenabled"]))
            if "globalstate" in self._data_file:
                self._output_file.write("Global State: {0}\r\n".format(self._data_file["globalstate"]))
            if "loggingoption" in self._data_file:
                self._output_file.write("Global State: {0}\r\n".format(self._data_file["loggingoption"]))
            if "stealthenabled" in self._data_file:
                self._output_file.write("Stealth Enabled: {0}\r\n".format(self._data_file["stealthenabled"]))
            if "version" in self._data_file:
                self._output_file.write("Version: {0}\r\n".format(self._data_file["version"]))
            if "loggingenabled" in self._data_file:
                self._output_file.write("Logging Enabled: {0}\r\n".format(self._data_file["loggingenabled"]))
            if "firewallunload" in self._data_file:
                self._output_file.write("Firewall Unload: {0}\r\n".format(self._data_file["firewallunload"]))

            if "exceptions" in self._data_file:
                self._output_file.write("Exceptions:\r\n")
                exps = self._data_file["exceptions"]
                for exp in exps:
                    self._output_file.write("\tPath: {0}\r\n".format(exp["path"]))
                    self._output_file.write("\tState: {0}\r\n".format(exp["state"]))

            if "firewall" in self._data_file:
                firewall_dict = self._data_file["firewall"]
                self._output_file.write("Firewall:\r\n")
                for fw_dict in firewall_dict:
                    self._output_file.write("\t{0}:\r\n".format(fw_dict))
                    self._output_file.write("\t\tState: {0}\r\n".format(firewall_dict[fw_dict]["state"]))
                    self._output_file.write("\t\tProc: {0}\r\n".format(firewall_dict[fw_dict]["proc"]))

            if "explicitauths" in self._data_file:
                explicit_auths = self._data_file["explicitauths"]
                self._output_file.write("Explicit Auths:\r\n")
                for explicit_auth in explicit_auths:
                    self._output_file.write("\t{0}\r\n".format(explicit_auth["path"]))

            if "signexceptions" in self._data_file:
                signed_exceptions = self._data_file["signexceptions"]
                self._output_file.write("Signed Exceptions:\r\n")
                for signed_exception in signed_exceptions:
                    proc_name = signed_exception["procname"]
                    if proc_name == "":
                        proc_name = "NO_PROC_NAME"
                    self._output_file.write("\tProc Name: {0}\r\n".format(proc_name))
                    if "bundleid" in signed_exception:
                        self._output_file.write("\tBundle ID : {0}\r\n".format(signed_exception["bundleid"]))
                    if "creator" in signed_exception:
                        self._output_file.write("\tCreator   : {0}\r\n".format(signed_exception["creator"]))

            if "applications" in self._data_file:
                applications = self._data_file["applications"]
                self._output_file.write("Applications:\r\n")
                for application in applications:
                    self._output_file.write("\tBundle ID: {0}\r\n".format(application["bundleid"]))
                    self._output_file.write("\tState    : {0}\r\n".format(application["state"]))

        except KeyError:
            pass
