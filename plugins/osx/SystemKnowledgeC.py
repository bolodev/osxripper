""" Module to information from /private/var/db/CoreDuet/Knowledge/KnowledgeC.db reference """
import codecs
import logging
import os
import sqlite3
from riplib.plugin import Plugin


__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemKnowledgeC(Plugin):
    """
    Parse information from /private/var/db/CoreDuet/Knowledge/KnowledgeC.db reference
    https://www.mac4n6.com/blog/2018/8/5/knowledge-is-power-using-the-knowledgecdb-database-on-macos-and-ios-to-determine-precise-user-and-application-usage
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.set_name("System KnowledgeC")
        self.set_description("Parse information from /private/var/db/CoreDuet/Knowledge/KnowledgeC.db")
        self.set_data_file("KnowledgeC.db")
        self.set_output_file("System_KnowledgeC.txt")
        self.set_type("sqlite")

    def parse(self):
        """
        Read the /private/var/db/CoreDuet/Knowledge/KnowledgeC.db SQLite database
        """
        mac4n6_sql = "SELECT datetime(ZCREATIONDATE+978307200, 'UNIXEPOCH', 'LOCALTIME') as \"ENTRY CREATION\"," \
                     "CASE ZSTARTDAYOFWEEK" \
                     " WHEN \"1\" THEN \"Sunday\"" \
                     " WHEN \"2\" THEN \"Monday\"" \
                     " WHEN \"3\" THEN \"Tuesday\"" \
                     " WHEN \"4\" THEN \"Wednesday\"" \
                     " WHEN \"5\" THEN \"Thursday\"" \
                     " WHEN \"6\" THEN \"Friday\"" \
                     " WHEN \"7\" THEN \"Saturday\"" \
                     " END \"DAY OF WEEK\", " \
                     "ZSECONDSFROMGMT / 3600 AS \"GMT OFFSET\", " \
                     "datetime(ZSTARTDATE + 978307200, 'UNIXEPOCH', 'LOCALTIME') as \"START\", " \
                     "datetime(ZENDDATE + 978307200, 'UNIXEPOCH', 'LOCALTIME') as \"END\", " \
                     "(ZENDDATE - ZSTARTDATE) as \"USAGE IN SECONDS\", " \
                     "ZSTREAMNAME," \
                     "ZVALUESTRING " \
                     "FROM " \
                     "ZOBJECT " \
                     "WHERE " \
                     "ZSTREAMNAME IS \"/app/inFocus\" " \
                     "ORDER BY \"START\""

        headers = "ENTRY CREATION\tDAY OF WEEK\tGMT OFFSET\tSTART\tEND\tUSAGE IN SECONDS\tSTREAMNAME\tVALUESTRING\r\n"

        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as output_file:
            output_file.write("=" * 10 + " " + self._name + " " + "=" * 10 + "\r\n")
            file = os.path.join(self._input_dir, "private", "var", "db", "CoreDuet", "Knowledge", self._data_file)
            output_file.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra"]:
                if os.path.isfile(file):
                    conn = None
                    try:
                        sqlite_connection = sqlite3.connect(file)
                        sqlite_connection.row_factory = sqlite3.Row
                        with sqlite_connection:
                            cur = sqlite_connection.cursor()
                            cur.execute(mac4n6_sql)
                            rows = cur.fetchall()
                            output_file.write(headers)
                            for row in rows:
                                output_file.write("{0}\t".format(row["ENTRY CREATION"]))
                                output_file.write("{0}\t".format(row["DAY OF WEEK"]))
                                output_file.write("{0}\t".format(row["GMT OFFSET"]))
                                output_file.write("{0}\t".format(row["START"]))
                                output_file.write("{0}\t".format(row["END"]))
                                output_file.write("{0}\t".format(row["USAGE IN SECONDS"]))
                                output_file.write("{0}\t".format(row["ZSTREAMNAME"]))
                                output_file.write("{0}\t".format(row["ZVALUESTRING"]))
                                output_file.write("\r\n")
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

            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard", "sierra",
                                      "el_capitan"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                output_file.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            output_file.write("=" * 40 + "\r\n\r\n")
        output_file.close()
