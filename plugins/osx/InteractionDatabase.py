""" Module to parse interactionC.db """
import codecs
import logging
import os
import sqlite3
import riplib.osxripper_time
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class InteractionDatabase(Plugin):
    """
    Parse information from /private/var/db/CoreDuet/People/interactionC.db
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("Interaction Database")
        self.set_description("Parse information from /private/var/db/CoreDuet/People/interactionC.db")
        self.set_data_file("interactionC.db")
        self.set_output_file("Interaction_Database.txt")
        self.set_type("sqlite")

    def parse(self):
        """
        Read the /private/var/db/CoreDuet/People/interactionC.db SQLite database
        """
        query = "SELECT zpk.z_name,zc.zdisplayname,zc.zidentifier," \
                "zc.zcreationdate," \
                "zc.zfirstincomingrecipientdate," \
                "zc.zfirstincomingsenderdate," \
                "zc.zfirstoutgoingrecipientdate," \
                "zc.zlastincomingrecipientdate," \
                "zc.zlastincomingsenderdate," \
                "zc.zlastoutgoingrecipientdate" \
                " FROM z_primarykey zpk,zcontacts zc WHERE zpk.z_ent = zc.z_ent"

        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            database_file = os.path.join(self._input_dir, "private", "var", "db", "CoreDuet", "People", self._data_file)
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
            if self._os_version in ["catalina", "mojave", "high_sierra", "sierra", "el_capitan"]:
                if not os.path.isfile(database_file):
                    logging.warning("File: %s does not exist or cannot be found.\r\n", self._data_file)
                    output_file.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(self._data_file))
                else:
                    output_file.write("Source Database: {0}\r\n\r\n".format(database_file))
                    conn = None
                    try:
                        conn = sqlite3.connect(database_file)
                        conn.row_factory = sqlite3.Row
                        with conn:
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            if len(rows) == 0:
                                output_file.write("No data in database.\r\n")
                            else:
                                for row in rows:
                                    creationdate = riplib.osxripper_time.get_cocoa_seconds(row["zcreationdate"])
                                    firstinrecipdate = riplib.osxripper_time.get_cocoa_seconds(row["zfirstincomingrecipientdate"])
                                    firstinsenderdate = riplib.osxripper_time.get_cocoa_seconds(row["zfirstincomingsenderdate"])
                                    firstoutrecipdate = riplib.osxripper_time.get_cocoa_seconds(row["zfirstoutgoingrecipientdate"])
                                    lastinrecipdate = riplib.osxripper_time.get_cocoa_seconds(row["zlastincomingrecipientdate"])
                                    lastinsenderdate = riplib.osxripper_time.get_cocoa_seconds(row["zlastincomingsenderdate"])
                                    lastoutrecipdate = riplib.osxripper_time.get_cocoa_seconds(row["zlastincomingsenderdate"])

                                    output_file.write("Name                         : {0}\r\n".format(row["z_name"]))
                                    output_file.write("Display Name                 : {0}\r\n".format(row["zdisplayname"]))
                                    output_file.write("Identifier                   : {0}\r\n".format(row["zidentifier"]))
                                    output_file.write("Creation Date                : {0}\r\n".format(creationdate))
                                    output_file.write("First Incoming Recipient Date: {0}\r\n".format(firstinrecipdate))
                                    output_file.write("First Incoming Sender Date   : {0}\r\n".format(firstinsenderdate))
                                    output_file.write("First Outgoing Recipient Date: {0}\r\n".format(firstoutrecipdate))
                                    output_file.write("Last Incoming Recipient Date : {0}\r\n".format(lastinrecipdate))
                                    output_file.write("Last Incoming Sender Date    : {0}\r\n".format(lastinsenderdate))
                                    output_file.write("Last Outgoing Recipient Date : {0}\r\n".format(lastoutrecipdate))
                                    output_file.write("\r\n")
                        output_file.write("\r\n")
                    except sqlite3.Error as error:
                        logging.error("%s", error.args[0])
                        print("[ERROR] {0}".format(error.args[0]))
                    finally:
                        if conn:
                            conn.close()
                    output_file.write("="*50 + "\r\n")

            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                output_file.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
        output_file.close()
