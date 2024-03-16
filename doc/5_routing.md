# 5. Routing

## Calculate shortest path

The table **graph** is required for the calculation of shortest paths.

The command
```
./src_py/route.py DATABASE LON_START LAT_START LON_DEST LAT_DEST CSV_FILE
```
calculates the shortest path and outputs the result
as a csv list (lon,lat,ele).

Visualization of a routing path:  
![routing_path.jpg](routing_path.jpg)

``` sql
/*
**  Conversion table from node id to a number from 1 to N
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
** Number of nodes in the subgraph
*/
SELECT max(no) FROM subgraph_nodes;
/*
** Edges with number of nodes from 1 to N
*/
SELECT s.edge_id,sns.no,sne.no,s.dist,s.way_id
FROM subgraph AS s
LEFT JOIN subgraph_nodes AS sns ON s.start_node_id=sns.node_id
LEFT JOIN subgraph_nodes AS sne ON s.end_node_id=sne.node_id;
```
