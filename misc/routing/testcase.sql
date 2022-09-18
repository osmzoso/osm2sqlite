/*
** Test der Tabelle 'graph_highway'
*/

.mode table

.print
.print 'Testcase 1 (Anzahl der Kanten)'
.print
SELECT count(*) AS 'anz_edges' FROM graph_highway
;

.print
.print 'Testcase 2 (node in Freiburg, Mettweg)'
.print
.print 'Ausgabe muss folgendes ergeben:'
.print '+--------------+------------+------+----------+'
.print '| node_id_from | node_id_to | dist |  way_id  |'
.print '+--------------+------------+------+----------+'
.print '| 29160858     | 5851921162 | 57   | 4607205  |'
.print '| 30312886     | 29160858   | 107  | 81059621 |'
.print '| 29160858     | 25245344   | 43   | 81059621 |'
.print '+--------------+------------+------+----------+'
.print 'Ausgabe der Query:'
SELECT *
FROM graph_highway
WHERE node_id_from=29160858 OR node_id_to=29160858
;

