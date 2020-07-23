""" Module to parse /private/var/db/dslocal/nodes/Default/users/<username>.plist """
import codecs
import logging
import os
import plistlib
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UserAccountsPlist(Plugin):
    """
    Plugin class to parse /private/var/db/dslocal/nodes/Default/users/<username>.plist
    """
    def __init__(self):
        """
        Initialise the class. N.B. in a full implementation of a class deriving from Plugin the self.*
        values should be changed.
        """
        super().__init__()
        self.set_name("User Accounts")
        self.set_description("Base class for plugins")
        self.set_output_file("UserAccounts.txt")
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
            logging.warning("Warning /private/var/db/dslocal/nodes/Default/users does not exist.")
            print("Warning /private/var/db/dslocal/nodes/Default/users does not exist.")

    def __parse_bplist(self, file):
        """
        Parse a User Account Binary Plist files
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion"]:
                parse_os = Parse01(output_file, file)
                parse_os.parse()
            elif self._os_version == "snow_leopard":
                parse_os = Parse02(output_file, file)
                parse_os.parse()
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
        bplist = open(self._data_file, "rb")
        plist = riplib.ccl_bplist.load(bplist)
        bplist.close()
        try:
            name = None
            if "home" in plist and "/Users" in plist["home"][0]:  # Only /Users
                self._output_file.write("="*10 + " User Accounts " + "="*10 + "\r\n")
                self._output_file.write("Source File: {0}\r\n\r\n".format(self._data_file))
                if "name" in plist:
                    self._output_file.write("Name          : {0}\r\n".format(plist["name"][0]))
                    name = plist["name"][0]
                if "realname" in plist:
                    self._output_file.write("Real Name     : {0}\r\n".format(plist["realname"][0]))
                if "home" in plist:
                    self._output_file.write("Home          : {0}\r\n".format(plist["home"][0]))
                if "hint" in plist:
                    self._output_file.write("Password Hint : {0}\r\n".format(plist["hint"][0]))
                if "authentication_authority" in plist:
                    self._output_file.write("Authentication: {0}\r\n".format(plist["authentication_authority"]))
                if "uid" in plist:
                    self._output_file.write("UID           : {0}\r\n".format(plist["uid"][0]))
                if "gid" in plist:
                    self._output_file.write("GID           : {0}\r\n".format(plist["gid"][0]))
                if "generateduid" in plist:
                    self._output_file.write("Generated UID : {0}\r\n".format(plist["generateduid"][0]))
                if "shell" in plist:
                    self._output_file.write("Shell         : {0}\r\n".format(plist["shell"][0]))
                if "picture" in plist:
                    self._output_file.write("Picture       : {0}\r\n".format(plist["picture"][0]))
                if "jpegphoto" in plist and name is not None:
                    output_dir = os.path.dirname(self._output_file)
                    jpeg = os.path.join(output_dir, "UserAccounts-" + name + "-jpgphoto.jpg")
                    with open(jpeg, "wb") as jpeg_output_file:
                        jpeg_output_file.write(plist["jpegphoto"][0])
                        jpeg_output_file.close()
                        jpeg_output_file.write("Logon Picture : {0}\r\n".format(jpeg))
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
        # Snow Leopard uses plain plists
        with open(self._data_file, 'rb') as plist_to_load:
            plist = plistlib.load(plist_to_load)
        plist_to_load.close()
        try:
            name = None
            if "home" in plist and "/Users" in plist["home"][0]:  # Only /Users
                self._output_file.write("="*10 + " User Accounts " + "="*10 + "\r\n")
                self._output_file.write("Source File: {0}\r\n\r\n".format(self._data_file))
                if "name" in plist:
                    self._output_file.write("Name          : {0}\r\n".format(plist["name"][0]))
                    name = plist["name"][0]
                if "realname" in plist:
                    self._output_file.write("Real Name     : {0}\r\n".format(plist["realname"][0]))
                if "home" in plist:
                    self._output_file.write("Home          : {0}\r\n".format(plist["home"][0]))
                if "hint" in plist:
                    self._output_file.write("Password Hint : {0}\r\n".format(plist["hint"][0]))
                if "authentication_authority" in plist:
                    self._output_file.write("Authentication: {0}\r\n".format(plist["authentication_authority"]))
                if "uid" in plist:
                    self._output_file.write("UID           : {0}\r\n".format(plist["uid"][0]))
                if "gid" in plist:
                    self._output_file.write("GID           : {0}\r\n".format(plist["gid"][0]))
                if "generateduid" in plist:
                    self._output_file.write("Generated UID : {0}\r\n".format(plist["generateduid"][0]))
                if "shell" in plist:
                    self._output_file.write("Shell         : {0}\r\n".format(plist["shell"][0]))
                if "picture" in plist:
                    self._output_file.write("Picture       : {0}\r\n".format(plist["picture"][0]))
                if "jpegphoto" in plist and name is not None:
                    output_dir = os.path.dirname(self._output_file)
                    jpeg = os.path.join(output_dir, "UserAccounts-" + name + "-jpgphoto.jpg")
                    with open(jpeg, "wb") as jpeg_output_file:
                        jpeg_output_file.write(plist["jpegphoto"][0])
                        jpeg_output_file.close()
                        jpeg_output_file.write("Logon Picture : {0}\r\n".format(jpeg))
            else:
                return
        except KeyError:
            pass
