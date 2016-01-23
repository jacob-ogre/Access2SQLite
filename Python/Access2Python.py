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

import os
import sqlite3 as lite
import sys

def main():
    make_tmpdir()
    tables = get_schema()
    write_CSVs(tables)
    load_to_SQLite()
    compress_CSVs()

def make_tmpdir():
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)
