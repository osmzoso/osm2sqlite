/*
** Queries to draw a map
*/
.mode table
.timer on

.parameter set $min_lon  7.8537118
.parameter set $min_lat 47.9945562
.parameter set $max_lon  7.8538969
.parameter set $max_lat 47.9946423
.parameter set $zoomlevel 17

.print '**********************************************************'
.print '0. Boundingbox'
.print '**********************************************************'
.parameter list

.print '**********************************************************'
.print '1. Determine all ways, nodes and relations in the area'
.print '**********************************************************'
CREATE TEMP TABLE bbox_ways AS
SELECT way_id
FROM rtree_way
WHERE max_lon>=$min_lon AND min_lon<=$max_lon
  AND max_lat>=$min_lat AND min_lat<=$max_lat
;
CREATE TEMP TABLE bbox_nodes AS
SELECT node_id
FROM rtree_node
WHERE max_lon>=$min_lon AND min_lon<=$max_lon
  AND max_lat>=$min_lat AND min_lat<=$max_lat
;
CREATE TEMP TABLE bbox_relations AS
SELECT rm.relation_id
FROM relation_members AS rm
JOIN relation_tags AS rt ON rm.relation_id=rt.relation_id
    -- only relations with type=multipolygon
    AND rt.key='type' AND rt.value='multipolygon'
WHERE (rm.ref='way' AND rm.ref_id IN (SELECT way_id FROM bbox_ways)) OR
      (rm.ref='node' AND rm.ref_id IN (SELECT node_id FROM bbox_nodes))
GROUP BY rm.relation_id
;

-- TEST
.timer off
SELECT * FROM bbox_ways;
SELECT * FROM bbox_nodes;
SELECT * FROM bbox_relations;
.timer on

.print '**********************************************************'
.print '2. Test join map_def table, create table "map_drawplan"'
.print '**********************************************************'
-- ********** TEST BEGIN **********
SELECT w.way_id,wt.key,wt.value,
       md.opcode,'way' AS ref,w.way_id AS ref_id,md.layer,md.width,md.fill,md.stroke,md.dash
FROM bbox_ways AS w
LEFT JOIN way_tags AS wt ON w.way_id=wt.way_id
LEFT JOIN map_def AS md ON wt.key=md.key AND wt.value LIKE md.value
  AND md.zoomlevel=$zoomlevel AND md.way_node='way'
;
SELECT n.node_id,nt.key,nt.value,
       md.opcode,'node' AS ref,n.node_id AS ref_id,md.layer,md.width,md.fill,md.stroke,md.dash
FROM bbox_nodes AS n
LEFT JOIN node_tags AS nt ON n.node_id=nt.node_id
LEFT JOIN map_def AS md ON nt.key=md.key AND nt.value LIKE md.value
  AND md.zoomlevel=$zoomlevel AND md.way_node='node'
;
SELECT r.relation_id,rt.key,rt.value,
       md.opcode,'relation' AS ref,r.relation_id AS ref_id,md.layer,md.width,md.fill,md.stroke,md.dash
FROM bbox_relations AS r
LEFT JOIN relation_tags AS rt ON r.relation_id=rt.relation_id
LEFT JOIN map_def AS md ON rt.key=md.key AND rt.value LIKE md.value
  AND md.zoomlevel=$zoomlevel AND md.way_node='way'
;
-- ********** TEST END **********

CREATE TEMP TABLE map_drawplan AS
  SELECT md.opcode,'way' AS ref,w.way_id AS ref_id,
    md.layer,md.width,md.fill,md.stroke,md.dash
  FROM bbox_ways AS w
  LEFT JOIN way_tags AS wt ON w.way_id=wt.way_id
  LEFT JOIN map_def AS md ON wt.key=md.key AND wt.value LIKE md.value
    AND md.zoomlevel=$zoomlevel AND md.way_node='way'
  WHERE md.opcode IS NOT NULL
UNION ALL
  SELECT md.opcode,'node' AS ref,n.node_id AS ref_id,
    md.layer,md.width,md.fill,md.stroke,md.dash
  FROM bbox_nodes AS n
  LEFT JOIN node_tags AS nt ON n.node_id=nt.node_id
  LEFT JOIN map_def AS md ON nt.key=md.key AND nt.value LIKE md.value
    AND md.zoomlevel=$zoomlevel AND md.way_node='node'
  WHERE md.opcode IS NOT NULL
UNION ALL
  SELECT md.opcode||'_mp','relation' AS ref,r.relation_id AS ref_id,
    md.layer,md.width,md.fill,md.stroke,md.dash
  FROM bbox_relations AS r
  LEFT JOIN relation_tags AS rt ON r.relation_id=rt.relation_id
  LEFT JOIN map_def AS md ON rt.key=md.key AND rt.value LIKE md.value
    AND md.zoomlevel=$zoomlevel AND md.way_node='way'
  WHERE md.opcode IS NOT NULL
;

-- TEST
.timer off
SELECT opcode,ref,ref_id,layer,width,fill,stroke,dash
FROM map_drawplan
ORDER BY layer
;
.timer on

