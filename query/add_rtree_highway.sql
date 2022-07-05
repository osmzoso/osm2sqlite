/*
** Creates an R*Tree index highway for all ways with key='highway'.
*/
CREATE VIRTUAL TABLE highway USING rtree(way_id, min_lat, max_lat, min_lon, max_lon);
INSERT INTO highway (way_id, min_lat, max_lat, min_lon, max_lon)
SELECT way_tags.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)
FROM way_tags
LEFT JOIN way_nodes ON way_tags.way_id=way_nodes.way_id
LEFT JOIN nodes ON way_nodes.node_id=nodes.node_id
WHERE way_tags.key='highway'
GROUP BY way_tags.way_id;

