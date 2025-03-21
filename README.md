# osm2sqlite

A simple command line tool for reading OpenStreetMap XML data into a SQLite database.

```
Usage:
osm2sqlite DATABASE OSM_FILE [OPTION]...

Options:
  rtree         Add R*Tree indexes
  addr          Add address tables
  graph         Add graph table
  noindex       Do not create indexes (not recommended)

When OSM_FILE is -, read standard input.
```

The command
```
osm2sqlite output.db input.osm
```
reads the [OSM XML](https://wiki.openstreetmap.org/wiki/OSM_XML) file **input.osm**
and creates in the database **output.db** the tables.

Some options can be used to create additional data.

The tables are described in the [documentation](doc/doc_osm2sqlite.md).

OSM data can be obtained from a provider such as [Geofabrik](https://download.geofabrik.de).

There are two program versions:  
- a Python version in a single file as a prototype (see ./tools/osm2sqlite.py)  
- a version in C in ./src (see [compilation notes](doc/compile-osm2sqlite.md))  

Runtime for a 700 MByte OSM file:  
Python : 2 minutes 36 seconds  
C      : 47 seconds  

|[**Download the latest version**](https://github.com/osmzoso/osm2sqlite/releases/latest)|
|----------------------------------------------------------------------------------------|

