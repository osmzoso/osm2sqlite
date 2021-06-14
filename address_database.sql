--
-- Creates a database "osm_addr.sqlite3" with addresses and coordinates
--
-- Requires an existing database "osm.sqlite3"
--
-- Usage:
-- sqlite3 < query_address_database.sql
--

-- Delete an existing database as a precaution
.shell del osm_addr.sqlite3

--
-- Time measurement
--
SELECT 'start : '||datetime('now','localtime');

-- Connection to the existing database with the OpenStreetMap data
ATTACH DATABASE "./osm.sqlite3" AS osm;

-- Connection to the new address database 
.print "creating new database 'osm_addr.sqlite3'..."
ATTACH DATABASE "./osm_addr.sqlite3" AS db;

--
-- 1. Determine address data from way tags
--
.print "   (creating temp. table 'osm_addr_way'...)"
CREATE TEMP TABLE osm_addr_way AS
WITH way_id AS
(
 SELECT DISTINCT way_id
 FROM osm.way_tags
 WHERE key IN ('addr:postcode','addr:city','addr:street','addr:housenumber')
)
SELECT way_id.way_id AS way_id,
 ifnull(postcode.value,'')      AS postcode,
 ifnull(city.value,'')          AS city,
 ifnull(street.value,'')        AS street,
 ifnull(housenumber.value,'')   AS housenumber
FROM way_id
LEFT JOIN osm.way_tags AS postcode    ON way_id.way_id=postcode.way_id    AND postcode.key   ='addr:postcode'
LEFT JOIN osm.way_tags AS city        ON way_id.way_id=city.way_id        AND city.key       ='addr:city'
LEFT JOIN osm.way_tags AS street      ON way_id.way_id=street.way_id      AND street.key     ='addr:street'
LEFT JOIN osm.way_tags AS housenumber ON way_id.way_id=housenumber.way_id AND housenumber.key='addr:housenumber'
;

--
-- 2. Calculate coordinates of address data from way tags
--
.print "   (creating temp. table 'osm_addr_way_coordinates'...)"
CREATE TEMP TABLE osm_addr_way_coordinates AS
SELECT way.way_id AS way_id,round(avg(n.lon),7) AS lon,round(avg(n.lat),7) AS lat
FROM osm_addr_way AS way
LEFT JOIN way_nodes AS wn ON way.way_id=wn.way_id
LEFT JOIN nodes     AS n  ON wn.node_id=n.node_id
GROUP BY way.way_id
;
CREATE INDEX osm_addr_way_coordinates_way_id ON osm_addr_way_coordinates (way_id)
;

--
-- 3. Determine address data from node tags
--
.print "   (creating temp. table 'osm_addr_node'...)"
CREATE TEMP TABLE osm_addr_node AS
WITH node_id AS
(
 SELECT DISTINCT node_id
 FROM osm.node_tags
 WHERE key IN ('addr:postcode','addr:city','addr:street','addr:housenumber')
)
SELECT node_id.node_id AS node_id,
 ifnull(postcode.value,'')        AS postcode,
 ifnull(city.value,'')            AS city,
 ifnull(street.value,'')          AS street,
 ifnull(housenumber.value,'')     AS housenumber
FROM node_id
LEFT JOIN osm.node_tags AS postcode    ON node_id.node_id=postcode.node_id    AND postcode.key   ='addr:postcode'
LEFT JOIN osm.node_tags AS city        ON node_id.node_id=city.node_id        AND city.key       ='addr:city'
LEFT JOIN osm.node_tags AS street      ON node_id.node_id=street.node_id      AND street.key     ='addr:street'
LEFT JOIN osm.node_tags AS housenumber ON node_id.node_id=housenumber.node_id AND housenumber.key='addr:housenumber'
;

--
-- 4. Create temporary overall table with all addresses
--
.print "   (creating temp. table 'osm_addr'...)"
CREATE TEMP TABLE osm_addr (
 addr_id     INTEGER PRIMARY KEY,
 way_id      INTEGER,
 node_id     INTEGER,
 postcode    TEXT,
 city        TEXT,
 street      TEXT,
 housenumber TEXT,
 lon         REAL,
 lat         REAL
);

INSERT INTO osm_addr (way_id,node_id,postcode,city,street,housenumber,lon,lat)

SELECT w.way_id,-1 AS node_id,w.postcode,w.city,w.street,w.housenumber,c.lon,c.lat
FROM osm_addr_way AS w
LEFT JOIN osm_addr_way_coordinates AS c ON w.way_id=c.way_id

UNION ALL

SELECT -1 AS way_id,n.node_id,n.postcode,n.city,n.street,n.housenumber,c.lon,c.lat
FROM osm_addr_node AS n
LEFT JOIN nodes AS c ON n.node_id=c.node_id

ORDER BY postcode,city,street,housenumber
;

--
-- 5. Create tables "addr_street" and "addr_housenumber" (normalize tables)
--
.print "creating table 'addr_street'..."
DROP TABLE IF EXISTS db.addr_street;
CREATE TABLE db.addr_street (
 street_id   INTEGER PRIMARY KEY,
 postcode    TEXT,
 city        TEXT,
 street      TEXT,
 min_lon     REAL,  -- Boundingbox slightly larger than in real life (0.002 degress)
 min_lat     REAL,
 max_lon     REAL,
 max_lat     REAL
);
INSERT INTO db.addr_street (postcode,city,street,min_lon,min_lat,max_lon,max_lat)
SELECT postcode,city,street,min(lon)-0.002,min(lat)-0.002,max(lon)+0.002,max(lat)+0.002
FROM osm_addr
GROUP BY postcode,city,street
;
-- index
CREATE INDEX db.addr_street_1 ON addr_street (postcode,city,street);

.print "creating table 'addr_housenumber'..."
DROP TABLE IF EXISTS db.addr_housenumber;
CREATE TABLE db.addr_housenumber (
 housenumber_id INTEGER PRIMARY KEY,
 street_id      INTEGER,
 housenumber    TEXT,
 lon            REAL,
 lat            REAL,
 way_id         INTEGER,
 node_id        INTEGER
);
INSERT INTO db.addr_housenumber (street_id,housenumber,lon,lat,way_id,node_id)
SELECT s.street_id,a.housenumber,a.lon,a.lat,a.way_id,a.node_id
FROM osm_addr AS a
LEFT JOIN addr_street AS s ON a.postcode=s.postcode AND a.city=s.city AND a.street=s.street
;
-- index
CREATE INDEX db.addr_housenumber_1 ON addr_housenumber (street_id);

--
-- 6. Create view
--
.print "creating view 'view_addr'..."
CREATE VIEW db.view_addr AS
SELECT s.street_id,s.postcode,s.city,s.street,h.housenumber,h.lon,h.lat,h.way_id,h.node_id
FROM addr_street AS s
LEFT JOIN addr_housenumber AS h ON s.street_id=h.street_id
;

--
-- 7. Finish, clean up temporary tables
--
DROP TABLE osm_addr_way;
DROP TABLE osm_addr_way_coordinates;
DROP TABLE osm_addr_node;
DROP TABLE osm_addr;

--
-- To check the street name in the address it is useful to
-- check if there is also a way with the same name nearby
--

--
-- 8. Determine the name of all ways with key='highway'
--
.print "   (creating temp. table 'highway_name'...)"
CREATE TEMP TABLE highway_name AS
WITH highway_way_id AS
(
 SELECT DISTINCT way_id
 FROM osm.way_tags
 WHERE key='highway'
)
SELECT
 highway_way_id.way_id    AS way_id,
 ifnull(highway.value,'') AS highway,
 ifnull(name.value,'')    AS name
FROM highway_way_id
LEFT JOIN way_tags AS highway ON highway_way_id.way_id=highway.way_id AND highway.key ='highway'
LEFT JOIN way_tags AS name    ON highway_way_id.way_id=name.way_id    AND name.key    ='name'
;

--
-- 9. Determine the boundingbox of the highway
--
.print "   (creating temp. table 'highway_name_bbox'...)"
CREATE TEMP TABLE highway_name_bbox AS
SELECT
 highway_name.way_id AS way_id,
 highway_name.name   AS name,
 min(nodes.lon)      AS min_lon,
 min(nodes.lat)      AS min_lat,
 max(nodes.lon)      AS max_lon,
 max(nodes.lat)      AS max_lat
FROM highway_name
LEFT JOIN way_nodes ON highway_name.way_id=way_nodes.way_id
LEFT JOIN nodes     ON way_nodes.node_id=nodes.node_id
WHERE highway_name.name!=''
GROUP BY highway_name.way_id
;
-- R*Tree index boundingbox
-- (uses auxiliary columns, available since SQLite version 3.24.0)
CREATE VIRTUAL TABLE highway USING rtree(
 way_id,
 min_lon, max_lon,
 min_lat, max_lat,
 +name TEXT
);
INSERT INTO highway (way_id, min_lon, max_lon, min_lat, max_lat, name)
SELECT               way_id, min_lon, max_lon, min_lat, max_lat, name
FROM highway_name_bbox
;

--
-- 10. Create table "addr_street_highway"
--
.print "creating table 'addr_street_highway'..."
DROP TABLE IF EXISTS db.addr_street_highway;
CREATE TABLE db.addr_street_highway (
 street_id INTEGER,
 way_id    INTEGER
);
INSERT INTO db.addr_street_highway (street_id,way_id)
SELECT s.street_id,h.way_id
FROM db.addr_street AS s
LEFT JOIN highway AS h ON
 -- only highways that overlap the boundingbox of the street
 h.max_lon>=s.min_lon AND h.min_lon<=s.max_lon AND
 h.max_lat>=s.min_lat AND h.min_lat<=s.max_lat
 -- streetname = highway name
 AND s.street=h.name
-- only streets with postcode info
WHERE s.postcode!=''
;
-- index
CREATE INDEX db.addr_street_highway_1 ON addr_street_highway (street_id);

--
-- Time measurement
--
SELECT 'finish : '||datetime('now','localtime');
