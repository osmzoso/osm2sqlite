# 1. osm2sqlite

A simple command line tool for reading OpenStreetMap XML data into a SQLite database.

```
Usage:
osm2sqlite FILE_OSM_XML FILE_SQLITE_DB [option ...]
```

The database can be easily queried with the [SQLite CLI tool](https://www.sqlite.org/cli.html).


To avoid unpacking the bzip2 file, both versions can read from stdin.

Examples:
```
7z e -so germany.osm.bz2 | osm2sqlite - germany.db addr
bzip2 -c -d ./xml/saarland.osm.bz2 | osm2sqlite.py - ./database/saarland.db
```

