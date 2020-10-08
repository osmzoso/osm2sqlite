# osm2sqlite

Reads [OpenStreetMap data in XML format](https://wiki.openstreetmap.org/wiki/OSM_XML) into a SQLite database.

The command
```shell
python osm2sqlite.py input.osm
```
reads the file *input.osm* and creates
a new database **osm.sqlite3** with the tables below.

> Time measurement (Intel Core i5 1.6 GHz, 16 GB RAM):  
> germany-latest.osm - about 3 hours


## nodes

column      | type                | description
------------|---------------------|------------------
node_id     | INTEGER PRIMARY KEY | node ID
lat         | REAL                | latitude
lon         | REAL                | longitude


## node_tags

column      | type                | description
------------|---------------------|------------------
node_id     | INTEGER             | node ID
key         | TEXT                | tag key
value       | TEXT                | tag value

- INDEX node_tags__node_id ON node_tags (node_id)
- INDEX node_tags__key     ON node_tags (key)


## way_nodes

column      | type                | description
------------|---------------------|------------------
way_id      | INTEGER             | way ID
node_id     | INTEGER             | node ID
node_order  | INTEGER             | node order

- INDEX way_nodes__way_id  ON way_nodes (way_id)
- INDEX way_nodes__node_id ON way_nodes (node_id)


## way_tags

column      | type                | description
------------|---------------------|------------------
way_id      | INTEGER             | way ID
key         | TEXT                | tag key
value       | TEXT                | tag value

- INDEX way_tags__way_id   ON way_tags (way_id)
- INDEX way_tags__key      ON way_tags (key)


## relation_members

column       | type                | description
-------------|---------------------|------------------
relation_id  | INTEGER             | relation ID
type         | TEXT                | type (node or way)
ref          | INTEGER             | ID (node or way ID)
role         | TEXT                | role (from via to)
member_order | INTEGER             | member order

- INDEX relation_members__relation_id ON relation_members ( relation_id )
- INDEX relation_members__type        ON relation_members ( type, ref )


## relation_tags

column       | type                | description
-------------|---------------------|------------------
relation_id  | INTEGER             | relation ID
key          | TEXT                | tag key
value        | TEXT                | tag value

- INDEX relation_tags__relation_id    ON relation_tags ( relation_id )
- INDEX relation_tags__key            ON relation_tags ( key )


---

### Spatial Index

Additionally a [R*Tree index](https://www.sqlite.org/rtree.html) _highway_ is created for
all ways with key='highway'.

``` sql
--
-- Boundingbox (Reiskirchen im Saarland, Sportplatz)
--
-- bbox_min_lon:  7.3298550-0.0018 (X)
-- bbox_max_lon:  7.3298550+0.0018
-- bbox_min_lat: 49.3558703-0.0018 (Y)
-- bbox_max_lat: 49.3558703+0.0018
--
```

Find all elements of the index that are contained within an area:

``` sql
SELECT way_id FROM highway
WHERE min_lon>= 7.3298550-0.0018 AND max_lon<= 7.3298550+0.0018
 AND  min_lat>=49.3558703-0.0018 AND max_lat<=49.3558703+0.0018
```

Find all bounding boxes that overlap the area:

``` sql
SELECT way_id FROM highway
WHERE max_lon>= 7.3298550-0.0018 AND min_lon<= 7.3298550+0.0018
 AND  max_lat>=49.3558703-0.0018 AND min_lat<=49.3558703+0.0018
```

Limit of a bounding box:

``` sql
SELECT * FROM highway WHERE way_id=79235038
```


---

### Examples for database queries

TODO

