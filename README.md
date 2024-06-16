# osm2sqlite

A simple command line tool for reading OpenStreetMap XML data into a SQLite database.

```
Usage:
osm2sqlite SQLITE_DATABASE OSM_XML_FILE [OPTION]...

Options:
  rtree         Add R*Tree indexes
  addr          Add address tables
  graph         Add graph table
  noindex       Do not create indexes (not recommended)

When OSM_XML_FILE is -, read standard input.
```

The command `osm2sqlite output.db input.osm` reads the
[OSM XML](https://wiki.openstreetmap.org/wiki/OSM_XML) file **input.osm** and
creates in the database **output.db** the [tables and indexes](doc/2_tables.md).  

OSM data can be obtained from a provider such as [Geofabrik](https://download.geofabrik.de).

After reading in the data, additional data can be created with some [options](doc/3_options.md).

|[**Download the latest version**](https://github.com/osmzoso/osm2sqlite/releases/latest)|
|----------------------------------------------------------------------------------------|

---

## Miscellaneous

There are two programme versions:  
- a version in Python as a prototype (./src_py)  
- a version in C (./src)  

Time measurement for **saarland.osm (700 MB)**:  
Python : 2 minutes 36 seconds  
C      : 47 seconds  

---

Directory [/doc](doc/) contains some documentation.  
Directory [/queries](queries/) contains some perhaps useful queries.  
Directory [/test](test/) contains testcases.  

Directory [/doc](doc/osm2sqlite.html) contains the documentation.  

---

Compiling the C version on Linux for Windows, see file **cross_compile_windows.sh**.

---

The bash script `example_db.sh` invokes the scripts to show the function.
