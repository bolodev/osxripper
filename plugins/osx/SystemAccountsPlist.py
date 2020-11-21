""" Module to parse user plists """
import codecs
import logging
import os
import plistlib
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemAccountsPlist(Plugin):
    """
    Plugin class to parse /private/var/db/dslocal/nodes/Default/users/<username>.plist
    """
    def __init__(self):
        """
        Initialise the class. N.B. in a full implementation of a class deriving from Plugin the self.*
        values should be changed.
        """
        super().__init__()
        self.set_name("System Accounts")
        self.set_description("Base class for plugins")
        self.set_output_file("SystemAccounts.txt")
        self.set_data_file("")  # In this case multiple files are being searched for across different directories
        self.set_type("bplist")

    def parse(self):
        """
        Public function called to parse the data file set in __init__
        """
        working_dir = os.path.join(self._input_dir, "private", "var", "db", "dslocal", "nodes", "Default", "users")
        if os.path.exists(working_dir):
            file_listing = os.listdir(working_dir)
            for file_name in file_listing:
                stat_info = os.stat(working_dir + os.path.sep + file_name)
                if file_name.endswith(".plist") and stat_info.st_size > 0:
                    test_plist = os.path.join(working_dir, file_name)
                    self.__parse_bplist(test_plist)
                else:
                    print("[INFO] User Plist {0} is zero length.".format(file_name))
                    logging.info("User Plist is zero length.")
        else:
            print("[WARNING] /private/var/db/dslocal/nodes/Default/users does not exist")

    def __parse_bplist(self, file):
        """
        Parse a User Account Binary Plist files
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            #                         "mavericks", "mountain_lion", "lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    output_file.write("{0} {1} {0}\r\n".format("="*10, output_file))
                    output_file.write("Source File: {0}\r\n\r\n".format(file))
                    parse_os = Parse01(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                with open(file, 'rb') as plist_to_load:
                    try:
                        # Snow Leopard uses plain plists
                        plist = plistlib.load(plist_to_load)
                        # output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                        output_file.write("{0} {1} {0}\r\n".format("="*10, output_file))
                        output_file.write("Source File: {0}\r\n\r\n".format(file))
                        parse_os = Parse02(output_file, plist)
                        parse_os.parse()
                    except IOError as error:
                        logging.error("IOError: %s", error.args)
                        print("[ERROR] {0}".format(error.args))
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
            if "home" in self._data_file and "/var" in self._data_file["home"][0]:  # Only /var based system accounts
                if "name" in self._data_file:
                    self._output_file.write("Name          : {0}\r\n".format(self._data_file["name"][0]))
                if "realname" in self._data_file:
                    self._output_file.write("Real Name     : {0}\r\n".format(self._data_file["realname"][0]))
                if "home" in self._data_file:
                    self._output_file.write("Home          : {0}\r\n".format(self._data_file["home"][0]))
                if "hint" in self._data_file:
                    self._output_file.write("Password Hint : {0}\r\n".format(self._data_file["hint"][0]))
                if "authentication_authority" in self._data_file:
                    self._output_file.write("Authentication: {0}\r\n".format(self._data_file["authentication_authority"]))
                if "uid" in self._data_file:
                    self._output_file.write("UID           : {0}\r\n".format(self._data_file["uid"][0]))
                if "gid" in self._data_file:
                    self._output_file.write("GID           : {0}\r\n".format(self._data_file["gid"][0]))
                if "generateduid" in self._data_file:
                    self._output_file.write("Generated UID : {0}\r\n".format(self._data_file["generateduid"][0]))
                if "shell" in self._data_file:
                    self._output_file.write("Shell         : {0}\r\n".format(self._data_file["shell"][0]))
                if "picture" in self._data_file:
                    self._output_file.write("Picture       : {0}\r\n".format(self._data_file["picture"][0]))
            else:
                return
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
            if "home" in self._data_file and "/var" in self._data_file["home"][0]:  # Only /var based system accounts
                if "name" in self._data_file:
                    self._output_file.write("Name          : {0}\r\n".format(self._data_file["name"][0]))
                if "realname" in self._data_file:
                    self._output_file.write("Real Name     : {0}\r\n".format(self._data_file["realname"][0]))
                if "home" in self._data_file:
                    self._output_file.write("Home          : {0}\r\n".format(self._data_file["home"][0]))
                if "hint" in self._data_file:
                    self._output_file.write("Password Hint : {0}\r\n".format(self._data_file["hint"][0]))
                if "authentication_authority" in self._data_file:
                    self._output_file.write("Authentication: {0}\r\n".format(self._data_file["authentication_authority"]))
                if "uid" in self._data_file:
                    self._output_file.write("UID           : {0}\r\n".format(self._data_file["uid"][0]))
                if "gid" in self._data_file:
                    self._output_file.write("GID           : {0}\r\n".format(self._data_file["gid"][0]))
                if "generateduid" in self._data_file:
                    self._output_file.write("Generated UID : {0}\r\n".format(self._data_file["generateduid"][0]))
                if "shell" in self._data_file:
                    self._output_file.write("Shell         : {0}\r\n".format(self._data_file["shell"][0]))
                if "picture" in self._data_file:
                    self._output_file.write("Picture       : {0}\r\n".format(self._data_file["picture"][0]))
            else:
                return
        except IOError as error:
            logging.error("IOError: %s", error.args)
            print("[ERROR] {0}".format(error.args))
        except KeyError:
            pass
