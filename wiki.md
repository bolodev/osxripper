## Writing Plugins

To write a plugin

* Do not worry about setting the OSX version, this is done by the __osxripper__ itself.
* Create and name a file in the __osx__ plugin directory under __plugins/osx__.
* In the plugin file add:
```python
from riplib.Plugin import plugin
```
* Declare the class - the naming convention in this case is to name the class the same as the python file
* Ensure "Plugin" is defined as the super class in the class declaration:
```python
class Foo(Plugin):
```
* Override the ```__init__``` function, the following needs to be defined for a new plugin:

```python
def __init__(self):
    """
    Initialise the class.
    """
    self._name = "My Plugin" # COMPULSORY
    self._description = "Get information from /path/file" # COMPULSORY
    self._data_file = "fileToParse.extension" # OPTIONAL
    self._output_file = "Writeme.txt" # COMPULSORY
    self._type = "plist" # COMPULSORY
```

For __self._type__ the one of the following values should be used:

1. text - for plain text files
2. plist - for plain XML plist files
3. bplist - for binary plist files
4. sqlite - for SQLite database files
5. dir_list - for straightforward directory listing
6. mixed/multiple - for a plugin that mixes data sources 

Other formats can be defined (i.e. binarycookie, asl log, etc.), but use the above types for those types of files


### EXAMPLE PLUGIN 
***
Assume being declared in a file called __"Example.py"__

N.B. The following variables are set by the osxripper script, they do not need to be set in the plugin script

* self._input_dir
* self._output_dir
* self._os_version


```python
    from riplib.Plugin import plugin
    import codecs
    import logging

    class Example(Plugin):

	def __init__(self):
		"""
		Initialise the class.
		"""
		self._name = "Example Plugin"
		self._description = "Get information from /path/file"
		self._data_file = "Example.file"
		self._output_file = "Example.txt"
		self._type = "text"
		
	def parse(self): 
		#Add your code here, it will get called by the osxripper.py script
		#Update the if-else statement as required
		with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
			of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
			of.write("Source File: {}\r\n\r\n".format(self._data_file))
			if self._os_version == "el_capitan":
				print("Doing something here")			
			elif self._os_version == "yosemite":
				print("Doing something here")
			elif self._os_version == "mavericks":
				print("Doing something here")
			elif self._os_version == "mountain_lion":
				print("Doing something here")
			elif self._os_version == "lion":
				print("Doing something here")
			elif self._os_version == "snow_leopard":
				print("Doing something here")
			else:
				logging.warning("Not a known OSX version.")
				print("[WARNING] Not a known OSX version.")
			of.write("="*40 + "\r\n\r\n")
		of.close()
```