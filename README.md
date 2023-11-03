# osm2sqlite

A command line tool for reading OpenStreetMap XML data into a SQLite database.

```
Usage:
osm2sqlite FILE_OSM_XML FILE_SQLITE_DB [option ...]
```

The command `osm2sqlite input.osm output.db` reads the
[OSM XML](https://wiki.openstreetmap.org/wiki/OSM_XML) file **input.osm** and
creates in the database **output.db** the tables and indexes.  
A description of the tables can be found [here](doc/2_tables.md)

OSM data can be obtained from a provider such as [Geofabrik](https://download.geofabrik.de).

After reading in the data, additional data can be created with some options.  
More information about the options can be found [here](doc/3_options.md)

The `rtree-ways` option creates an additional [R*Tree](https://www.sqlite.org/rtree.html)
index **rtree_way** for finding ways quickly.  

The `addr` option creates tables **addr_street** and **addr_housenumber** with addresses.  

The `graph` option creates an additional table **graph** with the complete graph
of all highways. This data is required for routing purposes.  

The `no-index` option suppresses the creation of the indexes (not recommended).

|[**Download the latest version**](https://github.com/osmzoso/osm2sqlite/releases/latest)|
|----------------------------------------------------------------------------------------|

---

## Miscellaneous

There is a version in Python as a prototype and there is a version in C.

Time measurement for **saarland.osm (700 MB)**:  
Python : 2 minutes 36 seconds  
C      : 47 seconds  

---

Directory [/routing](doc/5_routing.md) contains some routing experiments.  
Directory [/mapdrawing](doc/4_mapdrawing.md) contains some scripts to draw a map.  
Directory [/check_data](check_data/README.md) contains some scripts to check the data.  
Directory [/queries](queries/README.md) contains some perhaps useful queries.  
Directory [/test](test/README.md) contains testcases.  

---

Compiling the C version on Linux for Windows, see file **cross_compile_win.sh**.

---

The bash script `example_db.sh` invokes the scripts to show the function.

