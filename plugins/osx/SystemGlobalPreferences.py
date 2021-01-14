""" Module to derive time information from /Library/Preferences/.GlobalPreferences.plist """
import codecs
import logging
import os
import riplib.ccl_bplist
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemGlobalPreferences(Plugin):
    """
    Plugin to derive time information from /Library/Preferences/.GlobalPreferences.plist
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("System Settings")
        self.set_description("Parse /Library/Preferences/.GlobalPreferences.plist")
        self.set_data_file(".GlobalPreferences.plist")
        self.set_output_file("System.txt")
        self.set_type("bplist")

    def parse(self):
        """
        Parse /Library/Preferences/.GlobalPreferences.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            global_plist = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(global_plist))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan", "yosemite",
                                    "mavericks", "mountain_lion", "lion"]:
                if os.path.isfile(global_plist):
                    bplist = open(global_plist, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    parse_os = ParseVers110107(output_file, plist)
                    parse_os.parse()
                else:
                    logging.warning("File %s does not exist.", global_plist)
                    print("[WARNING] File {0} does not exist.".format(global_plist))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(global_plist):
                    bplist = open(global_plist, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    parse_os = ParseVers106(output_file, plist)
                    parse_os.parse()
            else:
                logging.warning("Not a known OSX version.")
                output_file.write("[WARNING] Not a known OSX version.\r\n")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()

class ParseVers110107():
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
        if "MultipleSessionEnabled" in self._data_file:
            self._output_file.write("Multiple Session Enabled       : {0}\r\n".format(self._data_file["MultipleSessionEnabled"]))
            if "com.apple.updatesettings_did_disable_ftp" in self._data_file:
                self._output_file.write("Update Settings Did Disable FTP: {0}\r\n".format(self._data_file["com.apple.updatesettings_did_disable_ftp"]))
            if "com.apple.AppleModemSettingTool.LastCountryCode" in self._data_file:
                self._output_file.write("Modem Last Country Code        : {0}\r\n".format(self._data_file["com.apple.AppleModemSettingTool.LastCountryCode"]))
            if "Country" in self._data_file:
                self._output_file.write("Country                        : {0}\r\n".format(self._data_file["Country"]))
            if "AppleLocale" in self._data_file:
                self._output_file.write("Apple Locale                   : {0}\r\n".format(self._data_file["AppleLocale"]))
            if "AppleLanguages" in self._data_file:
                apple_languages = self._data_file["AppleLanguages"]
                self._output_file.write("Languages:\r\n")
                for apple_language in apple_languages:
                    self._output_file.write("\tLanguage: {0}\r\n".format(apple_language))

class ParseVers106():
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
        if "com.apple.AppleModemSettingTool.LastCountryCode" in self._data_file:
            self._output_file.write("Last Country Code: {0}\r\n".format(self._data_file["com.apple.AppleModemSettingTool.LastCountryCode"]))
            if "com.apple.preferences.timezone.selected_city" in self._data_file:
                self._output_file.write("Selected City: {0}\r\n")
                selected_city = self._data_file["com.apple.preferences.timezone.selected_city"]
                if "RegionalCode" in selected_city:
                    self._output_file.write("\tRegional Code : {0}\r\n".format(selected_city["RegionalCode"]))
                if "Version" in selected_city:
                    self._output_file.write("\tVersion       : {0}\r\n".format(selected_city["Version"]))
                if "TimeZoneName" in selected_city:
                    self._output_file.write("\tTime Zone Name: {0}\r\n".format(selected_city["TimeZoneName"]))
                if "Latitude" in selected_city:
                    self._output_file.write("\tLatitude      : {0}\r\n".format(selected_city["Latitude"]))
                if "Longitude" in selected_city:
                    self._output_file.write("\tLongitude     : {0}\r\n".format(selected_city["Longitude"]))
                if "GeonameID" in selected_city:
                    self._output_file.write("\tGeoname ID    : {0}\r\n".format(selected_city["GeonameID"]))
                if "CountryCode" in selected_city:
                    self._output_file.write("\tCountry Code  : {0}\r\n".format(selected_city["CountryCode"]))
                if "Name" in selected_city:
                    self._output_file.write("\tName          : {0}\r\n".format(selected_city["Name"]))

            if "Country" in self._data_file:
                self._output_file.write("Country: {0}\r\n".format(self._data_file["Country"]))
            if "AppleLocale" in self._data_file:
                self._output_file.write("Apple Locale: {0}\r\n".format(self._data_file["AppleLocale"]))
            if "AppleLanguages" in self._data_file:
                self._output_file.write("Apple Languages:\r\n")
                for apple_language in self._data_file["AppleLanguages"]:
                    self._output_file.write("\t{0}\r\n".format(apple_language))
            if "com.apple.TimeZonePref.Last_Selected_City" in self._data_file:
                self._output_file.write("Last Selected City:\r\n")
                for item in self._data_file["com.apple.TimeZonePref.Last_Selected_City"]:
                    self._output_file.write("\t{0}\r\n".format(item))
