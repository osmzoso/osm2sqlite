/*
**
*/

SELECT 'graph edges    : '||count(*) FROM graph;

SELECT 'graph nodes    : '||count(*) FROM
(
    SELECT edge_start AS node_id FROM graph
    UNION
    SELECT edge_end AS node_id FROM graph
);

SELECT 'graph sum dist : '||format("%s", sum(dist)/1000.000)||' km' FROM graph;

