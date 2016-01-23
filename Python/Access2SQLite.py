# A very simple script to use mdbtools to convert Access dbs to SQLite.
# Copyright (c) 2016 Defenders of Wildlife, jmalcom@defenders.org

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from glob import glob
import os
from pprint import pprint as pp
import sqlite3 as lite
import subprocess
import sys

def main():
    """A very simple script that uses mdbtools to convert Access db to SQLite.

    USAGE
        python3 Access2SQLite.py <accdb> <tmpdir> <outdb>
    ARGS
        accdb, path to an Access database (post-1997)
        tmpdir, path to a temporary directory to which Access tables are written
        outdb, path to the SQLite database version of the Access db
    DEPENDS
        mdbtools; see https://github.com/brianb/mdbtools, or use Homebrew on OSX
    NOTES
        Sets each variable type to TEXT in lieu of trying to determine the type.
        Not sure how to handle BLOBs...not sure how Access handles blobs.
    """
    make_tmpdir()
    tables = get_tables()
    write_TABs(tables)
    load_to_SQLite(tables)
    compress_TABs()

def make_tmpdir():
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)

def get_tables():
    "Return a list of tables in Access database."
    tables = []
    proc = subprocess.Popen(["mdb-schema", accdb], stdout=subprocess.PIPE)
    res = proc.stdout.read()
    data = str(res).split("\\n")
    for i in data:
        if i.startswith("CREATE TABLE"):
            s1 = i.replace("CREATE TABLE ", "").replace("[", "").replace("]", "")
            tables.append(s1)
    return tables

def write_TABs(tabs):
    "Write the tables in accdb and specified in tabs, to tab'd files."
    for i in tabs:
        outf = os.path.join(tmpdir, i + "_table.tab")
        cmd = "mdb-export -d '\t' " + accdb + " " + i + " > " + outf
        subprocess.call(cmd, shell=True)

def load_to_SQLite(tabs):
    filenames = [os.path.join(tmpdir, i + "_table.tab") for i in tabs]
    con = lite.connect(outdb)
    with con:
        cur = con.cursor()
        for f in range(len(filenames)):
            line_n = 0
            recs = []
            for line in open(filenames[f]):
                data = line.rstrip().split("\t")
                if line_n == 0:
                    colnames = [x.replace("-", "") for x in data]
                    line_n += 1
                if line_n % 1000 == 0:
                    add_records(cur, colnames, recs, tabs[f])
                    if len(data) != len(colnames):
                        missing = list(" " * len(colnames) - len(data))
                        data.extend(missing)
                    recs = [tuple(data)]
                    line_n += 1
                else:
                    if len(data) != len(colnames):
                        missing = list(" " * (len(colnames) - len(data)))
                        data.extend(missing)
                    recs.append(tuple(data))
            add_records(cur, colnames, recs, tabs[f])

def add_records(cursor, cols, records, tabname):
    drop_state = "DROP TABLE IF EXISTS %s" % tabname
    tabpart = [cols[x] + " TXT" for x in range(len(cols))]
    make_table = "CREATE TABLE " + tabname + " (" + ", ".join(tabpart) + ")"
    insert_val = "INSERT INTO %s VALUES(%s)" % \
                 (tabname, ", ".join(list(len(cols) * "?")))
    
    cursor.execute(drop_state)
    cursor.execute(make_table)
    cursor.executemany(insert_val, records)

def compress_TABs():
    pass
    
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(main.__doc__)
        sys.exit()

    args = sys.argv
    accdb = args[1]
    tmpdir = args[2]
    outdb = args[3]
    main()
