""" Module for the quick summary plugin """
from riplib.plugin import Plugin

import plugins.osx.SmbServer as SmbServer
import plugins.osx.DhcpLeasesPlist as DhcpLeasesPlist
import plugins.osx.SystemTime as SystemTime
import plugins.osx.UserAccountsPlist as UserAccountsPlist
import plugins.osx.Playlists as PlayLists
import plugins.osx.TimeMachinePlist as TimeMachinePlist
import plugins.osx.BluetoothPlist as BluetoothPlist
import plugins.osx.InstallHistory as InstallHistory

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class Summary(Plugin):
    """
    Plugin to output a summary of the system
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Summary")
        self.set_description("Parse data for system summary")
        self.set_output_file("OSXRipper_Summary.txt")
        self.set_type("multiple")

    def parse(self):

        smb_server = SmbServer.SmbServer()
        smb_server.set_output_file(self.get_output_file)
        smb_server.set_os_version(self.get_os_version)
        smb_server.set_input_directory(self.get_input_dir)
        smb_server.set_output_directory(self.get_output_dir)
        smb_server.parse()

        dhcp_clients = DhcpLeasesPlist.DhcpLeasesPlist()
        dhcp_clients.set_output_file(self.get_output_file)
        dhcp_clients.set_os_version(self.get_os_version)
        dhcp_clients.set_input_directory(self.get_input_dir)
        dhcp_clients.set_output_directory(self.get_output_dir)
        dhcp_clients.parse()

        system_time = SystemTime.SystemTime()
        system_time.set_output_file(self.get_output_file)
        system_time.set_os_version(self.get_os_version)
        system_time.set_input_directory(self.get_input_dir)
        system_time.set_output_directory(self.get_output_dir)
        system_time.parse()

        user_accounts = UserAccountsPlist.UserAccountsPlist()
        user_accounts.set_output_file(self.get_output_file)
        user_accounts.set_os_version(self.get_os_version)
        user_accounts.set_input_directory(self.get_input_dir)
        user_accounts.set_output_directory(self.get_output_dir)
        user_accounts.parse()

        playlists = PlayLists.Playlists()
        playlists.set_output_file(self._output_file)
        playlists.set_os_version(self.get_os_version)
        playlists.set_input_directory(self.get_input_dir)
        playlists.set_output_directory(self.get_output_dir)
        playlists.parse()

        time_machine = TimeMachinePlist.TimeMachinePlist()
        time_machine.set_output_file(self.get_output_file)
        time_machine.set_os_version(self.get_os_version)
        time_machine.set_input_directory(self.get_input_dir)
        time_machine.set_output_directory(self.get_output_dir)
        time_machine.parse()

        bluetooth = BluetoothPlist.BluetoothPlist()
        bluetooth.set_output_file(self.get_output_file)
        bluetooth.set_os_version(self.get_os_version)
        bluetooth.set_input_directory(self.get_input_dir)
        bluetooth.set_output_directory(self.get_output_dir)
        bluetooth.parse()

        install_history = InstallHistory.InstallHistory()
        install_history.set_output_file(self.get_output_file)
        install_history.set_os_version(self.get_os_version)
        install_history.set_input_directory(self.get_input_dir)
        install_history.set_output_directory(self.get_output_dir)
        install_history.parse()
