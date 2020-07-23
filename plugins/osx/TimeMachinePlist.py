""" Module to parse /Library/Preferences/com.apple.TimeMachine.plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class TimeMachinePlist(Plugin):
    """
    Plugin to parse /Library/Preferences/com.apple.TimeMachine.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("TimeMachine")
        self.set_description("Parse data from /Library/Preferences/com.apple.TimeMachine.plist")
        self.set_data_file("com.apple.TimeMachine.plist")
        self.set_output_file("TimeMachine.txt")
        self.set_type("bplist")

    def parse(self):
        """
        Parse /Library/Preferences/com.apple.TimeMachine.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                plist = riplib.ccl_bplist.load(bplist)
                bplist.close()
            else:
                logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
                output_file.close()
                return

            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                parse_os = Parse01(output_file, plist)
                parse_os.parse()
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                parse_os = Parse02(output_file, plist)
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
        try:
            if "LastDestinationID" in self._data_file:
                self._output_file.write("Last Destination ID             : {0}\r\n".format(self._data_file["LastDestinationID"]))
            if "LocalizedDiskImageVolumeName" in self._data_file:
                self._output_file.write("Localized Disk Image Volume Name: {0}\r\n".format(self._data_file["LocalizedDiskImageVolumeName"]))
            if "SkipSystemFiles" in self._data_file:
                self._output_file.write("Skip System Files               : {0}\r\n".format(self._data_file["SkipSystemFiles"]))
            if "PreferencesVersion" in self._data_file:
                self._output_file.write("Preferences Version             : {0}\r\n".format(self._data_file["PreferencesVersion"]))
            if "HostUUIDs" in self._data_file:
                self._output_file.write("Host UUIDs:\r\n")
                for host_uuid in self._data_file["HostUUIDs"]:
                    self._output_file.write("\t{0}\r\n".format(host_uuid))
            if "Destinations" in self._data_file:
                self._output_file.write("Destinations:\r\n")
                for destination in self._data_file["Destinations"]:
                    if "LastKnownEncryptionState" in destination:
                        self._output_file.write("\tLast Known Encryption State      : {0}\r\n".format(destination["LastKnownEncryptionState"]))
                    if "RESULT" in destination:
                        self._output_file.write("\tRESULT                           : {0}\r\n".format(destination["RESULT"]))
                    if "BytesUsed" in destination:
                        self._output_file.write("\tBytes Used                       : {0}\r\n".format(destination["BytesUsed"]))
                    if "BytesAvailable" in destination:
                        self._output_file.write("\tBytes Available                  : {0}\r\n".format(destination["BytesAvailable"]))
                    if "RootVolumeUUID" in destination:
                        self._output_file.write("\tRoot Volume UUID                 : {0}\r\n".format(destination["RootVolumeUUID"]))
                    if "AlwaysShowDeletedBackupsWarning" in self._data_file:
                        self._output_file.write("Always Show Deleted Backups Warning: {0}\r\n".format(self._data_file["AlwaysShowDeletedBackupsWarning"]))
                    if "AutoBackup" in self._data_file:
                        self._output_file.write("AutoBackup                         : {0}\r\n".format(self._data_file["AutoBackup"]))
                    if "LastConfigurationTraceDate" in self._data_file:
                        self._output_file.write("Last Configuration Trace Date      : {0}\r\n".format(self._data_file["LastConfigurationTraceDate"]))
                    if "DestinationID" in destination:
                        self._output_file.write("\tDestination ID                   : {0}\r\n".format(destination["DestinationID"]))
                    if "DestinationUUIDs" in destination:
                        self._output_file.write("Destination UUIDs:\r\n")
                        for dest_uuid in destination["DestinationUUIDs"]:
                            self._output_file.write("\t\t{0}\r\n".format(dest_uuid))
                    if "SnapshotDates" in destination:
                        self._output_file.write("Snapshot Dates:\r\n")
                        for snap_date in destination["SnapshotDates"]:
                            self._output_file.write("\t\t{0}\r\n".format(snap_date))
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
            if "MobileBackups" in self._data_file:
                self._output_file.write("MobileBackups                      : {0}\r\n".format(self._data_file["MobileBackups"]))
            if "SkipSystemFiles" in self._data_file:
                self._output_file.write("Skip System Files                  : {0}\r\n".format(self._data_file["SkipSystemFiles"]))
            if "PreferencesVersion" in self._data_file:
                self._output_file.write("Preferences Version                : {0}\r\n".format(self._data_file["PreferencesVersion"]))
            if "AutoBackup" in self._data_file:
                self._output_file.write("AutoBackup                         : {0}\r\n".format(self._data_file["AutoBackup"]))
            if "RequiresACPower" in self._data_file:
                self._output_file.write("Requires AC Power                  : {0}\r\n".format(self._data_file["RequiresACPower"]))
            if "AlwaysShowDeletedBackupsWarning" in self._data_file:
                self._output_file.write("Always Show Deleted Backups Warning: {0}\r\n".format(self._data_file["AlwaysShowDeletedBackupsWarning"]))
            if "RootVolumeUUID" in self._data_file:
                self._output_file.write("Root Volume UUID                   : {0}\r\n".format(self._data_file["RootVolumeUUID"]))
            if "LastDestinationID" in self._data_file:
                self._output_file.write("Last Destination ID                : {0}\r\n".format(self._data_file["LastDestinationID"]))
            if "LocalizedDiskImageVolumeName" in self._data_file:
                self._output_file.write("Localized DiskImag eVolume Name    : {0}\r\n".format(self._data_file["LocalizedDiskImageVolumeName"]))
            if "HostUUIDs" in self._data_file:
                self._output_file.write("Host UUIDs:\r\n")
                for host_uuid in self._data_file["HostUUIDs"]:
                    self._output_file.write("\t{0}\r\n".format(host_uuid))
            if "SkipPaths" in self._data_file:
                self._output_file.write("Skip Paths:\r\n")
                for skip_path in self._data_file["SkipPaths"]:
                    self._output_file.write("\t{0}\r\n".format(skip_path))
            if "ExcludedVolumeUUIDs" in self._data_file:
                self._output_file.write("Excluded Volume UUIDs:\r\n")
                for exc_vol_uuid in self._data_file["ExcludedVolumeUUIDs"]:
                    self._output_file.write("\t{0}\r\n".format(exc_vol_uuid))
            if "IncludeByPath" in self._data_file:
                self._output_file.write("Include By Path:\r\n")
                for inc_path in self._data_file["IncludeByPath"]:
                    self._output_file.write("\t{0}\r\n".format(inc_path))
            if "Destinations" in self._data_file:
                self._output_file.write("Destinations:\r\n")
                for destination in self._data_file["Destinations"]:
                    if "RESULT" in destination:
                        self._output_file.write("\tRESULT         : {0}\r\n".format(destination["RESULT"]))
                    if "BytesUsed" in destination:
                        self._output_file.write("\tBytes Used     : {0}\r\n".format(destination["BytesUsed"]))
                    if "BytesAvailable" in destination:
                        self._output_file.write("\tBytes Available: {0}\r\n".format(destination["BytesAvailable"]))
                    if "DestinationID" in destination:
                        self._output_file.write("\tDestination ID : {0}\r\n".format(destination["DestinationID"]))
                    if "SnapshotCount" in destination:
                        self._output_file.write("\tSnapshot Count : {0}\r\n".format(destination["SnapshotCount"]))
                    if "DestinationUUIDs" in destination:
                        self._output_file.write("Destination UUIDs:\r\n")
                        for dest_uuid in destination["DestinationUUIDs"]:
                            self._output_file.write("\t\t{0}\r\n".format(dest_uuid))
                    if "SnapshotDates" in destination:
                        self._output_file.write("Snapshot Dates:\r\n")
                        for snap_date in destination["SnapshotDates"]:
                            self._output_file.write("\t\t{0}\r\n".format(snap_date))
                    self._output_file.write("\r\n")
        except KeyError:
            pass
