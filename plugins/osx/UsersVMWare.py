from riplib.Plugin import Plugin
import codecs
import logging
import os

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersVMWare(Plugin):
    """
    Parse information from /Users/{username}/Library/Application Support/VMware Fusion/vmInventory
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "VMware Inventory listing File"
        self._description = "Parse information from " \
                            "/Users/{username}/Library/Application Support/VMware Fusion/vmInventory file"
        self._data_file = "vmInventory"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "file"
    
    def parse(self):
        """
        Find the inventory listing file
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    inventory = os.path\
                        .join(users_path, username, "Library", "Application Support", "VMware Fusion", self._data_file)
                    if os.path.isfile(inventory):
                        self.__parse_config(inventory, username)
                    else:
                        logging.warning("{0} does not exist.".format(inventory))
                        print("[WARNING] {0} does not exist.".format(inventory))
        else:
            print("[WARNING] {0} does not exist.".format(users_path))
            
    def __parse_config(self, file, username):
        """
        /Users/{username}/Library/Application Support/VMware Fusion/vmInventory file
        N.B. OSX version checking removed as this is a common directory and file across versions
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_VMware_inventory.txt"), "a",
                         encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                inventory_file = codecs.open(file, "r", encoding="utf-8")
                for lines in inventory_file:
                    of.write(lines.replace("\n", "\r\n"))
                inventory_file.close()
            else:
                logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            of.write("="*40 + "\r\n\r\n")
        of.close()
