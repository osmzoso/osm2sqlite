/*
**
*/

SELECT 'graph edges    : '||max(edge_id) FROM graph;

SELECT 'graph nodes    : '||count(*) FROM
(
    SELECT start_node_id AS node_id FROM graph
    UNION
    SELECT end_node_id AS node_id FROM graph
);

SELECT 'graph sum dist : '||format("%s", sum(dist)/1000.000)||' km' FROM graph;

.mode table

SELECT key,count(*) AS number FROM
(
 SELECT wt.key,wt.value
 FROM graph AS g
 LEFT JOIN way_tags AS wt ON g.way_id=wt.way_id
) AS x
GROUP by key
ORDER BY number DESC
LIMIT 100
;


