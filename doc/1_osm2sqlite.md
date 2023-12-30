# 1. osm2sqlite

A simple command line tool for reading OpenStreetMap XML data into a SQLite database.

Examples:

Read the OSM XML file **test.osm** and create the tables and indexes in the database **test.db**:  
`osm2sqlite test.osm test.db`  

OSM data can be obtained from a provider such as [Geofabrik](https://download.geofabrik.de).

The OSM XML data is provided as bzip2 compressed data.

To avoid unpacking the bzip2 file, the tool can read from stdin.

Read .osm.bz2 file:  
`7z e -so germany.osm.bz2 | osm2sqlite - germany.db addr`  
`bzip2 -c -d ./xml/saarland.osm.bz2 | osm2sqlite.py - ./database/saarland.db`  

The .osm.bz2 format is deprecated. In future, only .osm.pbf files will be provided.

The tool "osmium" can convert .osm.pbf files to .osm.

Example to read .osm.pbf file with "osmium":  
`osmium cat freiburg.osm.pbf --output-format=osm --output=- | osm2sqlite - freiburg.db`

Convert .osm.pbf to osm.bz2 with "osmium":  
`osmium cat freiburg-regbez-latest.osm.pbf -o freiburg-regbez-latest.osm.bz2`

Install osmium on Fedora Linux:  
`sudo dnf install osmium-tool.x86_64`  

Convert .osm.pbf to osm with "osmium", output to stdout:   
`osmium cat bremen-latest.osm.pbf -f osm -o - | less -S`  
`osmium cat bremen-latest.osm.pbf --output-format=osm --output=- | less -S`  

The database can be easily queried with the [SQLite CLI tool](https://www.sqlite.org/cli.html).

