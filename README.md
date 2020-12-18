# osm2sqlite

Reads [OpenStreetMap data in XML format](https://wiki.openstreetmap.org/wiki/OSM_XML) into a SQLite database.

The command
```
python osm2sqlite.py input.osm
```
reads the file *input.osm* and creates
a new database **osm.sqlite3** with the tables below.

> Time measurement (Intel Core i5 1.6 GHz):  
> germany.osm - about 3 hours


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

- INDEX relation_members__relation_id ON relation_members ( relation_id )
- INDEX relation_members__type        ON relation_members ( type, ref )


### relation_tags

column       | type                | description
-------------|---------------------|-------------------------------------
relation_id  | INTEGER             | relation ID
key          | TEXT                | tag key
value        | TEXT                | tag value

- INDEX relation_tags__relation_id    ON relation_tags ( relation_id )
- INDEX relation_tags__key            ON relation_tags ( key )


The command
```
python osm2sqlite.py input.osm --omit_index
```
suppresses the creation of all indexes.


---

## Example Queries


Here are some examples for querying the database **osm.sqlite3**:


#### List of all cell phone antennas

```
sqlite3 osm.sqlite3 < query_cell_phone_antennas.sql
```


#### Separate Database with all addresses

With the command
```
sqlite3 < query_address_database.sql
```
a new database **osm_addr.sqlite3** with all addresses is created.


---

## Spatial Index


The command
```
sqlite3 osm.sqlite3 < spatial_index.sql
```
creates a [R*Tree index](https://www.sqlite.org/rtree.html) **highway** for
all ways with *key='highway'*.


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
