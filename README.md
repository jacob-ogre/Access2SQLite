# Access2SQLite
A small script to convert an Access database to an SQLite database.

Depends, critically, on [mdbtools from @brianb](https://github.com/brianb/mdbtools). The code isn't particularly safe - it uses `subprocess.call(..., shell=True)` at one point, so that should be changed if used in anything that's accessible from outside.
