from riplib.plugin import Plugin
import codecs
import logging
import os
import plistlib
import riplib.ccl_bplist

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
        self._name = "User Safari Download Plist"
        self._description = "Parse information from /Users/username/Library/Safari/Downloads.plist"
        self._data_file = "Downloads.plist"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
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
                        logging.warning("{0} does not exist.".format(plist))
                        print("[WARNING] {0} does not exist.".format(plist))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))
            
    def __parse_bplist(self, file, username):
        """
        Parse /Users/username/Library/Safari/Downloads.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Downloads.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave"]:
            if self._os_version in ["catalina", "mojave"]:
                # Does not exist
                pass
            elif self._os_version in ["high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "DownloadHistory" in plist:
                            of.write("Download History:\r\n")
                            for item in plist["DownloadHistory"]:
                                of.write("\tProgress Bytes So Far : {0}\r\n"
                                         .format(item["DownloadEntryProgressBytesSoFar"]))
                                of.write("\tProgress Total To Load: {0}\r\n"
                                         .format(item["DownloadEntryProgressTotalToLoad"]))
                                of.write("\tDate Added Key        : {0}\r\n"
                                         .format(item["DownloadEntryDateAddedKey"]))
                                of.write("\tDate Finished Key     : {0}\r\n"
                                         .format(item["DownloadEntryDateFinishedKey"]))
                                of.write("\tIdentifier            : {0}\r\n"
                                         .format(item["DownloadEntryIdentifier"]))
                                of.write("\tURL                   : {0}\r\n"
                                         .format(item["DownloadEntryURL"]))
                                of.write("\tRemove When Done Key  : {0}\r\n"
                                         .format(item["DownloadEntryRemoveWhenDoneKey"]))
                                of.write("\tPath                  : {0}\r\n"
                                         .format(item["DownloadEntryPath"]))
                                of.write("\r\n")
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version in ["mavericks", "mountain_lion", "lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "DownloadHistory" in plist:
                            of.write("Download History:\r\n")
                            for item in plist["DownloadHistory"]:
                                of.write("\tIdentifier            : {0}\r\n"
                                         .format(item["DownloadEntryIdentifier"]))
                                of.write("\tURL                   : {0}\r\n"
                                         .format(item["DownloadEntryURL"]))
                                of.write("\tProgress Total To Load: {0}\r\n"
                                         .format(item["DownloadEntryProgressTotalToLoad"]))
                                of.write("\tProgress Bytes So Far : {0}\r\n"
                                         .format(item["DownloadEntryProgressBytesSoFar"]))
                                of.write("\tPath                  : {0}\r\n"
                                         .format(item["DownloadEntryPath"]))
                                of.write("\r\n")
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(file):
                    try:
                        with open(file, "rb") as pl:
                            plist = plistlib.load(pl)
                            pl.close()
                        if "DownloadHistory" in plist:
                            downloads = plist["DownloadHistory"]
                            for download in downloads:
                                if "DownloadEntryURL" in download:
                                    of.write("URL                   : {0}\r\n".format(download["DownloadEntryURL"]))
                                if "DownloadEntryIdentifier" in download:
                                    of.write("Identifier            : {0}\r\n"
                                             .format(download["DownloadEntryIdentifier"]))
                                if "DownloadEntryPath" in download:
                                    of.write("Path                  : {0}\r\n"
                                             .format(download["DownloadEntryPath"]))
                                if "DownloadEntryPostPath" in download:
                                    of.write("Post Path             : {0}\r\n"
                                             .format(download["DownloadEntryPostPath"]))
                                if "DownloadEntryProgressBytesSoFar" in download:
                                    of.write("Progress Bytes So Far : {0}\r\n"
                                             .format(download["DownloadEntryProgressBytesSoFar"]))
                                if "DownloadEntryProgressTotalToLoad" in download:
                                    of.write("Progress Total To Load: {0}\r\n"
                                             .format(download["DownloadEntryProgressTotalToLoad"]))
                                of.write("\r\n")
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
