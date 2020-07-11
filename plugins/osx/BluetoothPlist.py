from riplib.Plugin import Plugin
import binascii
import codecs
import logging
import os
import riplib.ccl_bplist

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
        self._name = "Bluetooth Settings"
        self._description = "Parse bluetooth connection data."
        self._output_file = "Networking.txt"
        self._data_file = "com.apple.Bluetooth.plist"
        self._type = "bplist"
        
    def parse(self): 
        """
        /Library/Preferences/com.apple.Bluetooth.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "BluetoothVersionNumber" in plist:
                            of.write("Bluetooth Version Number: {0}\r\n".format(plist["BluetoothVersionNumber"]))

                        if "IgnoredDevices" in plist:
                            if len(plist["IgnoredDevices"]) == 0:
                                of.write("Ignored Devices:\r\n\tNo ignored devices listed.\r\n")
                            else:
                                of.write("Ignored Devices:\r\n")
                                for item in plist["IgnoredDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(item))
                        
                        if "BRPairedDevices" in plist:
                            if len(plist["BRPairedDevices"]) == 0:
                                of.write("BR Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("BR Paired Devices:\r\n")
                                for item in plist["BRPairedDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(item))
                        
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State: {0}\r\n".format(plist["BluetoothVersionNumber"]))
                        
                        if "HIDDevices" in plist:
                            if len(plist["HIDDevices"]) == 0:
                                of.write("HID Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("HID Devices:\r\n")
                                for item in plist["HIDDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(item))
                        
                        # PersistentPorts NOTHING OF INTEREST?????
                        
                        if "DeviceCache" in plist:
                            for device in plist["DeviceCache"]:
                                of.write("Device Cache\r\n")
                                of.write("\tDevice: {0}\r\n".format(device))

                                if "VendorID" in plist["DeviceCache"][device]:
                                    of.write("\t\tVendor ID: {0}\r\n".format(plist["DeviceCache"][device]["VendorID"]))
                                
                                if "Name" in plist["DeviceCache"][device]:
                                    of.write("\t\tName: {0}\r\n".format(plist["DeviceCache"][device]["Name"]))
                                
                                if "LMPSubversion" in plist["DeviceCache"][device]:
                                    of.write("\t\tLMP Subversion: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["LMPSubversion"]))
                                
                                if "PageScanPeriod" in plist["DeviceCache"][device]:
                                    of.write("\t\tPage Scan Period: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["PageScanPeriod"]))
                                
                                if "LastNameUpdate" in plist["DeviceCache"][device]:
                                    of.write("\t\tLast Name Update: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["LastNameUpdate"]))
                                
                                if "SupportedFeatures" in plist["DeviceCache"][device]:
                                    of.write("\t\tSupported Features: {0}\r\n"
                                             .format(binascii
                                                     .hexlify(plist["DeviceCache"][device]["SupportedFeatures"])))
                                
                                if "ProductID" in plist["DeviceCache"][device]:
                                    of.write("\t\tProduct ID: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["ProductID"]))
                                
                                if "LMPVersion" in plist["DeviceCache"][device]:
                                    of.write("\t\tLMP Version: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["LMPVersion"]))
                                
                                if "PageScanRepetitionMode" in plist["DeviceCache"][device]:
                                    of.write("\t\tPage Scan Repetition Mode: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["PageScanRepetitionMode"]))
                                
                                if "LastInquiryUpdate" in plist["DeviceCache"][device]:
                                    of.write("\t\tLast Inquiry Update: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["LastInquiryUpdate"]))
                                    
                                if "Manufacturer" in plist["DeviceCache"][device]:
                                    of.write("\t\tManufacturer: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["Manufacturer"]))
                                
                                if "ClockOffset" in plist["DeviceCache"][device]:
                                    of.write("\t\tClock Offset: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["ClockOffset"]))
                                
                                if "PageScanMode" in plist["DeviceCache"][device]:
                                    of.write("\t\tPage Scan Mode: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["PageScanMode"]))
                                
                                if "ClassOfDevice" in plist["DeviceCache"][device]:
                                    of.write("\t\tClass Of Device: {0}\r\n"
                                             .format(plist["DeviceCache"][device]["ClassOfDevice"]))
                            of.write("\r\n")
                            
                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address: {0}\r\n".format(binascii.hexlify(plist["D2D MAC Address"])))
                        
                        # PersistentPortsServices  NOTHING OF INTEREST?????
                        
                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for item in plist["PairedDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(item))
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
                
            elif self._os_version == "mavericks":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for paired_device in plist["PairedDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(paired_device))
                                    
                        if "DaemonControllersConfigurationKey" in plist:
                            if "DaemonControllersConfigurationKey" in plist:
                                of.write("Daemon Controllers Configuration Key:\r\n")
                                for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                    of.write("\t{0}\r\n".format(dmcck_key))
                                    for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                        of.write("\t\t{0}: {1}\r\n"
                                                 .format(item,
                                                         plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State: {0}\r\n".format(plist["ControllerPowerState"]))
                        if "HIDDevices" in plist:
                            of.write("HIDDevices\r\n")
                            for hid_device in plist["HIDDevices"]:
                                of.write("\tHID Device: {0}\r\n".format(hid_device))
                        if "BluetoothVersionNumber" in plist:
                            of.write("Bluetooth Version Number: {0}\r\n".format(plist["BluetoothVersionNumber"]))
                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address :{0}\r\n".format(plist["D2D MAC Address"]))
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                of.write("\tCached Device: {0}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    if "VendorID" in device_data:
                                        of.write("\t\tVendor ID: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["VendorID"]))
                                    if "Name" in device_data:
                                        of.write("\t\tName: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Name"]))
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    if "ProductID" in device_data:
                                        of.write("\t\tProduct ID: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ProductID"]))
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    if "Manufacturer" in device_data:
                                        of.write("\t\tManufacturer: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Manufacturer"]))
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))

                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
                    
            elif self._os_version == "mountain_lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for paired_device in plist["PairedDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(paired_device))
                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address :{0}\r\n".format(plist["D2D MAC Address"]))
                        if "DaemonControllersConfigurationKey" in plist:
                            of.write("Daemon Controllers Configuration Key:\r\n")
                            for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                of.write("\t{0}\r\n".format(dmcck_key))
                                for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                    of.write("\t\t{0}: {1}\r\n"
                                             .format(item, plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        if "PANInterfaces" in plist:
                            of.write("PAN Interfaces:\r\n")
                            for pan_interface in plist["PANInterfaces"]:
                                of.write("\tPAN Interface: {0}\r\n".format(pan_interface))
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State: {0}\r\n".format(plist["ControllerPowerState"]))
                        if "HIDDevices" in plist:
                            of.write("HIDDevices\r\n")
                            for hid_device in plist["HIDDevices"]:
                                of.write("\tHID Device: {0}\r\n".format(hid_device))
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                of.write("\tCached Device: {0}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    if "Name" in device_data:
                                        of.write("\t\tName: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Name"]))
                                    if "Manufacturer" in device_data:
                                        of.write("\t\tManufacturer: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Manufacturer"]))
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    if "ClockOffset" in device_data:
                                        of.write("\t\tClock Offset: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClockOffset"]))
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))
                                    if "LastInquiryUpdate" in device_data:
                                        of.write("\t\tLast Inquiry Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    if "InquiryRSSI" in device_data:
                                        of.write("\t\tInquiry RSSI: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["InquiryRSSI"]))
                                    if "PageScanMode" in device_data:
                                        of.write("\t\tPage Scan Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanMode"]))
                                    if "PageScanPeriod" in device_data:
                                        of.write("\t\tPage Scan Period: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanPeriod"]))
                                    if "PageScanRepetitionMode" in device_data:
                                        of.write("\t\tPage Scan Repetition Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                                    # EIRData NOT PARSED
                                    # Services NOT PARSED
                        # PersistentPorts NOT PARSED
                                
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "DaemonControllersConfigurationKey" in plist:
                            of.write("Daemon Controllers Configuration Key:\r\n")
                            for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                of.write("\t{0}\r\n".format(dmcck_key))
                                for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                    of.write("\t\t{0}: {1}\r\n"
                                             .format(item, plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        if "PANInterfaces" in plist:
                            of.write("PAN Interfaces:\r\n")
                            for pan_interface in plist["PANInterfaces"]:
                                of.write("\tPAN Interface: {0}\r\n".format(pan_interface))
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State: {0}\r\n".format(plist["ControllerPowerState"]))
                        if "HIDDevices" in plist:
                            of.write("HIDDevices\r\n")
                            for hid_device in plist["HIDDevices"]:
                                of.write("\tHID Device: {0}\r\n".format(hid_device))
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                of.write("\tCached Device: {0}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    if "Name" in device_data:
                                        of.write("\t\tName: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Name"]))
                                    if "Manufacturer" in device_data:
                                        of.write("\t\tManufacturer: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Manufacturer"]))
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    if "ClockOffset" in device_data:
                                        of.write("\t\tClock Offset: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClockOffset"]))
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))
                                    if "LastInquiryUpdate" in device_data:
                                        of.write("\t\tLast Inquiry Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    if "InquiryRSSI" in device_data:
                                        of.write("\t\tInquiry RSSI: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["InquiryRSSI"]))
                                    if "PageScanMode" in device_data:
                                        of.write("\t\tPage Scan Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanMode"]))
                                    if "PageScanPeriod" in device_data:
                                        of.write("\t\tPage Scan Period: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanPeriod"]))
                                    if "PageScanRepetitionMode" in device_data:
                                        of.write("\t\tPage Scan Repetition Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                                    # EIRData NOT PARSED
                                    # Services NOT PARSED
                        # PersistentPorts NOT PARSED
                        # PairedDevices ARRAY
                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for paired_device in plist["PairedDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(paired_device))
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "BluetoothAutoSeekHIDDevices" in plist:
                            of.write("Bluetooth Auto Seek HID Devices: {0}\r\n"
                                     .format(plist["BluetoothAutoSeekHIDDevices"]))
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State         : {0}\r\n".format(plist["ControllerPowerState"]))
                        if "BluetoothVersionNumber" in plist:
                            of.write("Bluetooth Version Number       : {0}\r\n".format(plist["BluetoothVersionNumber"]))
                        if "DaemonControllersConfigurationKey" in plist:
                            of.write("Daemon Controllers Configuration Key:\r\n")
                            for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                of.write("\t{0}\r\n".format(dmcck_key))
                                for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                    of.write("\t\t{0}: {1}\r\n"
                                             .format(item, plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        if "HIDDevices" in plist:
                            hid_array = plist["PairedDevices"]
                            of.write("HID Devices: {0}\r\n")
                            for hid_device in hid_array:
                                of.write("\t{0}\r\n".format(hid_device))
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                of.write("\tCached Device: {0}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    if "Name" in device_data:
                                        of.write("\t\tName: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Name"]))
                                    if "Manufacturer" in device_data:
                                        of.write("\t\tManufacturer: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Manufacturer"]))
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    if "ClockOffset" in device_data:
                                        of.write("\t\tClock Offset: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClockOffset"]))
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))
                                    if "LastInquiryUpdate" in device_data:
                                        of.write("\t\tLast Inquiry Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    if "InquiryRSSI" in device_data:
                                        of.write("\t\tInquiry RSSI: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["InquiryRSSI"]))
                                    if "PageScanMode" in device_data:
                                        of.write("\t\tPage Scan Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanMode"]))
                                    if "PageScanPeriod" in device_data:
                                        of.write("\t\tPage Scan Period: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanPeriod"]))
                                    if "PageScanRepetitionMode" in device_data:
                                        of.write("\t\tPage Scan Repetition Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                        if "PairedDevices" in plist:
                            paired_array = plist["PairedDevices"]
                            of.write("Paired Devices:\r\n")
                            for paired_device in paired_array:
                                of.write("\t{0}\r\n".format(paired_device))
                    except KeyError:
                        pass
                    of.write("\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
