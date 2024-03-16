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

SELECT 'graph sum dist : '||format('%s', sum(dist)/1000.000)||' km' FROM graph;
