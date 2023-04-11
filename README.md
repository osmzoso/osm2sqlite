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

- INDEX way_nodes__way_id  ON way_nodes (way_id)
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

- INDEX relation_members__relation_id ON relation_members (relation_id)
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

After reading in the data, additional data can be created with various options.

### no-index

The `no-index` option suppresses the creation of the indexes (not recommended).

### rtree-ways

The `rtree-ways` option creates an additional [R*Tree](https://www.sqlite.org/rtree.html)
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

Here are some examples for querying this index:

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

### addr

The `addr` option creates 2 tables with address data.
Table **addr_street** contains postcode, city, street and boundingbox of the street.  
Table **addr_housenumber** contains the coordinates of each housenumber.  
In addition, a view **addr_view** is created.  


---

## Miscellaneous

Time measurement for **saarland.osm (700 MB)** (Intel(R) Pentium(R) Silver J5005 CPU @ 1.50GHz):  

Python : 2 minutes 36 seconds  
C      : 47 seconds  

---

Compiling the C version on Linux (Fedora 37):  

*libsqlite3* and *libxml2* are required. Additional the *devel*-packages are required:  

    sudo dnf sqlite-devel.x86_64
    sudo dnf libxml2-devel.x86_64

Compile:

    gcc osm2sqlite.c -lsqlite3 -lxml2 -o osm2sqlite -Wall -Os -s -I/usr/include/libxml2

See also file *compile_osm2sqlite_c.sh*.

---

Reading a file compressed with bzip2 without unpacking it first:

The C version is able to read from stdin.

Examples:
```
7z e -so germany.osm.bz2 | osm2sqlite - germany.db
bzip2 -c -d ./xml/saarland-latest.osm.bz2 | osm2sqlite - ./database/saarland-latest.db addr rtree-ways
```

---

Directory /test

To test the program, the databases of the two program versions are compared.

It has been found that the mantissa rarely differs by 1 bit.  
However, this should not be a problem for calculations.  

```
+-------------+-------+-----------------------------+-----------------------------+---------------------+---------------------+
|   node_id   |  db   |    format("%!.50f",lon)     |    format("%!.50f",lat)     |    binary64_lon     |    binary64_lat     |
+-------------+-------+-----------------------------+-----------------------------+---------------------+---------------------+
| 536141      | db_c  | 7.3532162000000003132527126 | 49.310166099999996449157468 | x'401d69b181edab6a' | x'4048a7b385d3e9f7' |
| 536141      | db_py | 7.3532162000000003132527126 | 49.310166100000003552850103 | x'401d69b181edab6a' | x'4048a7b385d3e9f8' |
| 21520090    | db_c  | 7.09182739999999967039912   | 49.313916999999996447143213 | x'401c5e08007f81c0' | x'4048a82e6ea85447' |
| 21520090    | db_py | 7.09182739999999967039912   | 49.313917000000003555172656 | x'401c5e08007f81c0' | x'4048a82e6ea85448' |
| 33743557    | db_c  | 7.2362995000000003287254912 | 49.505478599999996449157468 | x'401cf1f87f023e9f' | x'4048c0b385d3e9f7' |
| 33743557    | db_py | 7.2362995000000003287254912 | 49.505478600000003552850103 | x'401cf1f87f023e9f' | x'4048c0b385d3e9f8' |
| 36160300    | db_c  | 7.2409255000000003477111931 | 49.575184900000003550800398 | x'401cf6b52c9d16fd' | x'4048c99fa8a75397' |
| 36160300    | db_py | 7.2409255000000003477111931 | 49.575184899999996447107764 | x'401cf6b52c9d16fd' | x'4048c99fa8a75396' |
+-------------+-------+-----------------------------+-----------------------------+---------------------+---------------------+
```

