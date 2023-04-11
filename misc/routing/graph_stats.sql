/*
**
*/

SELECT 'graph edges    : '||count(*) FROM graph;

SELECT 'graph nodes    : '||count(*) FROM
(
    SELECT node_id_from AS node_id FROM graph
    UNION
    SELECT node_id_to AS node_id FROM graph
);

SELECT 'graph sum dist : '||format("%s", sum(dist)/1000.000)||' km' FROM graph;

