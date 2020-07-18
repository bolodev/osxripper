""" osxripper driver script """
import argparse
import importlib
import logging
import os
import sys
from datetime import datetime
from plugins.osx_version import OSXVersion
from plugins.summary import Summary

__author__ = 'osxripper'
__version__ = '0.3'
__license__ = 'GPLv3'

active_plugin_list = []

# LOG_FILE = ""


def __set_sys_path():
    """
    Add the lib directory to the osx_plugin_sourceule search path to pick up library
    osx_plugin_sourceules.
    """
    current_dir = sys.path[0]  # assumes osxripper.py script directory
    library_dir = os.path.join(current_dir, "riplib")
    plugin_dir = os.path.join(current_dir, "plugins")
    sys.path.insert(1, library_dir)
    sys.path.insert(1, plugin_dir)


def __run_summary():
    """
    Run the Summary plugin
    """
    logging.info("Running Summary Plugin")
    osx_summary = Summary()
    osx_summary.set_os_version(__get_osx_version())
    osx_summary.set_input_directory(args.input)
    osx_summary.set_output_directory(args.output)
    osx_summary.parse()


def __get_osx_version():
    """
    Get the version of OSX
    """
    use_version = "big_sur"  # Default
    osx_version = OSXVersion()
    osx_version.set_input_directory(args.input)
    use_version = osx_version.parse()
    if "11.0" in use_version:
        use_version = "big_sur"
    if "10.16" in use_version:
        use_version = "big_sur"
    if "10.15" in use_version:
        use_version = "catalina"
    if "10.14" in use_version:
        use_version = "mojave"
    if "10.13" in use_version:
        use_version = "high_sierra"
    if "10.12" in use_version:
        use_version = "sierra"
    if "10.11" in use_version:
        use_version = "el_capitan"
    if "10.10" in use_version:
        use_version = "yosemite"
    if "10.9" in use_version:
        use_version = "mavericks"
    if "10.8" in use_version:
        use_version = "mountain_lion"
    if "10.7" in use_version:
        use_version = "lion"
    if "10.6" in use_version:
        use_version = "snow_leopard"
    print("[INFO] OSXVersion: {0}".format(use_version))
    logging.info("OSXVersion: %s", use_version)
    return use_version


def __load_from_file(osx_class_name):
    """
    Instantiate plugin class
    """
    osx_plugin_module = importlib.import_module('plugins.osx.' + osx_class_name)
    class_inst = getattr(osx_plugin_module, osx_class_name)()
    return class_inst


def __load_plugins():
    """
    Load the plugins for a the OSX version specified
    Adapted from http://stackoverflow.com/questions/301134/dynamic-mod-import-in-python
    """
    osx_plugins_path = os.path.join('.', 'plugins', "osx")
    osx_plugins_list = os.listdir(osx_plugins_path)
    osx_plugins_list.sort()
    for osx_plugin_source in osx_plugins_list:
        if osx_plugin_source.endswith(".py") and "__init__" not in osx_plugin_source:
            plugin_class = __load_from_file(os.path.splitext(osx_plugin_source)[0])
            if plugin_class is None:
                print("[ERROR] Unable to instantiate {0} from {1}"
                      .format(osx_plugin_source, osx_plugins_path))
                logging.error("[ERROR] Unable to instantiate %s from %s",
                              osx_plugin_source, osx_plugins_path)
            else:
                active_plugin = plugin_class()
                active_plugin_list.append(active_plugin)

    plugin_count = len(active_plugin_list)
    # if plugin_count == 0 or plugin_count > 1:
    print("[INFO] Loaded {0} plugins.".format(plugin_count))
    logging.info("Loaded %d plugins.", plugin_count)
    # else:
    #     print("[INFO] Loaded {0} plugins.".format(plugin_count))
    #     logging.info("Loaded {0} plugins.".format(plugin_count))


def __run_plugins():
    """
    Run the plugins from the active plugin list
    """
    osx_version = __get_osx_version()
    for active_plugin in active_plugin_list:
        print("[INFO] Running: {0}".format(active_plugin.get_name))
        logging.info("Running: %s", active_plugin.get_name)
        active_plugin.set_os_version(osx_version)
        active_plugin.set_input_directory(args.input)
        active_plugin.set_output_directory(args.output)
        active_plugin.parse()


def __list_plugins():
    """
    List the available plugins
    """
    __load_plugins()
    for active_plugin in active_plugin_list:
        print("{0} - {1}".format(active_plugin.get_name, active_plugin.get_description))


def main():
    """
    Main entry point
    """
    date_timestamp = datetime.now()
    # global LOG_FILE
    # LOG_FILE = os.path.join(args.output,
    #                         "_osxripper.{0}.txt".format(date_timestamp.strftime("%Y%m%d.%H%M%S")))
    log_file = os.path.join(args.output,
                            "_osxripper.{0}.txt".format(date_timestamp.strftime("%Y%m%d.%H%M%S")))
    logging.basicConfig(filename=log_file, level=logging.INFO)

    print("="*60)
    logging.info("="*60)
    print("[INFO] Starting osxripper...")
    logging.info("Starting osxripper...")
    print("[INFO] Start: {0}".format(date_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")))
    logging.info("Start: %s", date_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"))
    __set_sys_path()
    osx_version = __get_osx_version()
    if args.summary:
        print("[INFO] Loading summary for {0}.".format(osx_version))
        logging.info("Loading summary for %s.", osx_version)
        __run_summary()
    else:
        print("[INFO] Loading plugins for {0}.".format(osx_version))
        logging.info("Loading plugins for %s.", osx_version)
        __load_plugins()
        __run_plugins()
    print("[INFO] Output files written to {0}.".format(args.output))
    logging.info("Output files written to %s.", args.output)
    print("[INFO] Finish: {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))
    logging.info("Finish: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    print("[INFO] Finished.")
    logging.info("Finished.")
    print("="*60)
    logging.info("="*60)


def print_usage():
    """
    Print the command line usage
    """
    print("\nUSAGE:\n")
    print("python3 osxripper.py -i /root_directory_for_OSX_mount -o /some_directory_to_write_to\n")
    print("For help:")
    print("python3 osxripper.py -h or python3 osxripper.py --help")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input mountpoint or directory")
    parser.add_argument("-o", "--output", help="output or directory")
    parser.add_argument("-l", "--list", action="store_true", help="list the available plugins")
    parser.add_argument("-s", "--summary", action="store_true", help="only run the summary plugin")
    args = parser.parse_args()

    if args.list:
        __list_plugins()
        sys.exit(0)

    if not os.path.isdir(args.input):
        print("[ERROR] Input directory does not exist. \
         Ensure the input directory/mountpoint exists and is accessible.")
        sys.exit(1)
    if not os.path.isdir(args.output):
        print("[ERROR] Output directory does not exist. \
         Ensure the output directory/mountpoint exists and is accessible.")
        sys.exit(1)
    main()
