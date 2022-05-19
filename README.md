# osm2sqlite

Reads OpenStreetMap XML data into a SQLite database.

The command
```
osm2sqlite input.osm output.db
```
reads the [OSM XML](https://wiki.openstreetmap.org/wiki/OSM_XML) file
**input.osm** and creates in the database **output.db** the tables and indexes below.

(The command `osm2sqlite input.osm output.db --no-index` suppresses the creation of the indexes)

The database can be easily queried with the [SQLite CLI tool](https://www.sqlite.org/cli.html).

|[**Download the latest version**](https://github.com/osmzoso/osm2sqlite/releases/latest)|
|----------------------------------------------------------------------------------------|

---

> Time measurement (Intel Core i5 1.6 GHz):  
> saarland.osm (700 MB) - about 32 seconds  
> germany.osm (60 GB) - about 1 hour 10 minutes  

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

## Add tables with all addresses

The command `sqlite3 output.db < ./query/add_addr.sql` generates 2 tables:

Table **addr_street** contains postcode, city, street and boundingbox of the street.  
Table **addr_housenumber** contains the coordinates of each housenumber.  
In addition, a view **addr_view** is created.  


---

## Add a spatial index


The command
```
osm2sqlite input.osm output.db --spatial-index
```
creates an additional [R*Tree index](https://www.sqlite.org/rtree.html) **highway** for
all ways with *key='highway'*.

Internally, the index is generated with the following commands:

``` sql
CREATE VIRTUAL TABLE highway USING rtree( way_id, min_lat, max_lat, min_lon, max_lon );

INSERT INTO highway (way_id,min_lat,       max_lat,       min_lon,       max_lon)
SELECT      way_tags.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)
FROM      way_tags
LEFT JOIN way_nodes ON way_tags.way_id=way_nodes.way_id
LEFT JOIN nodes     ON way_nodes.node_id=nodes.node_id
WHERE way_tags.key='highway'
GROUP BY way_tags.way_id;
```

Here are some examples for querying this index:

``` sql
--
-- Boundingbox (Reiskirchen im Saarland, Sportplatz)
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
FROM highway
WHERE min_lon>= 7.3280550 AND max_lon<= 7.3316550
 AND  min_lat>=49.3540703 AND max_lat<=49.3576703
```

Find all elements of the index (ways) that overlap the boundingbox:

``` sql
SELECT way_id
FROM highway
WHERE max_lon>= 7.3280550 AND min_lon<= 7.3316550
 AND  max_lat>=49.3540703 AND min_lat<=49.3576703
```

Limits of an element of the index:

``` sql
SELECT min_lon,max_lon,min_lat,max_lat
FROM highway
WHERE way_id=79235038
```

