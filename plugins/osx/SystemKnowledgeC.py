from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3

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
        self._name = "System KnowledgeC"
        self._description = "Parse information from /private/var/db/CoreDuet/Knowledge/KnowledgeC.db"
        self._data_file = "KnowledgeC.db"
        self._output_file = "System_KnowledgeC.txt"
        self._type = "sqlite"

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

        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("=" * 10 + " " + self._name + " " + "=" * 10 + "\r\n")
            file = os.path.join(self._input_dir, "private", "var", "db", "CoreDuet", "Knowledge", self._data_file)
            of.write("Source File: {0}\r\n\r\n".format(file))
            # if self._os_version in ["big_sur", "catalina", "mojave", "high_sierra"]:
            if self._os_version in ["catalina", "mojave", "high_sierra"]:
                if os.path.isfile(file):
                    pass
                    conn = None
                    try:
                        sqlite_connection = sqlite3.connect(file)
                        sqlite_connection.row_factory = sqlite3.Row
                        with sqlite_connection:
                            cur = sqlite_connection.cursor()
                            cur.execute(mac4n6_sql)
                            rows = cur.fetchall()
                            of.write(headers)
                            for row in rows:
                                of.write("{0}\t".format(row["ENTRY CREATION"]))
                                of.write("{0}\t".format(row["DAY OF WEEK"]))
                                of.write("{0}\t".format(row["GMT OFFSET"]))
                                of.write("{0}\t".format(row["START"]))
                                of.write("{0}\t".format(row["END"]))
                                of.write("{0}\t".format(row["USAGE IN SECONDS"]))
                                of.write("{0}\t".format(row["ZSTREAMNAME"]))
                                of.write("{0}\t".format(row["ZVALUESTRING"]))
                                of.write("\r\n")
                        of.write("\r\n")
                    except sqlite3.Error as e:
                        logging.error("{0}".format(e.args[0]))
                        print("[ERROR] {0}".format(e.args[0]))
                    finally:
                        if conn:
                            conn.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard", "sierra",
                                      "el_capitan"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("=" * 40 + "\r\n\r\n")
        of.close()
