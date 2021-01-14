""" Module to parse Safari TopSites plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersSafariTopSites(Plugin):
    """
    Parse information from /Users/username/Library/Safari/TopSites.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("User Safari Top Sites")
        self.set_description("Parse information from /Users/username/Library/Safari/TopSites.plist")
        self.set_data_file("TopSites.plist")
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
        Parse /Users/username/Library/Safari/LastSession.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Top_Sites.txt"), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
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
                try:
                    if "DisplayedSitesLastModified" in plist:
                        output_file.write("Displayed Sites Last Modified: {0}\r\n\r\n".format(plist["DisplayedSitesLastModified"]))
                    if "TopSites" in plist:
                        output_file.write("Top Sites:\r\n")
                        for top_site in plist["TopSites"]:
                            if "TopSiteIsBuiltIn" in top_site:
                                output_file.write("\tIs Built In: {0}\r\n".format(top_site["TopSiteIsBuiltIn"]))
                            if "TopSiteURLString" in top_site:
                                output_file.write("\tURL String : {0}\r\n".format(top_site["TopSiteURLString"]))
                            if "TopSiteTitle" in top_site:
                                output_file.write("\tTitle      : {0}\r\n".format(top_site["TopSiteTitle"]))
                            output_file.write("\r\n")
                    output_file.write("\r\n")
                except KeyError:
                    pass
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
