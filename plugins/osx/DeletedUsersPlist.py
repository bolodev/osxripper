""" Module to parse data from accounts.plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class DeletedUsersPlist(Plugin):
    """
    Plugin to parse /Library/Preferences/com.apple.preferences.accounts.plist
    """

    def __init__(self):
        """
        Initialise plugins
        """
        super().__init__()
        self.set_name("Deleted Users")
        self.set_description("List deleted users")
        self.set_data_file("com.apple.preferences.accounts.plist")
        self.set_output_file("DeletedUsers.txt")
        self.set_type("bplist")

    def parse(self):
        """
        Parse bplist com.apple.preferences.accounts.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
            #                         "mavericks", "mountain_lion", "lion","snow_leopard"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist_to_load = riplib.ccl_bplist.load(bplist)
                    try:
                        if "deletedUsers" in plist_to_load:
                            user_array = plist_to_load["deletedUsers"]
                            for user in user_array:
                                output_file.write("Real Name: {0}\r\n".format(user["dsAttrTypeStandard:RealName"]))
                                output_file.write("Name     : {0}\r\n".format(user["name"]))
                                output_file.write("Date     : {0}\r\n".format(user["date"]))
                                output_file.write("UID      : {0}\r\n".format(user["dsAttrTypeStandard:UniqueID"]))
                                output_file.write("\r\n")
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: %s does not exist or cannot be found.", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()
