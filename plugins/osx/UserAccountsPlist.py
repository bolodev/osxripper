from riplib.plugin import Plugin
import codecs
import logging
import os
import plistlib
import riplib.ccl_bplist

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
        self._name = "User Accounts"
        self._description = "Base class for plugins"
        self._output_file = "UserAccounts.txt"
        self._data_file = ""  # In this case multiple files are being searched for across different directories
        self._type = "bplist"
        
    def parse(self): 
        """
        Public function called to parse the data file set in __init__
        """
        working_dir = os.path.join(self._input_dir, "private", "var", "db", "dslocal", "nodes", "Default", "users")
        if os.path.exists(working_dir):
            file_listing = os.listdir(working_dir)
            for f in file_listing:
                stat_info = os.stat(working_dir + os.path.sep + f)
                if f.endswith(".plist") and stat_info.st_size > 0:
                    test_plist = os.path.join(working_dir, f)
                    self.__parse_bplist(test_plist)
        else:
            print("Warning /private/var/db/dslocal/nodes/Default/users does not exist.")

    def __parse_bplist(self, file):
        """
        Parse a User Account Binary Plist files
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        name = None
                        if "home" in pl and "/Users" in pl["home"][0]:  # Only /Users
                            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                            of.write("Source File: {0}\r\n\r\n".format(file))
                            if "name" in pl:
                                of.write("Name          : {0}\r\n".format(pl["name"][0]))
                                name = pl["name"][0]
                            if "realname" in pl:
                                of.write("Real Name     : {0}\r\n".format(pl["realname"][0]))
                            if "home" in pl:
                                of.write("Home          : {0}\r\n".format(pl["home"][0]))
                            if "hint" in pl:
                                of.write("Password Hint : {0}\r\n".format(pl["hint"][0]))
                            if "authentication_authority" in pl:
                                of.write("Authentication: {0}\r\n".format(pl["authentication_authority"]))
                            if "uid" in pl:
                                of.write("UID           : {0}\r\n".format(pl["uid"][0]))
                            if "gid" in pl:
                                of.write("GID           : {0}\r\n".format(pl["gid"][0]))
                            if "generateduid" in pl:
                                of.write("Generated UID : {0}\r\n".format(pl["generateduid"][0]))
                            if "shell" in pl:
                                of.write("Shell         : {0}\r\n".format(pl["shell"][0]))
                            if "picture" in pl:
                                of.write("Picture       : {0}\r\n".format(pl["picture"][0]))
                            if "jpegphoto" in pl and name is not None:
                                jpeg = os.path.join(self._output_dir, "UserAccounts-" + name + "-jpgphoto.jpg")
                                with open(jpeg, "wb") as jof:
                                    jof.write(pl["jpegphoto"][0])
                                    jof.close()
                                    of.write("Logon Picture : {0}\r\n".format(jpeg))
                        else:
                            return
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                # Snow Leopard uses plain plists
                with open(file, 'rb') as pl:
                    try:
                        name = None
                        plist = plistlib.load(pl)
                        pl.close()
                        if "home" in plist and "/Users" in plist["home"][0]:  # Only /Users
                            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                            of.write("Source File: {0}\r\n\r\n".format(file))
                            if "name" in plist:
                                of.write("Name          : {0}\r\n".format(plist["name"][0]))
                                name = plist["name"][0]
                            if "realname" in plist:
                                of.write("Real Name     : {0}\r\n".format(plist["realname"][0]))
                            if "home" in plist:
                                of.write("Home          : {0}\r\n".format(plist["home"][0]))
                            if "hint" in plist:
                                of.write("Password Hint : {0}\r\n".format(plist["hint"][0]))
                            if "authentication_authority" in plist:
                                of.write("Authentication: {0}\r\n".format(plist["authentication_authority"]))
                            if "uid" in plist:
                                of.write("UID           : {0}\r\n".format(plist["uid"][0]))
                            if "gid" in plist:
                                of.write("GID           : {0}\r\n".format(plist["gid"][0]))
                            if "generateduid" in plist:
                                of.write("Generated UID : {0}\r\n".format(plist["generateduid"][0]))
                            if "shell" in plist:
                                of.write("Shell         : {0}\r\n".format(plist["shell"][0]))
                            if "picture" in plist:
                                of.write("Picture       : {0}\r\n".format(plist["picture"][0]))
                            if "jpegphoto" in plist and name is not None:
                                jpeg = os.path.join(self._output_dir, "UserAccounts-" + name + "-jpgphoto.jpg")
                                with open(jpeg, "wb") as jof:
                                    jof.write(plist["jpegphoto"][0])
                                    jof.close()
                                    of.write("Logon Picture : {0}\r\n".format(jpeg))
                        else:
                            return
                    except KeyError:
                        pass
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
