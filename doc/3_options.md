# 3. Options

## Overview

The `rtree-ways` option creates an additional [R*Tree](https://www.sqlite.org/rtree.html)
index **rtree_way** for finding ways quickly.  

The `addr` option creates tables **addr_street** and **addr_housenumber** with addresses.  

The `graph` option creates an additional table **graph** with the complete graph
of all highways. This data is required for routing purposes.  

The `no-index` option suppresses the creation of the indexes (not recommended).


## Option "rtree-ways"

Add R*Tree index **"rtree_way"**.  
The index is generated with the following commands:

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


## Option "addr"

Add adress tables.

Table **addr_street**:

```
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
```

Table **addr_housenumber**:

```
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
```

The view **addr_view** join the two tables.  


## Option "graph"

Add table **graph**:

```
column          | type                | description
----------------|---------------------|-------------------------------------
edge_id         | INTEGER PRIMARY KEY | edge ID
start\_node\_id | INTEGER             | edge start node ID
end\_node\_id   | INTEGER             | edge end node ID
dist            | INTEGER             | distance in meters
way_id          | INTEGER             | way ID
```

Query table "graph" to create a smaller subgraph:

``` sql
/*
** 1. Create temp. table with edges of the subgraph
**    - R*Tree 'rtree_way' is required, overlaps boundingbox slightly
**
** Boundingbox:
** min_lon (x1):  7.81
** min_lat (y1): 47.97
** max_lon (x2):  7.83
** max_lat (y2): 47.98
*/
CREATE TEMP TABLE subgraph AS
SELECT edge_id,start_node_id,end_node_id,dist,way_id
FROM graph
WHERE way_id IN (
 SELECT way_id
 FROM rtree_way
 WHERE max_lon>= 7.81 AND min_lon<= 7.83
  AND  max_lat>=47.97 AND min_lat<=47.98
)
```

``` sql
/*
** 2. Create temp. table with list of nodes in subgraph
**    - Conversion list from node id to a number from 1 to N
*/
CREATE TEMP TABLE subgraph_nodes (
 no      INTEGER PRIMARY KEY,
 node_id INTEGER,
 lon     REAL,
 lat     REAL
)
;
INSERT INTO subgraph_nodes (node_id, lon, lat)
SELECT s.node_id,n.lon,n.lat FROM
(
 SELECT start_node_id AS node_id FROM subgraph
 UNION
 SELECT end_node_id AS node_id FROM subgraph
) AS s
LEFT JOIN nodes AS n ON s.node_id=n.node_id
;
```

``` sql
-- Number of nodes in the subgraph
SELECT max(no) FROM subgraph_nodes
```

``` sql
-- Edges with number of nodes from 1 to N
SELECT s.edge_id,sns.no,sne.no,s.dist,s.way_id
FROM subgraph AS s
LEFT JOIN subgraph_nodes AS sns ON s.start_node_id=sns.node_id
LEFT JOIN subgraph_nodes AS sne ON s.end_node_id=sne.node_id
```


## Option "no-index"

This option suppresses the creation of the indexes (not recommended).
