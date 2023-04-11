/*
** Examples for querying the table 'graph'
**
** Boundingbox
**
** min_lon (x1):  7.81
** min_lat (y1): 47.97
** max_lon (x2):  7.83
** max_lat (y2): 47.98
*/
.timer on

/*
** 1. Determine subgraph
** (R*Tree 'rtree_way' is required, overlap boundingbox slightly)
*/
CREATE TEMP TABLE subgraph AS
SELECT node_id_from,node_id_to,dist,way_id
FROM graph
WHERE way_id IN (
  SELECT way_id
  FROM rtree_way
  WHERE max_lon>= 7.81 AND min_lon<= 7.83
   AND  max_lat>=47.97 AND min_lat<=47.98
);

/*
** 2.Nodes subgraph
*/
CREATE TEMP TABLE subgraph_nodes (
 id      INTEGER PRIMARY KEY,
 node_id INTEGER,
 lon     REAL,
 lat     REAL
);
INSERT INTO subgraph_nodes (node_id, lon, lat)
SELECT s.node_id,n.lon,n.lat FROM
(
  SELECT node_id_from AS node_id FROM subgraph
  UNION
  SELECT node_id_to AS node_id FROM subgraph
) AS s
LEFT JOIN nodes AS n ON s.node_id=n.node_id
;

/*
** Test
*/
.mode table
SELECT * FROM subgraph;
SELECT count(*) FROM subgraph;

SELECT * FROM subgraph_nodes;
SELECT count(*) FROM subgraph_nodes;

