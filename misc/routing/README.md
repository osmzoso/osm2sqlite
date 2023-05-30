# Routing

## Calculation of a simple graph for routing purposes

First, routable data must be created from the OSM data.

The testscript `calc_graph.py` creates a simple table with the graph data.

### Table 'graph'

column       | type                | description
-------------|---------------------|-------------------------------------
edge_id      | INTEGER PRIMARY KEY | edge ID
edge_start   | INTEGER             | edge start node ID
edge_end     | INTEGER             | edge end node ID
dist         | INTEGER             | distance in meters
way_id       | INTEGER             | way ID


Visualization of the table 'graph':  

![table_graph.jpg](./table_graph.jpg)

#### Create a subgraph

``` sql
/*
** 1. Create temp. table with edges of the subgraph
**    - R*Tree 'rtree_way' is required, overlaps boundingbox slightly
**
** Boundingbox:
** min_lon (x1):  7.81
** min_lat (y1): 47.97
** max_lon (x2):  7.83
** max_lat (y2): 47.98
*/
CREATE TEMP TABLE subgraph AS
SELECT edge_id,edge_start,edge_end,dist,way_id
FROM graph
WHERE way_id IN (
 SELECT way_id
 FROM rtree_way
 WHERE max_lon>= 7.81 AND min_lon<= 7.83
  AND  max_lat>=47.97 AND min_lat<=47.98
);
```

``` sql
/*
** 2. Create temp. table with list of nodes in subgraph
**    - Conversion list from node id to a number from 1 to N
**    - temp. index for fast search
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
 SELECT edge_start AS node_id FROM subgraph
 UNION
 SELECT edge_end AS node_id FROM subgraph
) AS s
LEFT JOIN nodes AS n ON s.node_id=n.node_id
;
CREATE INDEX subgraph_nodes__node_id ON subgraph_nodes(node_id);
```

#### Useful queries

``` sql
-- Number of nodes in the subgraph
SELECT max(no) FROM subgraph_nodes
```

``` sql
-- Edges with number of nodes from 1 to N
SELECT s.edge_id,sns.no,sne.no,s.dist,s.way_id
FROM subgraph AS s
LEFT JOIN subgraph_nodes AS sns ON s.edge_start=sns.node_id
LEFT JOIN subgraph_nodes AS sne ON s.edge_end=sne.node_id
```

