# osm2sqlite

A simple command line tool for reading OpenStreetMap XML data into a SQLite database.

```
Usage:
osm2sqlite DATABASE [OPTION ...]

Options:
  read FILE    Reads FILE into the database
               (When FILE is -, read stdin)
  rtree        Add R*Tree indexes
  addr         Add address tables
  graph        Add graph table
```

The command
```
osm2sqlite test.db read country.osm
```
reads the [OSM XML](https://wiki.openstreetmap.org/wiki/OSM_XML) file **country.osm**
and writes the data to in the **test.db** database.

The tables are described in the [documentation](doc/osm2sqlite.md).

Some options can be used to create additional data.

OSM data can be obtained from a provider such as [Geofabrik](https://download.geofabrik.de).

There are two program versions:  
- a prototype in Python (see ./test/osm2sqlite.py)
- a version in C (see [compiling annotations](doc/compiling_annotations.md))

Runtime for a 700 MByte OSM file:  
Python : 2 minutes 36 seconds  
C      : 47 seconds  

The [./tools](doc/tools.md) directory contains test scripts:  
- Test [drawing a map](doc/drawing_a_map.md)  
- Test [routing](doc/routing.md)  


|[**Download the latest version**](https://github.com/osmzoso/osm2sqlite/releases/latest)|
|----------------------------------------------------------------------------------------|

