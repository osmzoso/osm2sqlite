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
** Zoomlevel 13 (experimental)
*/
INSERT INTO map_def VALUES (13,'landuse','forest',           2,'area',0,'#add19e','none','');

INSERT INTO map_def VALUES (13,'highway','motorway',      5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (13,'highway','motorway',      7,'line',10,'none','#e892a2','');

INSERT INTO map_def VALUES (13,'highway','primary',       5,'line',8,'none','#a26e04','');
INSERT INTO map_def VALUES (13,'highway','primary',       7,'line',6,'none','#fcd6a4','');

INSERT INTO map_def VALUES (13,'highway','trunk',         5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (13,'highway','trunk',         7,'line',7,'none','#f9b29c','');

INSERT INTO map_def VALUES (13,'railway','rail',             5,'line', 4,'none','#777777','');
INSERT INTO map_def VALUES (13,'railway','rail',             8,'line', 2,'none','#eeeeee','8,8');


/*
** Zoomlevel 16
*/
INSERT INTO map_def VALUES (16,'landuse','farmland',          1,'area',0,'#eef0d5','none','');
INSERT INTO map_def VALUES (16,'landuse','commercial',        1,'area',1,'#f2dad9','#ddc4c2','');
INSERT INTO map_def VALUES (16,'landuse','residential',       1,'area',0,'#e0dfdf','none','');
INSERT INTO map_def VALUES (16,'landuse','industrial',        1,'area',0,'#ebdbe8','none','');
INSERT INTO map_def VALUES (16,'landuse','railway',           1,'area',0,'#e9dae7','none','');
INSERT INTO map_def VALUES (16,'landuse','grass',             2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (16,'landuse','meadow',            2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (16,'landuse','village_green',     2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (16,'natural','grassland',         2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (16,'natural','scrub',             2,'area',0,'#c8d7ab','none','');
INSERT INTO map_def VALUES (16,'landuse','forest',            2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (16,'natural','wood',              2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (16,'landuse','vineyard',          2,'area',0,'#bddc9a','none','');
INSERT INTO map_def VALUES (16,'landuse','farmyard',          2,'area',0,'#f5dcba','none','');
INSERT INTO map_def VALUES (16,'landuse','orchard',           2,'area',0,'#aedfa3','none','');
INSERT INTO map_def VALUES (16,'landuse','allotments',        2,'area',0,'#d5e4cb','none','');
INSERT INTO map_def VALUES (16,'leisure','park',              2,'area',0,'#c8facc','none','');
INSERT INTO map_def VALUES (16,'landuse','cemetery',          2,'area',0,'#aacbaf','none','');
INSERT INTO map_def VALUES (16,'landuse','recreation_ground', 2,'area',1,'#dffce2','#9dd5a1','');
INSERT INTO map_def VALUES (16,'amenity','%',                 2,'area',0,'#eeeeee','none','');
INSERT INTO map_def VALUES (16,'landuse','construction',      2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (16,'landuse','brownfield',        2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (16,'leisure','playground',        3,'area',1,'#dffce2','#a1dea6','');
INSERT INTO map_def VALUES (16,'tourism','camp_site',         3,'area',0,'#def6c0','none','');
INSERT INTO map_def VALUES (16,'leisure','pitch',             3,'area',1,'#aae0cb','#8ecfb5','');
INSERT INTO map_def VALUES (16,'leisure','swimming_pool',     3,'area',1,'#aad3df','#7dc7dc','');
INSERT INTO map_def VALUES (16,'highway','platform',          3,'area',1,'#bbbbbb','#929191','');
INSERT INTO map_def VALUES (16,'natural','tree_row',          3,'line',4,'none','#a9d291','');
INSERT INTO map_def VALUES (16,'natural','water',             4,'area',0,'#aad3df','none','');
INSERT INTO map_def VALUES (16,'waterway','stream',           4,'line',2,'none','#aad3df','');
INSERT INTO map_def VALUES (16,'barrier','%',                 4,'line',1,'none','#9fb0a1','');
INSERT INTO map_def VALUES (16,'building','%',                4,'area',1,'#d9d0c9','#bcb2a6','');
INSERT INTO map_def VALUES (16,'man_made','pier',             5,'line',2,'none','#f2efe9','');
INSERT INTO map_def VALUES (16,'border_type','nation',        5,'line',5,'none','#a6a9c0','');
INSERT INTO map_def VALUES (16,'border_type','nation',        6,'line',1,'none','#91769c','30 5 10 5');
INSERT INTO map_def VALUES (16,'highway','motorway',          5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (16,'highway','motorway',          7,'line',10,'none','#e892a2','');
INSERT INTO map_def VALUES (16,'highway','motorway_link',     5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (16,'highway','motorway_link',     7,'line',10,'none','#e892a2','');
INSERT INTO map_def VALUES (16,'highway','primary',           5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (16,'highway','primary',           7,'line',10,'none','#fcd6a4','');
INSERT INTO map_def VALUES (16,'highway','primary_link',      5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (16,'highway','primary_link',      7,'line',10,'none','#fcd6a4','');
INSERT INTO map_def VALUES (16,'highway','secondary',         5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','secondary',         8,'line', 9,'none','#f7fabf','');
INSERT INTO map_def VALUES (16,'highway','secondary_link',    5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','secondary_link',    8,'line', 9,'none','#f7fabf','');
INSERT INTO map_def VALUES (16,'highway','tertiary',          5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','tertiary',          8,'line',7,'none','#ffffff','');
INSERT INTO map_def VALUES (16,'highway','tertiary_link',     5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','tertiary_link',     8,'line',7,'none','#ffffff','');
INSERT INTO map_def VALUES (16,'highway','trunk',             5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','trunk',             7,'line',7,'none','#f9b29c','');
INSERT INTO map_def VALUES (16,'highway','trunk_link',        5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','trunk_link',        7,'line',7,'none','#f9b29c','');
INSERT INTO map_def VALUES (16,'highway','residential',       5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','residential',       8,'line', 4,'none','#ffffff','');
INSERT INTO map_def VALUES (16,'highway','unclassified',      5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (16,'highway','unclassified',      8,'line', 4,'none','#ffffff','');
INSERT INTO map_def VALUES (16,'highway','service',           8,'line', 2,'none','#ffffff','');
INSERT INTO map_def VALUES (16,'highway','living_street',     5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (16,'highway','living_street',     6,'line', 3,'none','#ededed','');
INSERT INTO map_def VALUES (16,'highway','pedestrian',        5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (16,'highway','pedestrian',        6,'line', 3,'none','#ededed','');
INSERT INTO map_def VALUES (16,'highway','track',             5,'line', 1,'none','#a5832c','9,3');
INSERT INTO map_def VALUES (16,'highway','footway',           5,'line', 1,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (16,'highway','path',              5,'line', 1,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (16,'highway','cycleway',          5,'line', 1,'none','#0e0efe','3,3');
INSERT INTO map_def VALUES (16,'highway','steps',             5,'line', 3,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (16,'railway','rail',              5,'line', 4,'none','#777777','');
INSERT INTO map_def VALUES (16,'railway','rail',              8,'line', 2,'none','#eeeeee','8,8');
INSERT INTO map_def VALUES (16,'railway','tram',              8,'line', 2,'none','#6e6e6e','');
INSERT INTO map_def VALUES (16,'power','line',                9,'line', 1,'none','#aaaaaa','');
INSERT INTO map_def VALUES (16,'name','%',                   12,'text', 8,'#303030','','');
/*
** Zoomlevel 17
*/
INSERT INTO map_def VALUES (17,'landuse','farmland',          1,'area',0,'#eef0d5','none','');
INSERT INTO map_def VALUES (17,'landuse','commercial',        1,'area',1,'#f2dad9','#ddc4c2','');
INSERT INTO map_def VALUES (17,'landuse','residential',       1,'area',0,'#e0dfdf','none','');
INSERT INTO map_def VALUES (17,'landuse','industrial',        1,'area',0,'#ebdbe8','none','');
INSERT INTO map_def VALUES (17,'landuse','railway',           1,'area',0,'#e9dae7','none','');
INSERT INTO map_def VALUES (17,'landuse','grass',             2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (17,'landuse','meadow',            2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (17,'landuse','village_green',     2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (17,'natural','grassland',         2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (17,'natural','scrub',             2,'area',0,'#c8d7ab','none','');
INSERT INTO map_def VALUES (17,'landuse','forest',            2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (17,'natural','wood',              2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (17,'landuse','vineyard',          2,'area',0,'#bddc9a','none','');
INSERT INTO map_def VALUES (17,'landuse','farmyard',          2,'area',0,'#f5dcba','none','');
INSERT INTO map_def VALUES (17,'landuse','orchard',           2,'area',0,'#aedfa3','none','');
INSERT INTO map_def VALUES (17,'landuse','allotments',        2,'area',0,'#d5e4cb','none','');
INSERT INTO map_def VALUES (17,'leisure','park',              2,'area',0,'#c8facc','none','');
INSERT INTO map_def VALUES (17,'landuse','cemetery',          2,'area',0,'#aacbaf','none','');
INSERT INTO map_def VALUES (17,'landuse','recreation_ground', 2,'area',1,'#dffce2','#9dd5a1','');
INSERT INTO map_def VALUES (17,'amenity','%',                 2,'area',0,'#eeeeee','none','');
INSERT INTO map_def VALUES (17,'landuse','construction',      2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (17,'landuse','brownfield',        2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (17,'leisure','playground',        3,'area',1,'#dffce2','#a1dea6','');
INSERT INTO map_def VALUES (17,'tourism','camp_site',         3,'area',0,'#def6c0','none','');
INSERT INTO map_def VALUES (17,'leisure','pitch',             3,'area',1,'#aae0cb','#8ecfb5','');
INSERT INTO map_def VALUES (17,'leisure','swimming_pool',     3,'area',1,'#aad3df','#7dc7dc','');
INSERT INTO map_def VALUES (17,'highway','platform',          3,'area',1,'#bbbbbb','#929191','');
INSERT INTO map_def VALUES (17,'natural','tree_row',          3,'line',4,'none','#a9d291','');
INSERT INTO map_def VALUES (17,'natural','water',             4,'area',0,'#aad3df','none','');
INSERT INTO map_def VALUES (17,'waterway','stream',           4,'line',2,'none','#aad3df','');
INSERT INTO map_def VALUES (17,'barrier','%',                 4,'line',1,'none','#9fb0a1','');
INSERT INTO map_def VALUES (17,'building','%',                4,'area',1,'#d9d0c9','#bcb2a6','');
INSERT INTO map_def VALUES (17,'man_made','pier',             5,'line',2,'none','#f2efe9','');
INSERT INTO map_def VALUES (17,'border_type','nation',        5,'line',5,'none','#a6a9c0','');
INSERT INTO map_def VALUES (17,'border_type','nation',        6,'line',1,'none','#91769c','30 5 10 5');
INSERT INTO map_def VALUES (17,'highway','motorway',          5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (17,'highway','motorway',          7,'line',10,'none','#e892a2','');
INSERT INTO map_def VALUES (17,'highway','motorway_link',     5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (17,'highway','motorway_link',     7,'line',10,'none','#e892a2','');
INSERT INTO map_def VALUES (17,'highway','primary',           5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (17,'highway','primary',           7,'line',10,'none','#fcd6a4','');
INSERT INTO map_def VALUES (17,'highway','primary_link',      5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (17,'highway','primary_link',      7,'line',10,'none','#fcd6a4','');
INSERT INTO map_def VALUES (17,'highway','secondary',         5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (17,'highway','secondary',         8,'line', 9,'none','#f7fabf','');
INSERT INTO map_def VALUES (17,'highway','secondary_link',    5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (17,'highway','secondary_link',    8,'line', 9,'none','#f7fabf','');
INSERT INTO map_def VALUES (17,'highway','tertiary',          5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (17,'highway','tertiary',          8,'line',7,'none','#ffffff','');
INSERT INTO map_def VALUES (17,'highway','tertiary_link',     5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (17,'highway','tertiary_link',     8,'line',7,'none','#ffffff','');
INSERT INTO map_def VALUES (17,'highway','trunk',             5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (17,'highway','trunk',             7,'line',7,'none','#f9b29c','');
INSERT INTO map_def VALUES (17,'highway','trunk_link',        5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (17,'highway','trunk_link',        7,'line',7,'none','#f9b29c','');
INSERT INTO map_def VALUES (17,'highway','residential',       5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (17,'highway','residential',       8,'line', 4,'none','#ffffff','');
INSERT INTO map_def VALUES (17,'highway','unclassified',      5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (17,'highway','unclassified',      8,'line', 4,'none','#ffffff','');
INSERT INTO map_def VALUES (17,'highway','service',           8,'line', 2,'none','#ffffff','');
INSERT INTO map_def VALUES (17,'highway','living_street',     5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (17,'highway','living_street',     6,'line', 3,'none','#ededed','');
INSERT INTO map_def VALUES (17,'highway','pedestrian',        5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (17,'highway','pedestrian',        6,'line', 3,'none','#ededed','');
INSERT INTO map_def VALUES (17,'highway','track',             5,'line', 1,'none','#a5832c','9,3');
INSERT INTO map_def VALUES (17,'highway','footway',           5,'line', 1,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (17,'highway','path',              5,'line', 1,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (17,'highway','cycleway',          5,'line', 1,'none','#0e0efe','3,3');
INSERT INTO map_def VALUES (17,'highway','steps',             5,'line', 3,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (17,'railway','rail',              5,'line', 4,'none','#777777','');
INSERT INTO map_def VALUES (17,'railway','rail',              8,'line', 2,'none','#eeeeee','8,8');
INSERT INTO map_def VALUES (17,'railway','tram',              8,'line', 2,'none','#6e6e6e','');
INSERT INTO map_def VALUES (17,'power','line',                9,'line', 1,'none','#aaaaaa','');
INSERT INTO map_def VALUES (17,'name','%',                   12,'text', 8,'#303030','','');
/*
** Zoomlevel 18
*/
INSERT INTO map_def VALUES (18,'landuse','farmland',          1,'area',0,'#eef0d5','none','');
INSERT INTO map_def VALUES (18,'landuse','commercial',        1,'area',1,'#f2dad9','#ddc4c2','');
INSERT INTO map_def VALUES (18,'landuse','residential',       1,'area',0,'#e0dfdf','none','');
INSERT INTO map_def VALUES (18,'landuse','industrial',        1,'area',0,'#ebdbe8','none','');
INSERT INTO map_def VALUES (18,'landuse','railway',           1,'area',0,'#e9dae7','none','');
INSERT INTO map_def VALUES (18,'landuse','grass',             2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (18,'landuse','meadow',            2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (18,'landuse','village_green',     2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (18,'natural','grassland',         2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (18,'natural','scrub',             2,'area',0,'#c8d7ab','none','');
INSERT INTO map_def VALUES (18,'landuse','forest',            2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (18,'natural','wood',              2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (18,'landuse','vineyard',          2,'area',0,'#bddc9a','none','');
INSERT INTO map_def VALUES (18,'landuse','farmyard',          2,'area',0,'#f5dcba','none','');
INSERT INTO map_def VALUES (18,'landuse','orchard',           2,'area',0,'#aedfa3','none','');
INSERT INTO map_def VALUES (18,'landuse','allotments',        2,'area',0,'#d5e4cb','none','');
INSERT INTO map_def VALUES (18,'leisure','park',              2,'area',0,'#c8facc','none','');
INSERT INTO map_def VALUES (18,'landuse','cemetery',          2,'area',0,'#aacbaf','none','');
INSERT INTO map_def VALUES (18,'landuse','recreation_ground', 2,'area',1,'#dffce2','#9dd5a1','');
INSERT INTO map_def VALUES (18,'amenity','%',                 2,'area',0,'#eeeeee','none','');
INSERT INTO map_def VALUES (18,'landuse','construction',      2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (18,'landuse','brownfield',        2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (18,'leisure','playground',        3,'area',1,'#dffce2','#a1dea6','');
INSERT INTO map_def VALUES (18,'tourism','camp_site',         3,'area',0,'#def6c0','none','');
INSERT INTO map_def VALUES (18,'leisure','pitch',             3,'area',1,'#aae0cb','#8ecfb5','');
INSERT INTO map_def VALUES (18,'leisure','swimming_pool',     3,'area',1,'#aad3df','#7dc7dc','');
INSERT INTO map_def VALUES (18,'highway','platform',          3,'area',1,'#bbbbbb','#929191','');
INSERT INTO map_def VALUES (18,'natural','tree_row',          3,'line',4,'none','#a9d291','');
INSERT INTO map_def VALUES (18,'natural','water',             4,'area',0,'#aad3df','none','');
INSERT INTO map_def VALUES (18,'waterway','stream',           4,'line',2,'none','#aad3df','');
INSERT INTO map_def VALUES (18,'barrier','%',                 4,'line',1,'none','#9fb0a1','');
INSERT INTO map_def VALUES (18,'building','%',                4,'area',1,'#d9d0c9','#bcb2a6','');
INSERT INTO map_def VALUES (18,'man_made','pier',             5,'line',2,'none','#f2efe9','');
INSERT INTO map_def VALUES (18,'border_type','nation',        5,'line',5,'none','#a6a9c0','');
INSERT INTO map_def VALUES (18,'border_type','nation',        6,'line',1,'none','#91769c','30 5 10 5');
INSERT INTO map_def VALUES (18,'highway','motorway',          5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (18,'highway','motorway',          7,'line',10,'none','#e892a2','');
INSERT INTO map_def VALUES (18,'highway','motorway_link',     5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (18,'highway','motorway_link',     7,'line',10,'none','#e892a2','');
INSERT INTO map_def VALUES (18,'highway','primary',           5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (18,'highway','primary',           7,'line',10,'none','#fcd6a4','');
INSERT INTO map_def VALUES (18,'highway','primary_link',      5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (18,'highway','primary_link',      7,'line',10,'none','#fcd6a4','');
INSERT INTO map_def VALUES (18,'highway','secondary',         5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (18,'highway','secondary',         8,'line', 9,'none','#f7fabf','');
INSERT INTO map_def VALUES (18,'highway','secondary_link',    5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (18,'highway','secondary_link',    8,'line', 9,'none','#f7fabf','');
INSERT INTO map_def VALUES (18,'highway','tertiary',          5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (18,'highway','tertiary',          8,'line',7,'none','#ffffff','');
INSERT INTO map_def VALUES (18,'highway','tertiary_link',     5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (18,'highway','tertiary_link',     8,'line',7,'none','#ffffff','');
INSERT INTO map_def VALUES (18,'highway','trunk',             5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (18,'highway','trunk',             7,'line',7,'none','#f9b29c','');
INSERT INTO map_def VALUES (18,'highway','trunk_link',        5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (18,'highway','trunk_link',        7,'line',7,'none','#f9b29c','');
INSERT INTO map_def VALUES (18,'highway','residential',       5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (18,'highway','residential',       8,'line', 4,'none','#ffffff','');
INSERT INTO map_def VALUES (18,'highway','unclassified',      5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (18,'highway','unclassified',      8,'line', 4,'none','#ffffff','');
INSERT INTO map_def VALUES (18,'highway','service',           8,'line', 2,'none','#ffffff','');
INSERT INTO map_def VALUES (18,'highway','living_street',     5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (18,'highway','living_street',     6,'line', 3,'none','#ededed','');
INSERT INTO map_def VALUES (18,'highway','pedestrian',        5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (18,'highway','pedestrian',        6,'line', 3,'none','#ededed','');
INSERT INTO map_def VALUES (18,'highway','track',             5,'line', 1,'none','#a5832c','9,3');
INSERT INTO map_def VALUES (18,'highway','footway',           5,'line', 1,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (18,'highway','path',              5,'line', 1,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (18,'highway','cycleway',          5,'line', 1,'none','#0e0efe','3,3');
INSERT INTO map_def VALUES (18,'highway','steps',             5,'line', 3,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (18,'railway','rail',              5,'line', 4,'none','#777777','');
INSERT INTO map_def VALUES (18,'railway','rail',              8,'line', 2,'none','#eeeeee','8,8');
INSERT INTO map_def VALUES (18,'railway','tram',              8,'line', 2,'none','#6e6e6e','');
INSERT INTO map_def VALUES (18,'power','line',                9,'line', 1,'none','#aaaaaa','');
INSERT INTO map_def VALUES (18,'name','%',                   12,'text', 8,'#303030','','');
/*
** Zoomlevel 19
*/
INSERT INTO map_def VALUES (19,'landuse','farmland',          1,'area',0,'#eef0d5','none','');
INSERT INTO map_def VALUES (19,'landuse','commercial',        1,'area',1,'#f2dad9','#ddc4c2','');
INSERT INTO map_def VALUES (19,'landuse','residential',       1,'area',0,'#e0dfdf','none','');
INSERT INTO map_def VALUES (19,'landuse','industrial',        1,'area',0,'#ebdbe8','none','');
INSERT INTO map_def VALUES (19,'landuse','railway',           1,'area',0,'#e9dae7','none','');
INSERT INTO map_def VALUES (19,'landuse','grass',             2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (19,'landuse','meadow',            2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (19,'landuse','village_green',     2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (19,'natural','grassland',         2,'area',0,'#cdebb0','none','');
INSERT INTO map_def VALUES (19,'natural','scrub',             2,'area',0,'#c8d7ab','none','');
INSERT INTO map_def VALUES (19,'landuse','forest',            2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (19,'natural','wood',              2,'area',0,'#add19e','none','');
INSERT INTO map_def VALUES (19,'landuse','vineyard',          2,'area',0,'#bddc9a','none','');
INSERT INTO map_def VALUES (19,'landuse','farmyard',          2,'area',0,'#f5dcba','none','');
INSERT INTO map_def VALUES (19,'landuse','orchard',           2,'area',0,'#aedfa3','none','');
INSERT INTO map_def VALUES (19,'landuse','allotments',        2,'area',0,'#d5e4cb','none','');
INSERT INTO map_def VALUES (19,'leisure','park',              2,'area',0,'#c8facc','none','');
INSERT INTO map_def VALUES (19,'landuse','cemetery',          2,'area',0,'#aacbaf','none','');
INSERT INTO map_def VALUES (19,'landuse','recreation_ground', 2,'area',1,'#dffce2','#9dd5a1','');
INSERT INTO map_def VALUES (19,'amenity','%',                 2,'area',0,'#eeeeee','none','');
INSERT INTO map_def VALUES (19,'landuse','construction',      2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (19,'landuse','brownfield',        2,'area',0,'#c7c7b4','none','');
INSERT INTO map_def VALUES (19,'leisure','playground',        3,'area',1,'#dffce2','#a1dea6','');
INSERT INTO map_def VALUES (19,'tourism','camp_site',         3,'area',0,'#def6c0','none','');
INSERT INTO map_def VALUES (19,'leisure','pitch',             3,'area',1,'#aae0cb','#8ecfb5','');
INSERT INTO map_def VALUES (19,'leisure','swimming_pool',     3,'area',1,'#aad3df','#7dc7dc','');
INSERT INTO map_def VALUES (19,'highway','platform',          3,'area',1,'#bbbbbb','#929191','');
INSERT INTO map_def VALUES (19,'natural','tree_row',          3,'line',4,'none','#a9d291','');
INSERT INTO map_def VALUES (19,'natural','water',             4,'area',0,'#aad3df','none','');
INSERT INTO map_def VALUES (19,'waterway','stream',           4,'line',2,'none','#aad3df','');
INSERT INTO map_def VALUES (19,'barrier','%',                 4,'line',1,'none','#9fb0a1','');
INSERT INTO map_def VALUES (19,'building','%',                4,'area',1,'#d9d0c9','#bcb2a6','');
INSERT INTO map_def VALUES (19,'man_made','pier',             5,'line',2,'none','#f2efe9','');
INSERT INTO map_def VALUES (19,'border_type','nation',        5,'line',5,'none','#a6a9c0','');
INSERT INTO map_def VALUES (19,'border_type','nation',        6,'line',1,'none','#91769c','30 5 10 5');
INSERT INTO map_def VALUES (19,'highway','motorway',          5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (19,'highway','motorway',          7,'line',10,'none','#e892a2','');
INSERT INTO map_def VALUES (19,'highway','motorway_link',     5,'line',12,'none','#de3a71','');
INSERT INTO map_def VALUES (19,'highway','motorway_link',     7,'line',10,'none','#e892a2','');
INSERT INTO map_def VALUES (19,'highway','primary',           5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (19,'highway','primary',           7,'line',10,'none','#fcd6a4','');
INSERT INTO map_def VALUES (19,'highway','primary_link',      5,'line',12,'none','#a26e04','');
INSERT INTO map_def VALUES (19,'highway','primary_link',      7,'line',10,'none','#fcd6a4','');
INSERT INTO map_def VALUES (19,'highway','secondary',         5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (19,'highway','secondary',         8,'line', 9,'none','#f7fabf','');
INSERT INTO map_def VALUES (19,'highway','secondary_link',    5,'line',11,'none','#888888','');
INSERT INTO map_def VALUES (19,'highway','secondary_link',    8,'line', 9,'none','#f7fabf','');
INSERT INTO map_def VALUES (19,'highway','tertiary',          5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (19,'highway','tertiary',          8,'line',7,'none','#ffffff','');
INSERT INTO map_def VALUES (19,'highway','tertiary_link',     5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (19,'highway','tertiary_link',     8,'line',7,'none','#ffffff','');
INSERT INTO map_def VALUES (19,'highway','trunk',             5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (19,'highway','trunk',             7,'line',7,'none','#f9b29c','');
INSERT INTO map_def VALUES (19,'highway','trunk_link',        5,'line',9,'none','#888888','');
INSERT INTO map_def VALUES (19,'highway','trunk_link',        7,'line',7,'none','#f9b29c','');
INSERT INTO map_def VALUES (19,'highway','residential',       5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (19,'highway','residential',       8,'line', 4,'none','#ffffff','');
INSERT INTO map_def VALUES (19,'highway','unclassified',      5,'line', 6,'none','#888888','');
INSERT INTO map_def VALUES (19,'highway','unclassified',      8,'line', 4,'none','#ffffff','');
INSERT INTO map_def VALUES (19,'highway','service',           8,'line', 2,'none','#ffffff','');
INSERT INTO map_def VALUES (19,'highway','living_street',     5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (19,'highway','living_street',     6,'line', 3,'none','#ededed','');
INSERT INTO map_def VALUES (19,'highway','pedestrian',        5,'line', 5,'none','#c4c4c4','');
INSERT INTO map_def VALUES (19,'highway','pedestrian',        6,'line', 3,'none','#ededed','');
INSERT INTO map_def VALUES (19,'highway','track',             5,'line', 1,'none','#a5832c','9,3');
INSERT INTO map_def VALUES (19,'highway','footway',           5,'line', 1,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (19,'highway','path',              5,'line', 1,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (19,'highway','cycleway',          5,'line', 1,'none','#0e0efe','3,3');
INSERT INTO map_def VALUES (19,'highway','steps',             5,'line', 3,'none','#fa8274','3,3');
INSERT INTO map_def VALUES (19,'railway','rail',              5,'line', 4,'none','#777777','');
INSERT INTO map_def VALUES (19,'railway','rail',              8,'line', 2,'none','#eeeeee','8,8');
INSERT INTO map_def VALUES (19,'railway','tram',              8,'line', 2,'none','#6e6e6e','');
INSERT INTO map_def VALUES (19,'power','line',                9,'line', 1,'none','#aaaaaa','');
INSERT INTO map_def VALUES (19,'name','%',                   12,'text', 8,'#303030','','');
/*
** Index
*/
CREATE INDEX map_def__key_value ON map_def (key, value);
COMMIT;
