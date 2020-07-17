""" Module for parsing bluetooth data """
import binascii
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class BluetoothPlist(Plugin):
    """
    Plugin class to parse /Library/Preferences/com.apple.Bluetooth.plist
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Bluetooth Settings")
        self.set_description("Parse bluetooth connection data.")
        self.set_output_file("Networking.txt")
        self.set_data_file("com.apple.Bluetooth.plist")
        self.set_type("bplist")

    def parse(self):
        """
        /Library/Preferences/com.apple.Bluetooth.plist
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
            logging.warning("File: %s does not exist or cannot be found.", file)
            output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            output_file.close()
            return

        # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
        if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
            parse_macOS = Parse01(output_file, plist)
            parse_macOS.parse()
        elif self._os_version == "mavericks":
            parse_macOS = Parse02(output_file, plist)
            parse_macOS.parse()
        elif self._os_version == "mountain_lion":
            parse_macOS = Parse03(output_file, plist)
            parse_macOS.parse()
        elif self._os_version == "lion":
            parse_macOS = Parse04(output_file, plist)
            parse_macOS.parse()
        elif self._os_version == "snow_leopard":
            parse_macOS = Parse05(output_file, plist)
            parse_macOS.parse()
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
            if "BluetoothVersionNumber" in self._data_file:
                self._output_file.write("Bluetooth Version Number: {0}\r\n".format(self._data_file["BluetoothVersionNumber"]))

            if "IgnoredDevices" in self._data_file:
                if len(self._data_file["IgnoredDevices"]) == 0:
                    self._output_file.write("Ignored Devices:\r\n\tNo ignored devices listed.\r\n")
                else:
                    self._output_file.write("Ignored Devices:\r\n")
                    for item in self._data_file["IgnoredDevices"]:
                        self._output_file.write("\tDevice: {0}\r\n".format(item))

            if "BRPairedDevices" in self._data_file:
                if len(self._data_file["BRPairedDevices"]) == 0:
                    self._output_file.write("BR Paired Devices:\r\n\tNo paired devices listed.\r\n")
                else:
                    self._output_file.write("BR Paired Devices:\r\n")
                    for item in self._data_file["BRPairedDevices"]:
                        self._output_file.write("\tDevice: {0}\r\n".format(item))

            if "ControllerPowerState" in self._data_file:
                self._output_file.write("Controller Power State: {0}\r\n".format(self._data_file["BluetoothVersionNumber"]))

            if "HIDDevices" in self._data_file:
                if len(self._data_file["HIDDevices"]) == 0:
                    self._output_file.write("HID Devices:\r\n\tNo paired devices listed.\r\n")
                else:
                    self._output_file.write("HID Devices:\r\n")
                    for item in self._data_file["HIDDevices"]:
                        self._output_file.write("\tDevice: {0}\r\n".format(item))

            # PersistentPorts NOTHING OF INTEREST?????

            if "DeviceCache" in self._data_file:
                for device in self._data_file["DeviceCache"]:
                    self._output_file.write("Device Cache\r\n")
                    self._output_file.write("\tDevice: {0}\r\n".format(device))

                    if "VendorID" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tVendor ID: {0}\r\n".format(self._data_file["DeviceCache"][device]["VendorID"]))

                    if "Name" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tName: {0}\r\n".format(self._data_file["DeviceCache"][device]["Name"]))

                    if "LMPSubversion" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tLMP Subversion: {0}\r\n".format(self._data_file["DeviceCache"][device]["LMPSubversion"]))

                    if "PageScanPeriod" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tPage Scan Period: {0}\r\n".format(self._data_file["DeviceCache"][device]["PageScanPeriod"]))

                    if "LastNameUpdate" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tLast Name Update: {0}\r\n".format(self._data_file["DeviceCache"][device]["LastNameUpdate"]))

                    if "SupportedFeatures" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tSupported Features: {0}\r\n".format(binascii.hexlify(self._data_file["DeviceCache"][device]["SupportedFeatures"])))

                    if "ProductID" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tProduct ID: {0}\r\n".format(self._data_file["DeviceCache"][device]["ProductID"]))

                    if "LMPVersion" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tLMP Version: {0}\r\n".format(self._data_file["DeviceCache"][device]["LMPVersion"]))

                    if "PageScanRepetitionMode" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tPage Scan Repetition Mode: {0}\r\n".format(self._data_file["DeviceCache"][device]["PageScanRepetitionMode"]))

                    if "LastInquiryUpdate" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tLast Inquiry Update: {0}\r\n".format(self._data_file["DeviceCache"][device]["LastInquiryUpdate"]))

                    if "Manufacturer" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tManufacturer: {0}\r\n".format(self._data_file["DeviceCache"][device]["Manufacturer"]))

                    if "ClockOffset" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tClock Offset: {0}\r\n".format(self._data_file["DeviceCache"][device]["ClockOffset"]))

                    if "PageScanMode" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tPage Scan Mode: {0}\r\n".format(self._data_file["DeviceCache"][device]["PageScanMode"]))

                    if "ClassOfDevice" in self._data_file["DeviceCache"][device]:
                        self._output_file.write("\t\tClass Of Device: {0}\r\n".format(self._data_file["DeviceCache"][device]["ClassOfDevice"]))
                self._output_file.write("\r\n")

            if "D2D MAC Address" in self._data_file:
                self._output_file.write("D2D MAC Address: {0}\r\n".format(binascii.hexlify(self._data_file["D2D MAC Address"])))

            # PersistentPortsServices  NOTHING OF INTEREST?????

            if "PairedDevices" in self._data_file:
                if len(self._data_file["PairedDevices"]) == 0:
                    self._output_file.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                else:
                    self._output_file.write("Paired Devices:\r\n")
                    for item in self._data_file["PairedDevices"]:
                        self._output_file.write("\tDevice: {0}\r\n".format(item))
        except KeyError:
            pass
        self._output_file.write("\r\n")

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
            if "PairedDevices" in self._data_file:
                if len(self._data_file["PairedDevices"]) == 0:
                    self._output_file.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                else:
                    self._output_file.write("Paired Devices:\r\n")
                    for paired_device in self._data_file["PairedDevices"]:
                        self._output_file.write("\tDevice: {0}\r\n".format(paired_device))

            if "DaemonControllersConfigurationKey" in self._data_file:
                if "DaemonControllersConfigurationKey" in self._data_file:
                    self._output_file.write("Daemon Controllers Configuration Key:\r\n")
                    for dmcck_key in self._data_file["DaemonControllersConfigurationKey"]:
                        self._output_file.write("\t{0}\r\n".format(dmcck_key))
                        for item in self._data_file["DaemonControllersConfigurationKey"][dmcck_key]:
                            self._output_file.write("\t\t{0}: {1}\r\n".format(item, self._data_file["DaemonControllersConfigurationKey"][dmcck_key][item]))
            if "ControllerPowerState" in self._data_file:
                self._output_file.write("Controller Power State: {0}\r\n".format(self._data_file["ControllerPowerState"]))
            if "HIDDevices" in self._data_file:
                self._output_file.write("HIDDevices\r\n")
                for hid_device in self._data_file["HIDDevices"]:
                    self._output_file.write("\tHID Device: {0}\r\n".format(hid_device))
            if "BluetoothVersionNumber" in self._data_file:
                self._output_file.write("Bluetooth Version Number: {0}\r\n".format(self._data_file["BluetoothVersionNumber"]))
            if "D2D MAC Address" in self._data_file:
                self._output_file.write("D2D MAC Address :{0}\r\n".format(self._data_file["D2D MAC Address"]))
            if "DeviceCache" in self._data_file:
                self._output_file.write("Device Cache\r\n")
                for cached_device in self._data_file["DeviceCache"]:
                    self._output_file.write("\tCached Device: {0}\r\n".format(cached_device))
                    for device_data in self._data_file["DeviceCache"][cached_device]:
                        if "VendorID" in device_data:
                            self._output_file.write("\t\tVendor ID: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["VendorID"]))
                        if "Name" in device_data:
                            self._output_file.write("\t\tName: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["Name"]))
                        if "LMPSubversion" in device_data:
                            self._output_file.write("\t\tLMP Subversion: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LMPSubversion"]))
                        if "LastNameUpdate" in device_data:
                            self._output_file.write("\t\tLast Name Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastNameUpdate"]))
                        if "ProductID" in device_data:
                            self._output_file.write("\t\tProduct ID: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["ProductID"]))
                        if "LMPVersion" in device_data:
                            self._output_file.write("\t\tLMP Version: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LMPVersion"]))
                        if "BatteryPercent" in device_data:
                            self._output_file.write("\t\tBattery Percent: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["BatteryPercent"]))
                        if "Manufacturer" in device_data:
                            self._output_file.write("\t\tManufacturer: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["Manufacturer"]))
                        if "ClassOfDevice" in device_data:
                            self._output_file.write("\t\tClass Of Device: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["ClassOfDevice"]))
                        if "LastServicesUpdate" in device_data:
                            self._output_file.write("\t\tLast Services Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastServicesUpdate"]))

        except KeyError:
            pass
        self._output_file.write("\r\n")

class Parse03():
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
            if "PairedDevices" in self._data_file:
                if len(self._data_file["PairedDevices"]) == 0:
                    self._output_file.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                else:
                    self._output_file.write("Paired Devices:\r\n")
                    for paired_device in self._data_file["PairedDevices"]:
                        self._output_file.write("\tDevice: {0}\r\n".format(paired_device))
            if "D2D MAC Address" in self._data_file:
                self._output_file.write("D2D MAC Address :{0}\r\n".format(self._data_file["D2D MAC Address"]))
            if "DaemonControllersConfigurationKey" in self._data_file:
                self._output_file.write("Daemon Controllers Configuration Key:\r\n")
                for dmcck_key in self._data_file["DaemonControllersConfigurationKey"]:
                    self._output_file.write("\t{0}\r\n".format(dmcck_key))
                    for item in self._data_file["DaemonControllersConfigurationKey"][dmcck_key]:
                        self._output_file.write("\t\t{0}: {1}\r\n".format(item, self._data_file["DaemonControllersConfigurationKey"][dmcck_key][item]))
            if "PANInterfaces" in self._data_file:
                self._output_file.write("PAN Interfaces:\r\n")
                for pan_interface in self._data_file["PANInterfaces"]:
                    self._output_file.write("\tPAN Interface: {0}\r\n".format(pan_interface))
            if "ControllerPowerState" in self._data_file:
                self._output_file.write("Controller Power State: {0}\r\n".format(self._data_file["ControllerPowerState"]))
            if "HIDDevices" in self._data_file:
                self._output_file.write("HIDDevices\r\n")
                for hid_device in self._data_file["HIDDevices"]:
                    self._output_file.write("\tHID Device: {0}\r\n".format(hid_device))
            if "DeviceCache" in self._data_file:
                self._output_file.write("Device Cache\r\n")
                for cached_device in self._data_file["DeviceCache"]:
                    self._output_file.write("\tCached Device: {0}\r\n".format(cached_device))
                    for device_data in self._data_file["DeviceCache"][cached_device]:
                        if "Name" in device_data:
                            self._output_file.write("\t\tName: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["Name"]))
                        if "Manufacturer" in device_data:
                            self._output_file.write("\t\tManufacturer: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["Manufacturer"]))
                        if "ClassOfDevice" in device_data:
                            self._output_file.write("\t\tClass Of Device: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["ClassOfDevice"]))
                        if "BatteryPercent" in device_data:
                            self._output_file.write("\t\tBattery Percent: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["BatteryPercent"]))
                        if "ClockOffset" in device_data:
                            self._output_file.write("\t\tClock Offset: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["ClockOffset"]))
                        if "LastNameUpdate" in device_data:
                            self._output_file.write("\t\tLast Name Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastNameUpdate"]))
                        if "LastServicesUpdate" in device_data:
                            self._output_file.write("\t\tLast Services Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastServicesUpdate"]))
                        if "LastInquiryUpdate" in device_data:
                            self._output_file.write("\t\tLast Inquiry Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                        if "LMPVersion" in device_data:
                            self._output_file.write("\t\tLMP Version: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LMPVersion"]))
                        if "LMPSubversion" in device_data:
                            self._output_file.write("\t\tLMP Subversion: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LMPSubversion"]))
                        if "InquiryRSSI" in device_data:
                            self._output_file.write("\t\tInquiry RSSI: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["InquiryRSSI"]))
                        if "PageScanMode" in device_data:
                            self._output_file.write("\t\tPage Scan Mode: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["PageScanMode"]))
                        if "PageScanPeriod" in device_data:
                            self._output_file.write("\t\tPage Scan Period: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["PageScanPeriod"]))
                        if "PageScanRepetitionMode" in device_data:
                            self._output_file.write("\t\tPage Scan Repetition Mode: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                        # EIRData NOT PARSED
                        # Services NOT PARSED
            # PersistentPorts NOT PARSED
        except KeyError:
            pass
        self._output_file.write("\r\n")

class Parse04():
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
            if "DaemonControllersConfigurationKey" in self._data_file:
                self._output_file.write("Daemon Controllers Configuration Key:\r\n")
                for dmcck_key in self._data_file["DaemonControllersConfigurationKey"]:
                    self._output_file.write("\t{0}\r\n".format(dmcck_key))
                    for item in self._data_file["DaemonControllersConfigurationKey"][dmcck_key]:
                        self._output_file.write("\t\t{0}: {1}\r\n".format(item, self._data_file["DaemonControllersConfigurationKey"][dmcck_key][item]))
            if "PANInterfaces" in self._data_file:
                self._output_file.write("PAN Interfaces:\r\n")
                for pan_interface in self._data_file["PANInterfaces"]:
                    self._output_file.write("\tPAN Interface: {0}\r\n".format(pan_interface))
            if "ControllerPowerState" in self._data_file:
                self._output_file.write("Controller Power State: {0}\r\n".format(self._data_file["ControllerPowerState"]))
            if "HIDDevices" in self._data_file:
                self._output_file.write("HIDDevices\r\n")
                for hid_device in self._data_file["HIDDevices"]:
                    self._output_file.write("\tHID Device: {0}\r\n".format(hid_device))
            if "DeviceCache" in self._data_file:
                self._output_file.write("Device Cache\r\n")
                for cached_device in self._data_file["DeviceCache"]:
                    self._output_file.write("\tCached Device: {0}\r\n".format(cached_device))
                    for device_data in self._data_file["DeviceCache"][cached_device]:
                        if "Name" in device_data:
                            self._output_file.write("\t\tName: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["Name"]))
                        if "Manufacturer" in device_data:
                            self._output_file.write("\t\tManufacturer: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["Manufacturer"]))
                        if "ClassOfDevice" in device_data:
                            self._output_file.write("\t\tClass Of Device: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["ClassOfDevice"]))
                        if "BatteryPercent" in device_data:
                            self._output_file.write("\t\tBattery Percent: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["BatteryPercent"]))
                        if "ClockOffset" in device_data:
                            self._output_file.write("\t\tClock Offset: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["ClockOffset"]))
                        if "LastNameUpdate" in device_data:
                            self._output_file.write("\t\tLast Name Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastNameUpdate"]))
                        if "LastServicesUpdate" in device_data:
                            self._output_file.write("\t\tLast Services Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastServicesUpdate"]))
                        if "LastInquiryUpdate" in device_data:
                            self._output_file.write("\t\tLast Inquiry Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                        if "LMPVersion" in device_data:
                            self._output_file.write("\t\tLMP Version: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LMPVersion"]))
                        if "LMPSubversion" in device_data:
                            self._output_file.write("\t\tLMP Subversion: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LMPSubversion"]))
                        if "InquiryRSSI" in device_data:
                            self._output_file.write("\t\tInquiry RSSI: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["InquiryRSSI"]))
                        if "PageScanMode" in device_data:
                            self._output_file.write("\t\tPage Scan Mode: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["PageScanMode"]))
                        if "PageScanPeriod" in device_data:
                            self._output_file.write("\t\tPage Scan Period: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["PageScanPeriod"]))
                        if "PageScanRepetitionMode" in device_data:
                            self._output_file.write("\t\tPage Scan Repetition Mode: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                        # EIRData NOT PARSED
                        # Services NOT PARSED
            # PersistentPorts NOT PARSED
            # PairedDevices ARRAY
            if "PairedDevices" in self._data_file:
                if len(self._data_file["PairedDevices"]) == 0:
                    self._output_file.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                else:
                    self._output_file.write("Paired Devices:\r\n")
                    for paired_device in self._data_file["PairedDevices"]:
                        self._output_file.write("\tDevice: {0}\r\n".format(paired_device))
        except KeyError:
            pass
        self._output_file.write("\r\n")

class Parse05():
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
            if "BluetoothAutoSeekHIDDevices" in self._data_file:
                self._output_file.write("Bluetooth Auto Seek HID Devices: {0}\r\n".format(self._data_file["BluetoothAutoSeekHIDDevices"]))
            if "ControllerPowerState" in self._data_file:
                self._output_file.write("Controller Power State         : {0}\r\n".format(self._data_file["ControllerPowerState"]))
            if "BluetoothVersionNumber" in self._data_file:
                self._output_file.write("Bluetooth Version Number       : {0}\r\n".format(self._data_file["BluetoothVersionNumber"]))
            if "DaemonControllersConfigurationKey" in self._data_file:
                self._output_file.write("Daemon Controllers Configuration Key:\r\n")
                for dmcck_key in self._data_file["DaemonControllersConfigurationKey"]:
                    self._output_file.write("\t{0}\r\n".format(dmcck_key))
                    for item in self._data_file["DaemonControllersConfigurationKey"][dmcck_key]:
                        self._output_file.write("\t\t{0}: {1}\r\n".format(item, self._data_file["DaemonControllersConfigurationKey"][dmcck_key][item]))
            if "HIDDevices" in self._data_file:
                hid_array = self._data_file["PairedDevices"]
                self._output_file.write("HID Devices: {0}\r\n")
                for hid_device in hid_array:
                    self._output_file.write("\t{0}\r\n".format(hid_device))
            if "DeviceCache" in self._data_file:
                self._output_file.write("Device Cache\r\n")
                for cached_device in self._data_file["DeviceCache"]:
                    self._output_file.write("\tCached Device: {0}\r\n".format(cached_device))
                    for device_data in self._data_file["DeviceCache"][cached_device]:
                        if "Name" in device_data:
                            self._output_file.write("\t\tName: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["Name"]))
                        if "Manufacturer" in device_data:
                            self._output_file.write("\t\tManufacturer: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["Manufacturer"]))
                        if "ClassOfDevice" in device_data:
                            self._output_file.write("\t\tClass Of Device: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["ClassOfDevice"]))
                        if "BatteryPercent" in device_data:
                            self._output_file.write("\t\tBattery Percent: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["BatteryPercent"]))
                        if "ClockOffset" in device_data:
                            self._output_file.write("\t\tClock Offset: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["ClockOffset"]))
                        if "LastNameUpdate" in device_data:
                            self._output_file.write("\t\tLast Name Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastNameUpdate"]))
                        if "LastServicesUpdate" in device_data:
                            self._output_file.write("\t\tLast Services Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastServicesUpdate"]))
                        if "LastInquiryUpdate" in device_data:
                            self._output_file.write("\t\tLast Inquiry Update: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                        if "LMPVersion" in device_data:
                            self._output_file.write("\t\tLMP Version: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LMPVersion"]))
                        if "LMPSubversion" in device_data:
                            self._output_file.write("\t\tLMP Subversion: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["LMPSubversion"]))
                        if "InquiryRSSI" in device_data:
                            self._output_file.write("\t\tInquiry RSSI: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["InquiryRSSI"]))
                        if "PageScanMode" in device_data:
                            self._output_file.write("\t\tPage Scan Mode: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["PageScanMode"]))
                        if "PageScanPeriod" in device_data:
                            self._output_file.write("\t\tPage Scan Period: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["PageScanPeriod"]))
                        if "PageScanRepetitionMode" in device_data:
                            self._output_file.write("\t\tPage Scan Repetition Mode: {0}\r\n".format(self._data_file["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
            if "PairedDevices" in self._data_file:
                paired_array = self._data_file["PairedDevices"]
                self._output_file.write("Paired Devices:\r\n")
                for paired_device in paired_array:
                    self._output_file.write("\t{0}\r\n".format(paired_device))
        except KeyError:
            pass
        self._output_file.write("\r\n")
