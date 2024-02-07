A simple command line tool for reading OpenStreetMap XML data into a SQLite database.

# 1. Read OSM XML data

Read file **test.osm** into database **test.db**:  
`osm2sqlite test.db test.osm`  

The database can be easily queried with the [SQLite CLI tool](https://www.sqlite.org/cli.html).

OSM data can be obtained from a provider such as [Geofabrik](https://download.geofabrik.de).

The OSM XML data is provided as bzip2 compressed data.

To avoid unpacking the bzip2 file, the tool can read from stdin.

Read .osm.bz2 file:  
`7z e -so ../germany.osm.bz2 | osm2sqlite germany.db -`  
`bzip2 -c -d ../germany.osm.bz2 | osm2sqlite germany.db -`  

> The .osm.bz2 format is [deprecated](https://download.geofabrik.de/bz2.html).  
> In future, only .osm.pbf files will be provided from Geofabrik.

The tool **osmium** can convert .osm.pbf files to .osm.

Install osmium on Fedora Linux:  
`sudo dnf install osmium-tool.x86_64`  

Convert .osm.pbf to osm, output to stdout:   
`osmium cat myfile.osm.pbf --output-format=osm --output=- | less -S`  
`osmium cat myfile.osm.pbf -f osm -o - | less -S`  

Convert myfile.osm.pbf to myfile.osm.bz2:  
`osmium cat myfile.osm.pbf -o myfile.osm.bz2`

Read .osm.pbf file into a SQLite database:  
`osmium cat freiburg.osm.pbf -f osm -o - | osm2sqlite freiburg.db -`
