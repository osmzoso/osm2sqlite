.print "----------------------------------------------"
.print "Test2: Show table difference"
.print "----------------------------------------------"
.mode table

ATTACH DATABASE './osm_c.db'  AS db_c;
ATTACH DATABASE './osm_py.db' AS db_py;

.print 'diff in table "nodes":'
SELECT 'osm_c' AS source,* FROM db_c.nodes
EXCEPT
SELECT 'osm_c' AS source,* FROM db_py.nodes
;
SELECT 'osm_py'AS source,* FROM db_py.nodes
EXCEPT
SELECT 'osm_py'AS source,* FROM db_c.nodes
;

.print 'diff in table "node_tags":'
SELECT 'osm_c' AS source,* FROM db_c.node_tags
EXCEPT
SELECT 'osm_c' AS source,* FROM db_py.node_tags
;
SELECT 'osm_py'AS source,* FROM db_py.node_tags
EXCEPT
SELECT 'osm_py'AS source,* FROM db_c.node_tags
;

.print 'diff in table "way_nodes":'
SELECT 'osm_c' AS source,* FROM db_c.way_nodes
EXCEPT
SELECT 'osm_c' AS source,* FROM db_py.way_nodes
;
SELECT 'osm_py'AS source,* FROM db_py.way_nodes
EXCEPT
SELECT 'osm_py'AS source,* FROM db_c.way_nodes
;

.print 'diff in table "way_tags":'
SELECT 'osm_c' AS source,* FROM db_c.way_tags
EXCEPT
SELECT 'osm_c' AS source,* FROM db_py.way_tags
;
SELECT 'osm_py'AS source,* FROM db_py.way_tags
EXCEPT
SELECT 'osm_py'AS source,* FROM db_c.way_tags
;

.print 'diff in table "relation_members":'
SELECT 'osm_c' AS source,* FROM db_c.relation_members
EXCEPT
SELECT 'osm_c' AS source,* FROM db_py.relation_members
;
SELECT 'osm_py'AS source,* FROM db_py.relation_members
EXCEPT
SELECT 'osm_py'AS source,* FROM db_c.relation_members
;

.print 'diff in table "relation_tags":'
SELECT 'osm_c' AS source,* FROM db_c.relation_tags
EXCEPT
SELECT 'osm_c' AS source,* FROM db_py.relation_tags
;
SELECT 'osm_py'AS source,* FROM db_py.relation_tags
EXCEPT
SELECT 'osm_py'AS source,* FROM db_c.relation_tags
;

.print 'diff in table "addr_street":'
SELECT 'osm_c' AS source,* FROM db_c.addr_street
EXCEPT
SELECT 'osm_c' AS source,* FROM db_py.addr_street
;
SELECT 'osm_py'AS source,* FROM db_py.addr_street
EXCEPT
SELECT 'osm_py'AS source,* FROM db_c.addr_street
;

.print 'diff in table "addr_housenumber":'
SELECT 'osm_c' AS source,* FROM db_c.addr_housenumber
EXCEPT
SELECT 'osm_c' AS source,* FROM db_py.addr_housenumber
;
SELECT 'osm_py'AS source,* FROM db_py.addr_housenumber
EXCEPT
SELECT 'osm_py'AS source,* FROM db_c.addr_housenumber
;

