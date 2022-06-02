""" Module for base Plugin classes """
# import pprint

__author__ = 'osxripper'
__version__ = '0.2'
__license__ = 'GPLv3'


class PluginDescription():
    """
    Class to hold basic description data
    """
    def __init__(self):
        """
        Initialise the class
        """
        self._name = "Plugin"
        self._description = "Base class for plugins"
        self._type = "text"  # use [text|plist|bplist|sqlite|dir_list|mixed]
        self._os_version = "yosemite"

    def __call__(self):
        return self

    @property
    def get_name(self):
        """
        Return the name of the plugin
        """
        return self._name

    @property
    def get_description(self):
        """
        Return the description of the plugin
        """
        return self._description

    @property
    def get_type(self):
        """
        Return the plugin type
        """
        return self._type

    @property
    def get_os_version(self):
        """
        Return the version of the OS
        """
        return self._os_version

    def set_name(self, plugin_name):
        """
        Set the plugin name
        """
        self._name = plugin_name

    def set_description(self, plugin_description):
        """
        Set the plugin description
        """
        self._description = plugin_description

    def set_type(self, plugin_type):
        """
        Set the plugin type
        """
        self._type = plugin_type

    def set_os_version(self, osx_version):
        """
        Set the version of OSX to be run
        """
        self._os_version = osx_version


class Plugin(PluginDescription):
    """
    Base plugin class to inherit from and override as necessary
    """
    def __init__(self):
        """
        Initialise the class. N.B. in a full implementation of a class deriving
        from Plugin the self.* values should be changed.
        """
        super().__init__()
        self._input_dir = None
        self._output_dir = None
        self._output_file = None
        self._data_file = None

    # def __call__(self):
    #     return self

    @property
    def get_input_dir(self):
        """
        Return plugin input directory
        """
        return self._input_dir

    @property
    def get_output_dir(self):
        """
        Return plugin output directory
        """
        return self._output_dir

    @property
    def get_output_file(self):
        """
        Return plugin output file
        """
        return self._output_file

    @property
    def get_data_file(self):
        """
        Return the file the plugin will parse
        """
        return self._data_file

    def set_input_directory(self, file):
        """
        Set the input directory for the plugin
        """
        self._input_dir = file

    def set_output_directory(self, file):
        """
        Set the output directory for the plugin
        """
        self._output_dir = file

    def set_output_file(self, output_file):
        """
        Set the output file for the plugin
        """
        self._output_file = output_file

    def set_data_file(self, data_file):
        """
        Set the data file to parse
        """
        self._data_file = data_file

    def parse(self):
        """
        Public function called to parse the data file set in __init__, override as necessary
        """


    # @staticmethod
    # def pprint(data):
    #     """
    #     Pretty print format the data
    #     """
    #     return pprint.pformat(data, indent=4, width=80).replace("\n", "\r\n") + "\r\n"

    def __str__(self):
        """
        Return a string representation of the plugin
        """
        return "Plugin(%s, %s, %s)" % (self._name, self._type, self._data_file)

    def __repr__(self):
        """
        Return a string representation of the plugin
        """
        return "Plugin(%s)" % str(self)
