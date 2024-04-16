/*
** Create a smaller subgraph from the table "graph"
**   - R*Tree 'rtree_way' is required
**   - overlaps boundingbox slightly
**
**        car_oneway       # 2^5  32
**        bike_oneway      # 2^4  16
**        car              # 2^3   8
**        bike_road        # 2^2   4
**        bike_gravel      # 2^1   2
**        foot             # 2^0   1
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
.parameter set $permitted 8

/*
** 1. Create the subgraph
**    - temp. table "subgraph"
**    - temp. look-up table "subgraph_nodes" to get node numbers from 1 to N
*/
CREATE TEMP TABLE subgraph AS
SELECT edge_id,start_node_id,end_node_id,dist,permit
FROM graph
WHERE way_id IN (
 SELECT way_id
 FROM rtree_way
 WHERE max_lon>=$min_lon AND min_lon<=$max_lon
   AND max_lat>=$min_lat AND min_lat<=$max_lat)
 AND permit & $permitted=$permitted;

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
** 2. Query the subgraph
*/

/*
** Number of nodes
*/
SELECT max(no) FROM subgraph_nodes;
/*
** List of edges with node numbers from 1 to N
*/
SELECT g.edge_id,ns.no,ne.no,g.dist,g.permit --,format('%02x',g.permit)
FROM subgraph AS g
LEFT JOIN subgraph_nodes AS ns ON g.start_node_id=ns.node_id
LEFT JOIN subgraph_nodes AS ne ON g.end_node_id=ne.node_id;
