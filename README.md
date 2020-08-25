# osm2sqlite

Import of OpenStreetMap data in XML format into a SQLite database

Usage:  
python osm2sqlite.py input.osm


## Created tables in the SQLite database

    CREATE TABLE nodes (
     node_id INTEGER PRIMARX KEY,  -- node ID
     lat     REAL,                 -- latitude
     lon     REAL                  -- longitude
    )

    CREATE TABLE node_tags (
     node_id INTEGER,              -- node ID
     key     TEXT,                 -- tag key
     value   TEXT                  -- tag value
    )

    CREATE TABLE way_tags (
     way_id INTEGER,               -- way ID
     key    TEXT,                  -- tag key
     value  TEXT                   -- tag value
    )

    CREATE TABLE way_nodes (
     way_id      INTEGER,          -- way ID
     local_order INTEGER,          -- nodes sorting
     node_id     INTEGER           -- node ID


## Created indexes in the SQLite database

    CREATE INDEX node_tags__node_id ON node_tags (node_id)
    CREATE INDEX node_tags__key     ON node_tags (key)
    CREATE INDEX way_tags__way_id   ON way_tags (way_id)
    CREATE INDEX way_tags__key      ON way_tags (key)
    CREATE INDEX way_nodes__way_id  ON way_nodes (way_id)
    CREATE INDEX way_nodes__node_id ON way_nodes (node_id)
