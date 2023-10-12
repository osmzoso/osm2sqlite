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

The database can be easily queried with the [SQLite CLI tool](https://www.sqlite.org/cli.html).

OSM data can be obtained from a provider such as [Geofabrik](https://download.geofabrik.de).

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

Internally, the index is generated with the following commands:

``` sql
CREATE VIRTUAL TABLE rtree_way USING rtree(way_id, min_lat, max_lat, min_lon, max_lon);

INSERT INTO rtree_way (way_id, min_lat, max_lat, min_lon, max_lon)
SELECT way_nodes.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)
FROM way_nodes
LEFT JOIN nodes ON way_nodes.node_id=nodes.node_id
GROUP BY way_nodes.way_id;
```

Here are some examples for using this index:

``` sql
--
-- Boundingbox
--
-- min_lon (x1):  7.3280550
-- min_lat (y1): 49.3540703
-- max_lon (x2):  7.3316550
-- max_lat (y2): 49.3576703
--
```

Find all elements of the index (ways) that are contained within the boundingbox:

``` sql
SELECT way_id
FROM rtree_way
WHERE min_lon>= 7.3280550 AND max_lon<= 7.3316550
 AND  min_lat>=49.3540703 AND max_lat<=49.3576703
```

Find all elements of the index (ways) that overlap the boundingbox:

``` sql
SELECT way_id
FROM rtree_way
WHERE max_lon>= 7.3280550 AND min_lon<= 7.3316550
 AND  max_lat>=49.3540703 AND min_lat<=49.3576703
```

Limits of an element of the index:

``` sql
SELECT min_lon,max_lon,min_lat,max_lat
FROM rtree_way
WHERE way_id=79235038
```

### Option `addr`

This option creates 2 tables with address data.

Table **addr_street**:

column       | type                | description
-------------|---------------------|-------------------------------------
street_id    | INTEGER PRIMARY KEY | street ID
postcode     | TEXT                | postcode
city         | TEXT                | city
street       | TEXT                | street
min_lon      | REAL                | boundingbox min. longitude
min_lat      | REAL                | boundingbox min. latitude
max_lon      | REAL                | boundingbox max. longitude
max_lat      | REAL                | boundingbox max. latitude

- INDEX addr_street_1 ON addr_street (postcode,city,street)

Table **addr_housenumber**:

column         | type                | description
---------------|---------------------|-------------------------------------
housenumber_id | INTEGER PRIMARY KEY | housenumber ID
street_id      | INTEGER             | street ID
housenumber    | TEXT                | housenumber
lon            | REAL                | longitude
lat            | REAL                | latitude
way_id         | INTEGER             | way ID
node_id        | INTEGER             | node ID

- INDEX addr_housenumber_1 ON addr_housenumber (street_id)

The view **addr_view** join the two tables.  

### Option `graph`

This option creates a table **graph** in the database.  
This table contains the complete graph of all streets.  

Table **graph**:

column          | type                | description
----------------|---------------------|-------------------------------------
edge_id         | INTEGER PRIMARY KEY | edge ID
start\_node\_id | INTEGER             | edge start node ID
end\_node\_id   | INTEGER             | edge end node ID
dist            | INTEGER             | distance in meters
way_id          | INTEGER             | way ID

Visualization of the table 'graph':  

![table_graph.jpg](./images/table_graph.jpg)

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
7z e -so germany.osm.bz2 | osm2sqlite - germany.db
bzip2 -c -d ./xml/saarland.osm.bz2 | osm2sqlite.py - ./database/saarland.db addr
```

