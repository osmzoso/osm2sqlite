--
-- Creates tables with addresses and coordinates
--
BEGIN TRANSACTION;
--
-- 1. Determine address data from way tags
--
CREATE TEMP TABLE osm_addr_way (
 way_id      INTEGER PRIMARY KEY,
 postcode    TEXT,
 city        TEXT,
 street      TEXT,
 housenumber TEXT
);
INSERT INTO osm_addr_way
 SELECT way_id,value AS postcode,'','',''
 FROM way_tags WHERE key='addr:postcode'
 ON CONFLICT(way_id) DO UPDATE SET postcode=excluded.postcode;
INSERT INTO osm_addr_way
 SELECT way_id,'',value AS city,'',''
 FROM way_tags WHERE key='addr:city'
 ON CONFLICT(way_id) DO UPDATE SET city=excluded.city;
INSERT INTO osm_addr_way
 SELECT way_id,'','',value AS street,''
 FROM way_tags WHERE key='addr:street'
 ON CONFLICT(way_id) DO UPDATE SET street=excluded.street;
INSERT INTO osm_addr_way
 SELECT way_id,'','','',value AS housenumber
 FROM way_tags WHERE key='addr:housenumber'
 ON CONFLICT(way_id) DO UPDATE SET housenumber=excluded.housenumber;
--
-- 2. Calculate coordinates of address data from way tags
--
CREATE TEMP TABLE osm_addr_way_coordinates AS
SELECT way.way_id AS way_id,round(avg(n.lon),7) AS lon,round(avg(n.lat),7) AS lat
FROM osm_addr_way AS way
LEFT JOIN way_nodes AS wn ON way.way_id=wn.way_id
LEFT JOIN nodes     AS n  ON wn.node_id=n.node_id
GROUP BY way.way_id;
CREATE INDEX osm_addr_way_coordinates_way_id ON osm_addr_way_coordinates (way_id);
--
-- 3. Determine address data from node tags
--
CREATE TEMP TABLE osm_addr_node (
 node_id     INTEGER PRIMARY KEY,
 postcode    TEXT,
 city        TEXT,
 street      TEXT,
 housenumber TEXT
);
INSERT INTO osm_addr_node
 SELECT node_id,value AS postcode,'','',''
 FROM node_tags WHERE key='addr:postcode'
 ON CONFLICT(node_id) DO UPDATE SET postcode=excluded.postcode;
INSERT INTO osm_addr_node
 SELECT node_id,'',value AS city,'',''
 FROM node_tags WHERE key='addr:city'
 ON CONFLICT(node_id) DO UPDATE SET city=excluded.city;
INSERT INTO osm_addr_node
 SELECT node_id,'','',value AS street,''
 FROM node_tags WHERE key='addr:street'
 ON CONFLICT(node_id) DO UPDATE SET street=excluded.street;
INSERT INTO osm_addr_node
 SELECT node_id,'','','',value AS housenumber
 FROM node_tags WHERE key='addr:housenumber'
 ON CONFLICT(node_id) DO UPDATE SET housenumber=excluded.housenumber;
--
-- 4. Create temporary overall table with all addresses
--
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
ORDER BY postcode,city,street,housenumber;
--
-- 5. Create tables "addr_street" and "addr_housenumber" (normalize tables)
--
DROP TABLE IF EXISTS addr_street;
CREATE TABLE addr_street (
 street_id   INTEGER PRIMARY KEY,
 postcode    TEXT,
 city        TEXT,
 street      TEXT,
 min_lon     REAL,
 min_lat     REAL,
 max_lon     REAL,
 max_lat     REAL
);
INSERT INTO addr_street (postcode,city,street,min_lon,min_lat,max_lon,max_lat)
 SELECT postcode,city,street,min(lon),min(lat),max(lon),max(lat)
 FROM osm_addr
 GROUP BY postcode,city,street;
CREATE INDEX addr_street_1 ON addr_street (postcode,city,street);
DROP TABLE IF EXISTS addr_housenumber;
CREATE TABLE addr_housenumber (
 housenumber_id INTEGER PRIMARY KEY,
 street_id      INTEGER,
 housenumber    TEXT,
 lon            REAL,
 lat            REAL,
 way_id         INTEGER,
 node_id        INTEGER
);
INSERT INTO addr_housenumber (street_id,housenumber,lon,lat,way_id,node_id)
 SELECT s.street_id,a.housenumber,a.lon,a.lat,a.way_id,a.node_id
 FROM osm_addr AS a
 LEFT JOIN addr_street AS s ON a.postcode=s.postcode AND a.city=s.city AND a.street=s.street;
CREATE INDEX addr_housenumber_1 ON addr_housenumber (street_id);
--
-- 6. Create view
--
DROP VIEW IF EXISTS addr_view;
CREATE VIEW addr_view AS
SELECT s.street_id,s.postcode,s.city,s.street,h.housenumber,h.lon,h.lat,h.way_id,h.node_id
FROM addr_street AS s
LEFT JOIN addr_housenumber AS h ON s.street_id=h.street_id;
--
-- 7. Finish, clean up temporary tables
--
COMMIT TRANSACTION;
DROP TABLE osm_addr_way;
DROP TABLE osm_addr_way_coordinates;
DROP TABLE osm_addr_node;
DROP TABLE osm_addr;

