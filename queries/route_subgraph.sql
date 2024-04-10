/*
** Create a smaller temp. table "subgraph" from the table "graph"
**   - R*Tree 'rtree_way' is required
**   - overlaps boundingbox slightly
*/
.mode table
.timer on

/*
** Boundingbox:
**    min_lon (x1):  7.81, min_lat (y1): 47.97
**    max_lon (x2):  7.83, max_lat (y2): 47.98
*/
.parameter set $min_lon  7.81
.parameter set $min_lat 47.97
.parameter set $max_lon  7.83
.parameter set $max_lat 47.98

/*
**
*/
CREATE TEMP TABLE subgraph AS
SELECT edge_id,start_node_id,end_node_id,dist,way_id
FROM graph
WHERE way_id IN (
 SELECT way_id
 FROM rtree_way
 WHERE max_lon>=$min_lon AND min_lon<=$max_lon
   AND max_lat>=$min_lat AND min_lat<=$max_lat
);
/*
** Look-up table to get node numbers from 1 to N
*/
CREATE TEMP TABLE subgraph_nodes (
 no      INTEGER PRIMARY KEY,
 node_id INTEGER,
 lon     REAL,
 lat     REAL
);
INSERT INTO subgraph_nodes (node_id, lon, lat)
SELECT s.node_id,n.lon,n.lat FROM
(
 SELECT start_node_id AS node_id FROM subgraph
 UNION
 SELECT end_node_id AS node_id FROM subgraph
) AS s
LEFT JOIN nodes AS n ON s.node_id=n.node_id;
/*
** Determine the largest node number
*/
SELECT max(no) FROM subgraph_nodes;
/*
** Show all edges with number of nodes from 1 to N
*/
SELECT s.edge_id,sns.no,sne.no,s.dist,s.way_id
FROM subgraph AS s
LEFT JOIN subgraph_nodes AS sns ON s.start_node_id=sns.node_id
LEFT JOIN subgraph_nodes AS sne ON s.end_node_id=sne.node_id;
