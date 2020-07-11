from riplib.Plugin import Plugin

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
        self._name = "Summary"
        self._description = "Parse data for system summary"
        self._output_file = "OSXRipper_Summary.txt"
        self._type = "multiple"

    def parse(self):

        smb_server = SmbServer.SmbServer()
        smb_server._output_file = self._output_file
        smb_server.set_os_version(self._os_version)
        smb_server.set_input_directory(self._input_dir)
        smb_server.set_output_directory(self._output_dir)
        smb_server.parse()

        dhcp_clients = DhcpLeasesPlist.DhcpLeasesPlist()
        dhcp_clients._output_file = self._output_file
        dhcp_clients.set_os_version(self._os_version)
        dhcp_clients.set_input_directory(self._input_dir)
        dhcp_clients.set_output_directory(self._output_dir)
        dhcp_clients.parse()

        system_time = SystemTime.SystemTime()
        system_time._output_file = self._output_file
        system_time.set_os_version(self._os_version)
        system_time.set_input_directory(self._input_dir)
        system_time.set_output_directory(self._output_dir)
        system_time.parse()

        user_accounts = UserAccountsPlist.UserAccountsPlist()
        user_accounts._output_file = self._output_file
        user_accounts.set_os_version(self._os_version)
        user_accounts.set_input_directory(self._input_dir)
        user_accounts.set_output_directory(self._output_dir)
        user_accounts.parse()

        playlists = PlayLists.Playlists()
        playlists._output_file = self._output_file
        playlists.set_os_version(self._os_version)
        playlists.set_input_directory(self._input_dir)
        playlists.set_output_directory(self._output_dir)
        playlists.parse()

        time_machine = TimeMachinePlist.TimeMachinePlist()
        time_machine._output_file = self._output_file
        time_machine.set_os_version(self._os_version)
        time_machine.set_input_directory(self._input_dir)
        time_machine.set_output_directory(self._output_dir)
        time_machine.parse()

        bluetooth = BluetoothPlist.BluetoothPlist()
        bluetooth._output_file = self._output_file
        bluetooth.set_os_version(self._os_version)
        bluetooth.set_input_directory(self._input_dir)
        bluetooth.set_output_directory(self._output_dir)
        bluetooth.parse()

        install_history = InstallHistory.InstallHistory()
        install_history._output_file = self._output_file
        install_history.set_os_version(self._os_version)
        install_history.set_input_directory(self._input_dir)
        install_history.set_output_directory(self._output_dir)
        install_history.parse()
