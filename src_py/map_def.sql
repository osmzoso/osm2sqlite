/*
**
*/
DROP TABLE IF EXISTS map_def;
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE map_def (
  zoomlevel INTEGER,
  key       TEXT,
  value     TEXT,
  layer     INTEGER,
  style     TEXT,      -- 'area', 'line', 'point'
  width     INTEGER,
  fill      TEXT,
  stroke    TEXT,
  dash      TEXT
);
/*
** Zoomlevel 16
*/
INSERT INTO map_def VALUES (16,'landuse','farmland',         1,'area',0,'#eef0d5','none','');
INSERT INTO map_def VALUES (16,'landuse','commercial',       1,'area',1,'#f2dad9','#ddc4c2','');
INSERT INTO map_def VALUES (16,'landuse','residential',      1,'area',0,'#e0dfdf','none','');
INSERT INTO map_def VALUES (16,'landuse','industrial',       1,'area',0,'#ebdbe8','none','');
INSERT INTO map_def VALUES (16,'landuse','grass',            2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (16,'landuse','meadow',           2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (16,'landuse','village_green',    2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (16,'natural','grassland',        2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (16,'landuse','forest',           2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (16,'natural','wood',             2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (16,'landuse','vineyard',         2,'area',0,'#bddc9a','none','');
INSERT INTO map_def VALUES (16,'landuse','farmyard',         2,'area',0,'#f5dcba','none','');
INSERT INTO map_def VALUES (16,'landuse','orchard',          2,'area',0,'#aedfa3','none','');
INSERT INTO map_def VALUES (16,'landuse','allotments',       2,'area',0,'#d5e4cb','none','');
INSERT INTO map_def VALUES (16,'leisure','park',             2,'area',0,'#c8facc','none','');
INSERT INTO map_def VALUES (16,'landuse','cemetery',         2,'area',0,'#aacbaf','none','');
INSERT INTO map_def VALUES (16,'landuse','recreation_ground',2,'area',1,'#dffce2','9dd5a1','');
INSERT INTO map_def VALUES (16,'landuse','construction',     2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (16,'landuse','brownfield',       2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (16,'leisure','playground',       3,'area',1,'#dffce2','#a1dea6','');
INSERT INTO map_def VALUES (16,'leisure','pitch',            3,'area',1,'#aae0cb','#8ecfb5','');
INSERT INTO map_def VALUES (16,'leisure','swimming_pool',    3,'area',1,'#aad3df','#7dc7dc','');
INSERT INTO map_def VALUES (16,'natural','water',            4,'area',0,'#aad3df','none','');
INSERT INTO map_def VALUES (16,'waterway','stream',          4,'line',2,'none','#aad3df','');
INSERT INTO map_def VALUES (16,'barrier','%',                4,'line',1,'none','#9fb0a1','');
INSERT INTO map_def VALUES (16,'building','%',               4,'area',1,'#d9d0c9','#bcb2a6','');

INSERT INTO map_def VALUES (16,'highway','motorway',      5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (16,'highway','motorway',      7,'line',10,'none','#e892a2','');

INSERT INTO map_def VALUES (16,'highway','motorway_link',      5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (16,'highway','motorway_link',      7,'line',10,'none','#e892a2','');

INSERT INTO map_def VALUES (16,'highway','primary',       5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (16,'highway','primary',       7,'line',10,'none','#fcd6a4','');

INSERT INTO map_def VALUES (16,'highway','primary_link',  5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (16,'highway','primary_link',  7,'line',10,'none','#fcd6a4','');

INSERT INTO map_def VALUES (16,'highway','secondary',     5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','secondary',     8,'line', 9,'none','#f7fabf','');

INSERT INTO map_def VALUES (16,'highway','secondary_link',5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','secondary_link',8,'line', 9,'none','#f7fabf','');

INSERT INTO map_def VALUES (16,'highway','tertiary',      5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','tertiary',      8,'line',7,'none','#ffffff','');

INSERT INTO map_def VALUES (16,'highway','tertiary_link', 5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','tertiary_link', 8,'line',7,'none','#ffffff','');

INSERT INTO map_def VALUES (16,'highway','trunk',         5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','trunk',         7,'line',7,'none','#f9b29c','');

INSERT INTO map_def VALUES (16,'highway','trunk_link',    5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','trunk_link',    7,'line',7,'none','#f9b29c','');

INSERT INTO map_def VALUES (16,'highway','residential',      5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','residential',      8,'line', 4,'none','#ffffff','');

INSERT INTO map_def VALUES (16,'highway','unclassified',      5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','unclassified',      8,'line', 4,'none','#ffffff','');

--INSERT INTO map_def VALUES (16,'highway','service',          5,'line', 2,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','service',          8,'line', 2,'none','#ffffff','');

INSERT INTO map_def VALUES (16,'highway','living_street',    5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (16,'highway','living_street',    6,'line', 3,'none','#ededed','');

INSERT INTO map_def VALUES (16,'highway','pedestrian',       5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (16,'highway','pedestrian',       6,'line', 3,'none','#ededed','');

INSERT INTO map_def VALUES (16,'highway','track',            5,'line', 1,'none','#a5832c','9,3');

INSERT INTO map_def VALUES (16,'highway','footway',          5,'line', 1,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (16,'highway','path',             5,'line', 1,'none','#fa8274','3,3');

INSERT INTO map_def VALUES (16,'highway','cycleway',         5,'line', 1,'none','#0e0efe','3,3');

INSERT INTO map_def VALUES (16,'highway','steps',            5,'line', 3,'none','#fa8274','3,3');

INSERT INTO map_def VALUES (16,'railway','rail',             5,'line', 4,'none','#444444','');
INSERT INTO map_def VALUES (16,'railway','rail',             8,'line', 2,'none','#eeeeee','8,8');

INSERT INTO map_def VALUES (16,'power','line',               9,'line', 1,'none','#aaaaaa','');

/*
** Zoomlevel 17
*/
INSERT INTO map_def VALUES (17,'highway','service',          5,'line', 4,'none','#888888','');
INSERT INTO map_def VALUES (17,'highway','service',          8,'line', 2,'none','#ffffff','');

/*
            # Layer 1
            # Layer 2
            # Layer 3
            # Layer 4
            #
            elif key == 'railway' and value == 'tram':
                way1 = {'layer': 8, 'style': 'line', 'width': 4, 'fill': '#6e6e6e', 'outline': '', 'dash': ''}
            elif key == 'amenity':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#eeeeee', 'outline': '#d8c3c2', 'dash': ''}
            elif key == 'landuse' and value == 'railway':
                way1 = {'layer': 1, 'style': 'polygon', 'width': 0, 'fill': '#e9dae7', 'outline': '#aaa5a8', 'dash': ''}
            elif key == 'natural' and value == 'scrub':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#c8d7ab', 'outline': '', 'dash': ''}
            elif key == 'natural' and value == 'tree_row':
                way1 = {'layer': 2, 'style': 'line', 'width': 4, 'fill': '#9cd79f', 'outline': '', 'dash': ''}    # opacity 0.5
            elif key == 'highway' and value == 'platform':
                way1 = {'layer': 3, 'style': 'polygon', 'width': 0, 'fill': '#bbbbbb', 'outline': '#929191', 'dash': ''}
*/

CREATE INDEX map_def__key_value ON map_def (key, value);
COMMIT;