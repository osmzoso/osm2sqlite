/*
** Create R*Tree indexes
**
** https://www.sqlite.org/rtree.html
**
*/
DROP TABLE IF EXISTS rtree_way;
CREATE VIRTUAL TABLE rtree_way USING rtree(way_id, min_lat, max_lat, min_lon, max_lon);
INSERT INTO rtree_way (way_id, min_lat, max_lat, min_lon, max_lon)
SELECT way_nodes.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)
FROM way_nodes
LEFT JOIN nodes ON way_nodes.node_id=nodes.node_id
GROUP BY way_nodes.way_id;

DROP TABLE IF EXISTS rtree_node;
CREATE VIRTUAL TABLE rtree_node USING rtree(node_id, min_lat, max_lat, min_lon, max_lon);
INSERT INTO rtree_node (node_id, min_lat, max_lat, min_lon, max_lon)
SELECT DISTINCT nodes.node_id,nodes.lat,nodes.lat,nodes.lon,nodes.lon
FROM nodes
LEFT JOIN node_tags ON nodes.node_id=node_tags.node_id
WHERE node_tags.node_id IS NOT NULL;
