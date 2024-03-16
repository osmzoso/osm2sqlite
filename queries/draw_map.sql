/*
**
**
*/
.mode table
.timer on

.parameter set $min_lon  7.8537118
.parameter set $min_lat 47.9945562
.parameter set $max_lon  7.8538969
.parameter set $max_lat 47.9946423
.parameter set $zoomlevel 16
.parameter list

.print "ways:"
SELECT way_id
FROM rtree_way
WHERE max_lon>=$min_lon AND min_lon<=$max_lon
  AND max_lat>=$min_lat AND min_lat<=$max_lat
;

.print "nodes:"
SELECT node_id
FROM rtree_node
WHERE max_lon>=$min_lon AND min_lon<=$max_lon
  AND max_lat>=$min_lat AND min_lat<=$max_lat
;

.print "*********** TEST1:"
WITH bbox_ways AS
(
  SELECT way_id
  FROM rtree_way
  WHERE max_lon>=$min_lon AND min_lon<=$max_lon
    AND max_lat>=$min_lat AND min_lat<=$max_lat
)
SELECT w.way_id,
 wt.key,wt.value,
 md.layer,md.style,md.width,md.fill,md.stroke,md.dash
FROM bbox_ways AS w
LEFT JOIN way_tags AS wt ON w.way_id=wt.way_id
LEFT JOIN map_def AS md ON wt.key=md.key AND wt.value LIKE md.value AND md.zoomlevel=$zoomlevel
;

WITH bbox_nodes AS
(
  SELECT node_id
  FROM rtree_node
  WHERE max_lon>=$min_lon AND min_lon<=$max_lon
    AND max_lat>=$min_lat AND min_lat<=$max_lat
)
SELECT n.node_id,
 nt.key,nt.value,
 md.layer,md.style,md.width,md.fill,md.stroke,md.dash
FROM bbox_nodes AS n
LEFT JOIN node_tags AS nt ON n.node_id=nt.node_id
LEFT JOIN map_def AS md ON nt.key=md.key AND nt.value LIKE md.value AND md.zoomlevel=$zoomlevel
;
/*
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
*/

.print "TEST2:"
WITH bbox_nodes AS
(
  SELECT node_id
  FROM rtree_node
  WHERE max_lon>=$min_lon AND min_lon<=$max_lon
    AND max_lat>=$min_lat AND min_lat<=$max_lat
)
SELECT bb.node_id,json_group_object(nt.key,nt.value) AS tags_json
FROM bbox_nodes AS bb
LEFT JOIN node_tags AS nt ON bb.node_id=nt.node_id
GROUP BY bb.node_id
;

/*
.print
.print 'Test group json'
.print
.mode table
CREATE TEMP TABLE way_tags_json AS
SELECT way_id,json_group_object(key,value) AS tags_json
FROM way_tags
GROUP BY way_id
LIMIT 20
;
*/
