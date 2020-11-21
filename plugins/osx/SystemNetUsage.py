""" Module to get information from /private/var/networkd/netusage.sqlite """
import codecs
import logging
import os
import sqlite3
import riplib.osxripper_time
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemNetUsage(Plugin):
    """
    Parse information from /private/var/networkd/netusage.sqlite
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("System Net Usage")
        self.set_description("Parse information from /private/var/networkd/netusage.sqlite")
        self.set_data_file("netusage.sqlite")
        self.set_output_file("System_NetUsage.txt")
        self.set_type("sqlite")

    def parse(self):
        """
        Read the /private/var/networkd/netusage.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "private", "var", "networkd", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
            # if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                if os.path.isfile(file):
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        conn.row_factory = sqlite3.Row
                        output_file.write("="*10 + " Network Attachments " + "="*10 + "\r\n")
                        run_network_attachment_query(conn, output_file)
                        output_file.write("="*10 + " Networked Processes " + "="*10 + "\r\n")
                        run_process_query(conn, output_file)
                        output_file.write("="*10 + " Network Process Usage " + "="*10 + "\r\n")
                        run_live_usage_query(conn, output_file)
                        output_file.write("\r\n")
                    except sqlite3.Error as error:
                        logging.error("%s", error.args[0])
                        print("[ERROR] {0}".format(error.args[0]))
                    finally:
                        if conn:
                            conn.close()
                else:
                    logging.warning("File: %s does not exist or cannot be found.\r\n", file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("="*40 + "\r\n\r\n")
        output_file.close()


def run_process_query(sqlite_connection, output_file):
    """
    Query Process & time details
    """
    query = "SELECT zpk.z_name,zp.zprocname,zp.zfirsttimestamp,zp.ztimestamp FROM zprocess zp,z_primarykey zpk " \
            "WHERE zp.z_ent = zpk.z_ent ORDER BY zpk.z_name"
    with sqlite_connection:
        cur = sqlite_connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            first_timestamp = riplib.osxripper_time.get_cocoa_seconds(row["zfirsttimestamp"])
            timestamp = riplib.osxripper_time.get_cocoa_seconds(row["ztimestamp"])
            output_file.write("Name           : {0}\r\n".format(row["z_name"]))
            output_file.write("Process        : {0}\r\n".format(row["zprocname"]))
            output_file.write("First Timestamp: {0}\r\n".format(first_timestamp))
            output_file.write("Timestamp      : {0}\r\n".format(timestamp))
            output_file.write("\r\n")


def run_live_usage_query(sqlite_connection, output_file):
    """
    Query Process & time details for WiFi usage
    """
    query = "SELECT zpk.z_name,zp.zprocname,zlu.ztimestamp,zlu.zwifiin," \
            "zlu.zwifiout,zlu.zwiredin,zlu.zwiredout,zlu.zwwanin,zlu.zwwanout FROM zprocess zp,zliveusage zlu," \
            "z_primarykey zpk WHERE zp.z_ent = zpk.z_ent AND zp.z_pk = zlu.zhasprocess ORDER BY zpk.z_name"
    with sqlite_connection:
        cur = sqlite_connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            ztimestamp = riplib.osxripper_time.get_cocoa_seconds(row["ztimestamp"])
            output_file.write("Name     : {0}\r\n".format(row["z_name"]))
            output_file.write("Process  : {0}\r\n".format(row["zprocname"]))
            output_file.write("Timestamp: {0}\r\n".format(ztimestamp))
            output_file.write("WiFi In  : {0}\r\n".format(row["zwifiin"]))
            output_file.write("WiFi Out : {0}\r\n".format(row["zwifiout"]))
            output_file.write("Wired In : {0}\r\n".format(row["zwiredin"]))
            output_file.write("Wired Out: {0}\r\n".format(row["zwiredout"]))
            output_file.write("WAN In   : {0}\r\n".format(row["zwwanin"]))
            output_file.write("WAN Out  : {0}\r\n".format(row["zwwanout"]))
            output_file.write("\r\n")


def run_network_attachment_query(sqlite_connection, output_file):
    """
    Query to Network and MAC address data
    """
    query = "SELECT zpk.z_name,zna.zidentifier,zna.zfirsttimestamp,zna.ztimestamp " \
            "FROM znetworkattachment zna,z_primarykey zpk " \
            "WHERE zna.z_ent = zpk.z_ent ORDER BY zpk.z_name"
    with sqlite_connection:
        cur = sqlite_connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            zfirsttimestamp = riplib.osxripper_time.get_cocoa_seconds(row["zfirsttimestamp"])
            ztimestamp = riplib.osxripper_time.get_cocoa_seconds(row["ztimestamp"])
            output_file.write("Name           : {0}\r\n".format(row[0]))
            if row["zidentifier"] is None:
                output_file.write("Network        : None\r\n")
                output_file.write("MAC Address    : None\r\n")
            else:
                ident = row["zidentifier"]
                dash_index = ident.rfind("-")
                network_name = ident[0:dash_index]
                network_mac = ident[dash_index+1:len(ident)]
                output_file.write("Network        : {0}\r\n".format(network_name))
                output_file.write("MAC Address    : {0}\r\n".format(network_mac))
            output_file.write("First Timestamp: {0}\r\n".format(zfirsttimestamp))
            output_file.write("Timestamp      : {0}\r\n".format(ztimestamp))
            output_file.write("\r\n")
