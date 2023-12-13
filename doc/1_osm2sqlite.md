# 1. osm2sqlite

A simple command line tool for reading OpenStreetMap XML data into a SQLite database.

The command `osm2sqlite input.osm output.db` reads the OSM XML file **input.osm** and
creates in the database **output.db** the tables and indexes.  

The database can be easily queried with the [SQLite CLI tool](https://www.sqlite.org/cli.html).

To avoid unpacking the bzip2 file, the tool can read from stdin.

Examples:  
`7z e -so germany.osm.bz2 | osm2sqlite - germany.db addr`  
`bzip2 -c -d ./xml/saarland.osm.bz2 | osm2sqlite.py - ./database/saarland.db`  

The .osm.bz2 format is deprecated. In future, only .osm.pbf files will be provided.

Convert .osm.pbf to osm.bz2 with "osmium":  
`osmium cat freiburg-regbez-latest.osm.pbf -o freiburg-regbez-latest.osm.bz2`

Install osmium on Fedora Linux:  
`sudo dnf install osmium-tool.x86_64`  

Convert .osm.pbf to osm with "osmium", output to stdout:   
`osmium cat bremen-latest.osm.pbf -f osm -o - | less -S`  
`osmium cat bremen-latest.osm.pbf --output-format=osm --output=- | less -S`  

Example to read .osm.pbf file with "osmium":  
`osmium cat freiburg.osm.pbf --output-format=osm --output=- | osm2sqlite - freiburg.db`

