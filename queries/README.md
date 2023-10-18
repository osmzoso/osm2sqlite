# Queries

This directory may contain useful queries.

The database can be easily queried with the [SQLite CLI tool](https://www.sqlite.org/cli.html).


## R*Tree index "rtree_way"

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


## Adress tables

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


## Table size

Output from `sqlite3_analyzer freiburg-regbez-latest.db`:

```
/** Disk-Space Utilization Report For freiburg-regbez-latest.db

Page size in bytes................................ 65536     
...

*** Page counts for all tables and indices separately *************************

WAY_NODES......................................... 5940        17.8% 
NODES............................................. 5727        17.1% 
WAY_NODES__WAY_ID................................. 4339        13.0% 
WAY_NODES__NODE_ID................................ 4181        12.5% 
WAY_TAGS.......................................... 3313         9.9% 
WAY_TAGS__KEY..................................... 1894         5.7% 
WAY_TAGS__WAY_ID.................................. 1340         4.0% 
RTREE_WAY_NODE.................................... 1156         3.5% 
NODE_TAGS......................................... 1103         3.3% 
NODE_TAGS__KEY.................................... 604          1.8% 
RELATION_MEMBERS.................................. 480          1.4% 
RTREE_WAY_ROWID................................... 472          1.4% 
NODE_TAGS__NODE_ID................................ 469          1.4% 
GRAPH............................................. 374          1.1% 
ADDR_HOUSENUMBER.................................. 356          1.1% 
RELATION_MEMBERS__TYPE............................ 320          0.96% 
RTREE_HIGHWAY_NODE................................ 287          0.86% 
RELATION_MEMBERS__RELATION_ID..................... 279          0.84% 
GRAPH__WAY_ID..................................... 180          0.54% 
RELATION_TAGS..................................... 152          0.46% 
RTREE_HIGHWAY_ROWID............................... 111          0.33% 
ADDR_HOUSENUMBER__STREET_ID....................... 102          0.31% 
RELATION_TAGS__KEY................................ 70           0.21% 
RELATION_TAGS__RELATION_ID........................ 51           0.15% 
ADDR_STREET....................................... 50           0.15% 
ADDR_STREET__POSTCODE_CITY_STREET................. 27           0.081% 
RTREE_WAY_PARENT.................................. 14           0.042% 
RTREE_HIGHWAY_PARENT.............................. 4            0.012% 
SQLITE_SCHEMA..................................... 1            0.003% 
```

