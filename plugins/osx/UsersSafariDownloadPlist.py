""" Module tp parse Downloads plist """
import codecs
import logging
import os
import plistlib
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersSafariDownloadPlist(Plugin):
    """
    Parse information from /Users/username/Library/Safari/Downloads.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Safari Download Plist")
        self.set_description("Parse information from /Users/username/Library/Safari/Downloads.plist")
        self.set_data_file("Downloads.plist")
        self.set_output_file("")  # this will have to be defined per user account
        self.set_type("bplist")

    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    plist = os.path.join(users_path, username, "Library", "Safari", self._data_file)
                    if os.path.isfile(plist):
                        self.__parse_bplist(plist, username)
                    else:
                        logging.warning("%s does not exist.", plist)
                        print("[WARNING] {0} does not exist.".format(plist))
        else:
            logging.warning("%s does not exist.", users_path)
            print("[WARNING] {0} does not exist.".format(users_path))

    def __parse_bplist(self, file, username):
        """
        Parse /Users/username/Library/Safari/Downloads.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Downloads.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["big_sur", "catalina", "mojave"]:
                # Does not exist
                pass
            elif self._os_version in ["high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    parse_os = ParseVers10131010(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version in ["mavericks", "mountain_lion", "lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    parse_os = ParseVers109107(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(file):
                    with open(file, "rb") as plist_to_load:
                        plist = plistlib.load(plist_to_load)
                        plist_to_load.close()
                        parse_os = ParseVer106(output_file, plist)
                        parse_os.parse()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()

class ParseVers10131010():
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
            if "DownloadHistory" in self._data_file:
                self._output_file.write("Download History:\r\n")
                for item in self._data_file["DownloadHistory"]:
                    self._output_file.write("\tProgress Bytes So Far : {0}\r\n".format(item["DownloadEntryProgressBytesSoFar"]))
                    self._output_file.write("\tProgress Total To Load: {0}\r\n".format(item["DownloadEntryProgressTotalToLoad"]))
                    self._output_file.write("\tDate Added Key        : {0}\r\n".format(item["DownloadEntryDateAddedKey"]))
                    self._output_file.write("\tDate Finished Key     : {0}\r\n".format(item["DownloadEntryDateFinishedKey"]))
                    self._output_file.write("\tIdentifier            : {0}\r\n".format(item["DownloadEntryIdentifier"]))
                    self._output_file.write("\tURL                   : {0}\r\n".format(item["DownloadEntryURL"]))
                    self._output_file.write("\tRemove When Done Key  : {0}\r\n".format(item["DownloadEntryRemoveWhenDoneKey"]))
                    self._output_file.write("\tPath                  : {0}\r\n".format(item["DownloadEntryPath"]))
                    self._output_file.write("\r\n")
        except KeyError:
            pass

class ParseVers109107():
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
            if "DownloadHistory" in self._data_file:
                self._output_file.write("Download History:\r\n")
                for item in self._data_file["DownloadHistory"]:
                    self._output_file.write("\tIdentifier            : {0}\r\n".format(item["DownloadEntryIdentifier"]))
                    self._output_file.write("\tURL                   : {0}\r\n".format(item["DownloadEntryURL"]))
                    self._output_file.write("\tProgress Total To Load: {0}\r\n".format(item["DownloadEntryProgressTotalToLoad"]))
                    self._output_file.write("\tProgress Bytes So Far : {0}\r\n".format(item["DownloadEntryProgressBytesSoFar"]))
                    self._output_file.write("\tPath                  : {0}\r\n".format(item["DownloadEntryPath"]))
                    self._output_file.write("\r\n")
        except KeyError:
            pass

class ParseVer106():
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
            if "DownloadHistory" in self._data_file:
                downloads = self._data_file["DownloadHistory"]
                for download in downloads:
                    if "DownloadEntryURL" in download:
                        self._output_file.write("URL                   : {0}\r\n".format(download["DownloadEntryURL"]))
                    if "DownloadEntryIdentifier" in download:
                        self._output_file.write("Identifier            : {0}\r\n".format(download["DownloadEntryIdentifier"]))
                    if "DownloadEntryPath" in download:
                        self._output_file.write("Path                  : {0}\r\n".format(download["DownloadEntryPath"]))
                    if "DownloadEntryPostPath" in download:
                        self._output_file.write("Post Path             : {0}\r\n".format(download["DownloadEntryPostPath"]))
                    if "DownloadEntryProgressBytesSoFar" in download:
                        self._output_file.write("Progress Bytes So Far : {0}\r\n".format(download["DownloadEntryProgressBytesSoFar"]))
                    if "DownloadEntryProgressTotalToLoad" in download:
                        self._output_file.write("Progress Total To Load: {0}\r\n".format(download["DownloadEntryProgressTotalToLoad"]))
                    self._output_file.write("\r\n")
        except KeyError:
            pass
