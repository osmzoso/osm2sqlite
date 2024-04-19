/*
** OSM general statistics
*/

-------------------------------------------------------------

SELECT 'number of nodes : '||count(*) FROM nodes;

SELECT 'number of ways  : '||count() FROM
(
  SELECT DISTINCT way_id FROM way_nodes
)
;

-------------------------------------------------------------
.mode table

.print
.print 'All way keys:'
.print
SELECT key,count(*) AS number
FROM way_tags
GROUP BY key
ORDER BY number DESC
;

.print
.print 'All node keys:'
.print
SELECT key,count(*) AS number
FROM node_tags
GROUP BY key
ORDER BY number DESC
;

.print
.print 'All relation keys:'
.print
SELECT key,count(*) AS number
FROM relation_tags
GROUP BY key
ORDER BY number DESC
;

