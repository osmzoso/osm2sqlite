/*
** Create a smaller subgraph from the table "graph"
**   - R*Tree 'rtree_way' is required
**   - overlaps boundingbox slightly
*/
.mode table
.timer on

/* Boundingbox: min_lon(x1), min_lat(y1), max_lon(x2), max_lat(y2) */
.parameter set $min_lon  7.81
.parameter set $min_lat 47.97
.parameter set $max_lon  7.83
.parameter set $max_lat 47.98
/*
** permit = bit field access
**  Bit 0: foot        (decimal 2^0 =  1)
**  Bit 1: bike_gravel (decimal 2^1 =  2)
**  Bit 2: bike_road   (decimal 2^2 =  4)
**  Bit 3: car         (decimal 2^3 =  8)
**  Bit 4: bike_oneway (decimal 2^4 = 16)
**  Bit 5: car_oneway  (decimal 2^5 = 32)
**
** Possible masks:
**  foot        : 0b000001 (decimal 1)
**  bike_gravel : 0b000010 (decimal 2)
**  bike_road   : 0b000100 (decimal 4)
**  car         : 0b001000 (decimal 8)
*/
.parameter set $mask_permit 8

/*
** 1. Create temp. table "subgraph"
*/
CREATE TEMP TABLE subgraph AS
SELECT edge_id,start_node_id,end_node_id,dist,
       CASE
         WHEN ($mask_permit=2 AND permit&16=16) OR
              ($mask_permit=4 AND permit&16=16) OR
              ($mask_permit=8 AND permit&32=32) THEN 1
         ELSE 0
       END AS directed
FROM graph
WHERE permit & $mask_permit != 0 AND
      way_id IN (
                 SELECT way_id FROM rtree_way
                 WHERE max_lon>=$min_lon AND min_lon<=$max_lon
                   AND max_lat>=$min_lat AND min_lat<=$max_lat
                )
;
/* Create temp. table "subgraph_nodes"
** (look-up table to get node numbers from 1 to N)
*/
CREATE TEMP TABLE subgraph_nodes (
 no      INTEGER PRIMARY KEY,
 node_id INTEGER,
 lon     REAL,
 lat     REAL
)
;
INSERT INTO subgraph_nodes (node_id, lon, lat)
SELECT s.node_id,n.lon,n.lat FROM
(
 SELECT start_node_id AS node_id FROM subgraph
 UNION
 SELECT end_node_id AS node_id FROM subgraph
) AS s
LEFT JOIN nodes AS n ON s.node_id=n.node_id
;

/*
** 2. Query the subgraph
*/

/* Number of nodes */
SELECT max(no) FROM subgraph_nodes;
/* List of edges with node numbers from 1 to N */
SELECT g.edge_id,ns.no,ne.no,g.dist,g.directed 
FROM subgraph AS g
LEFT JOIN subgraph_nodes AS ns ON g.start_node_id=ns.node_id
LEFT JOIN subgraph_nodes AS ne ON g.end_node_id=ne.node_id;

