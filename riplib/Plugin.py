import pprint

__author__ = 'osxripper'
__version__ = '0.2'
__license__ = 'GPLv3'


class Plugin(object):
    """
    Base plugin class to inherit from and override as necessary
    """
    def __init__(self):
        """
        Initialise the class. N.B. in a full implementation of a class deriving
        from Plugin the self.* values should be changed.
        """
        self._name = "Plugin"
        self._description = "Base class for plugins"
        self._input_dir = None
        self._output_dir = None
        self._output_file = None
        self._data_file = None
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

    def set_os_version(self, osx_version):
        """
        Set the version of OSX to be run
        """
        self._os_version = osx_version

    def parse(self):
        """
        Public function called to parse the data file set in __init__, override as necessary
        """
        pass

    @staticmethod
    def pprint(data):
        """
        Pretty print format the data
        """
        return pprint.pformat(data, indent=4, width=80).replace("\n", "\r\n") + "\r\n"

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
