# osm2sqlite

A command line tool for reading OpenStreetMap XML data into a SQLite database.

```
Usage:
osm2sqlite FILE_OSM_XML FILE_SQLITE_DB [option ...]
```

The command `osm2sqlite input.osm output.db` reads the
[OSM XML](https://wiki.openstreetmap.org/wiki/OSM_XML) file **input.osm** and
creates in the database **output.db** the tables and indexes below.

The option `no-index` suppresses the creation of the indexes (not recommended).

OSM data can be obtained from a provider such as [Geofabrik](https://download.geofabrik.de).

The bash script `example_db.sh` invokes the scripts to show the function.

|[**Download the latest version**](https://github.com/osmzoso/osm2sqlite/releases/latest)|
|----------------------------------------------------------------------------------------|

---

## Tables and Indexes

### nodes

column       | type                | description
-------------|---------------------|-------------------------------------
node_id      | INTEGER PRIMARY KEY | node ID
lon          | REAL                | longitude
lat          | REAL                | latitude


### node_tags

column       | type                | description
-------------|---------------------|-------------------------------------
node_id      | INTEGER             | node ID
key          | TEXT                | tag key
value        | TEXT                | tag value

- INDEX node_tags__node_id ON node_tags (node_id)
- INDEX node_tags__key     ON node_tags (key)


### way_nodes

column       | type                | description
-------------|---------------------|-------------------------------------
way_id       | INTEGER             | way ID
node_id      | INTEGER             | node ID
node_order   | INTEGER             | node order

- INDEX way_nodes__way_id  ON way_nodes (way_id, node_order)
- INDEX way_nodes__node_id ON way_nodes (node_id)


### way_tags

column       | type                | description
-------------|---------------------|-------------------------------------
way_id       | INTEGER             | way ID
key          | TEXT                | tag key
value        | TEXT                | tag value

- INDEX way_tags__way_id   ON way_tags (way_id)
- INDEX way_tags__key      ON way_tags (key)


### relation_members

column       | type                | description
-------------|---------------------|-------------------------------------
relation_id  | INTEGER             | relation ID
type         | TEXT                | type ('node','way','relation')
ref          | INTEGER             | node, way or relation ID
role         | TEXT                | describes a particular feature
member_order | INTEGER             | member order

- INDEX relation_members__relation_id ON relation_members (relation_id, member_order)
- INDEX relation_members__type        ON relation_members (type, ref)


### relation_tags

column       | type                | description
-------------|---------------------|-------------------------------------
relation_id  | INTEGER             | relation ID
key          | TEXT                | tag key
value        | TEXT                | tag value

- INDEX relation_tags__relation_id    ON relation_tags (relation_id)
- INDEX relation_tags__key            ON relation_tags (key)


---

## Options

After reading in the data, additional data can be created with some options.

### Option `rtree-ways`

This option creates an additional [R*Tree](https://www.sqlite.org/rtree.html)
index **rtree_way** for finding ways quickly.  
Examples of querying this index can be found [here](queries/README.md).

### Option `addr`

This option creates tables **addr_street** and **addr_housenumber** with addresses.  
A description of these tables can be found [here](queries/README.md#adress-tables).  

### Option `graph`

This option creates an additional table **graph** with the complete graph
of all highways. This data is required for routing purposes.  
More information can be found [here](routing/README.md).

### Option `no-index`

This option suppresses the creation of the indexes (not recommended).


---

## Miscellaneous

There is a version in Python as a prototype and there is a version in C.

Time measurement for **saarland.osm (700 MB)**:  
Python : 2 minutes 36 seconds  
C      : 47 seconds  

---

Directory [/routing](routing/README.md) contains some routing experiments.  
Directory [/mapdrawing](mapdrawing/README.md) contains some scripts to draw a map.  
Directory [/check_data](check_data/README.md) contains some scripts to check the data.  
Directory [/queries](queries/README.md) contains some perhaps useful queries.  
Directory [/test](test/README.md) contains testcases.  

---

Compiling the C version on Linux for Windows, see file **cross_compile_win.sh**.

---

To avoid unpacking the bzip2 file, both versions can read from stdin.

Examples:
```
7z e -so germany.osm.bz2 | osm2sqlite - germany.db addr
bzip2 -c -d ./xml/saarland.osm.bz2 | osm2sqlite.py - ./database/saarland.db
```

