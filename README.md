# osm2sqlite

Read OpenStreetMap data in XML format into a SQLite database

With

    python osm2sqlite.py input_xml.osm

a database **osm.sqlite3** is created.



## Tables and Indexes in the database


Table **nodes**:

name        | type                | description
------------|---------------------|------------------
node_id     | INTEGER PRIMARY KEY | node ID
lat         | REAL                | latitude
lon         | REAL                | longitude


Table **node_tags**:

name        | type                | description
------------|---------------------|------------------
node_id     | INTEGER             | node ID
key         | TEXT                | tag key
value       | TEXT                | tag value

- INDEX node_tags__node_id ON node_tags (node_id)
- INDEX node_tags__key     ON node_tags (key)


Table **way_tags**:

name        | type                | description
------------|---------------------|------------------
way_id      | INTEGER             | way ID
key         | TEXT                | tag key
value       | TEXT                | tag value

- INDEX way_tags__way_id   ON way_tags (way_id)
- INDEX way_tags__key      ON way_tags (key)


Table **way_nodes**:

name        | type                | description
------------|---------------------|------------------
way_id      | INTEGER             | way ID
local_order | INTEGER             | nodes sorting
node_id     | INTEGER             | node ID

- INDEX way_nodes__way_id  ON way_nodes (way_id)
- INDEX way_nodes__node_id ON way_nodes (node_id)



## Spatial Index


Additionally a R*Tree index _highway_ is created for
all ways with key='highway'.
