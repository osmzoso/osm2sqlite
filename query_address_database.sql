--
-- Creates from the database "osm.sqlite3" a new database "osm_addr.sqlite3"
-- with all addresses and coordinates
--
-- Usage:
-- sqlite3 < query_address_database.sql
--

--
-- Time measurement
--
SELECT 'start : '||datetime('now','localtime');

-- Connection to the database with the OpenStreetMap data
ATTACH DATABASE "./osm.sqlite3" AS osm;

-- Connection to the new address database 
.print "creating new database 'osm_addr.sqlite3'..."
-- Delete any existing database as a precaution
.shell del osm_addr.sqlite3
ATTACH DATABASE "./osm_addr.sqlite3" AS db;

--
-- 1. Determine address data from way tags
--
.print "creating temporary table 'osm_addr_way'..."
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
.print "creating temporary table 'osm_addr_way_coordinates'..."
CREATE TEMP TABLE osm_addr_way_coordinates AS
SELECT way.way_id AS way_id,round(avg(n.lat),7) AS lat,round(avg(n.lon),7) AS lon
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
.print "creating temporary table 'osm_addr_node'..."
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
.print "creating temporary table 'osm_addr'..."
CREATE TEMP TABLE osm_addr (
 addr_id     INTEGER PRIMARY KEY,
 way_id      INTEGER,
 node_id     INTEGER,
 postcode    TEXT,
 city        TEXT,
 street      TEXT,
 housenumber TEXT,
 lat         REAL,
 lon         REAL
);

INSERT INTO osm_addr (way_id,node_id,postcode,city,street,housenumber,lat,lon)

SELECT w.way_id,-1 AS node_id,w.postcode,w.city,w.street,w.housenumber,c.lat,c.lon
FROM osm_addr_way AS w
LEFT JOIN osm_addr_way_coordinates AS c ON w.way_id=c.way_id

UNION ALL

SELECT -1 AS way_id,n.node_id,n.postcode,n.city,n.street,n.housenumber,c.lat,c.lon
FROM osm_addr_node AS n
LEFT JOIN nodes AS c ON n.node_id=c.node_id

ORDER BY postcode,city,street,housenumber
;

--
-- 5. Create tables "osm_street" and "osm_housenumber" (normalise data)
--
.print "creating table 'osm_street'..."
DROP TABLE IF EXISTS db.osm_street;
CREATE TABLE db.osm_street (
 street_id   INTEGER PRIMARY KEY,
 postcode    TEXT,
 city        TEXT,
 street      TEXT
);
INSERT INTO db.osm_street (postcode,city,street)
SELECT DISTINCT postcode,city,street FROM osm_addr
;
.print "creating index 'osm_street_1'..."
CREATE INDEX db.osm_street_1 ON osm_street (postcode,city,street);

.print "creating table 'osm_housenumber'..."
DROP TABLE IF EXISTS db.osm_housenumber;
CREATE TABLE db.osm_housenumber (
 housenumber_id INTEGER PRIMARY KEY,
 street_id      INTEGER,
 housenumber    TEXT,
 lat            REAL,
 lon            REAL,
 way_id         INTEGER,
 node_id        INTEGER
);
INSERT INTO db.osm_housenumber (street_id,housenumber,lat,lon,way_id,node_id)
SELECT s.street_id,a.housenumber,a.lat,a.lon,a.way_id,a.node_id
FROM osm_addr AS a
LEFT JOIN osm_street AS s ON a.postcode=s.postcode AND a.city=s.city AND a.street=s.street
;
.print "creating index 'osm_housenumber_1'..."
CREATE INDEX db.osm_housenumber_1 ON osm_housenumber (street_id);

--
-- 6. Create overall view
--
.print "creating overall view 'view_osm_addr'..."
CREATE VIEW db.view_osm_addr AS
SELECT s.postcode,s.city,s.street,h.housenumber,h.lon,h.lat,h.way_id,h.node_id
FROM osm_street AS s
LEFT JOIN osm_housenumber AS h ON s.street_id=h.street_id
;

/*
--
-- 7. Create R*Tree index
--
.print "creating R*Tree index 'location'..."
DROP TABLE IF EXISTS db.location;
CREATE VIRTUAL TABLE db.location USING rtree (housenumber_id,lon,lat);
INSERT INTO db.location (housenumber_id,lon,lat)
SELECT housenumber_id,lon,lat FROM osm_housenumber;
*/

--
-- Time measurement
--
SELECT 'finish : '||datetime('now','localtime');
