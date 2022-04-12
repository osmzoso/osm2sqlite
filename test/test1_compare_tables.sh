#
# Testcase1
#
# Compare tables between C-Version and Python-Version
#
if [ $# = 0 ]
then
    echo "Error: No OSM Filename"
    echo "Usage:"
    echo "$0 FILE_OSM_XML"
    exit 1
fi
file_osm_xml=$1

echo "----------------------------------------------"
echo "Help Output C-Version"
echo "----------------------------------------------"
osm2sqlite
echo "----------------------------------------------"
echo "Help Output Python-Version"
echo "----------------------------------------------"
python ../osm2sqlite.py

echo "----------------------------------------------"
echo "Read OSM XML $file_osm_xml"
echo "----------------------------------------------"
set -x              # activate bash debugging mode
rm -f osm_c.db
osm2sqlite $file_osm_xml osm_c.db
rm -f osm_py.db
python ../osm2sqlite.py $file_osm_xml osm_py.db
set +x              # stop bash debugging mode
# Print size and MD5-Hash of the databases
ls -l *.db
md5sum *.db

echo "----------------------------------------------"
echo "Check difference"
echo "----------------------------------------------"
sql_shell="
.mode table

-- Connection to the databases
ATTACH DATABASE './osm_c.db'  AS v1;
ATTACH DATABASE './osm_py.db' AS v2;

.print 'diff in table \"nodes\":'
SELECT 'osm_c' AS source,* FROM v1.nodes
EXCEPT
SELECT 'osm_c' AS source,* FROM v2.nodes
;
SELECT 'osm_py'AS source,* FROM v2.nodes
EXCEPT
SELECT 'osm_py'AS source,* FROM v1.nodes
;

.print 'diff in table \"node_tags\":'
SELECT 'osm_c' AS source,* FROM v1.node_tags
EXCEPT
SELECT 'osm_c' AS source,* FROM v2.node_tags
;
SELECT 'osm_py'AS source,* FROM v2.node_tags
EXCEPT
SELECT 'osm_py'AS source,* FROM v1.node_tags
;

.print 'diff in table \"way_nodes\":'
SELECT 'osm_c' AS source,* FROM v1.way_nodes
EXCEPT
SELECT 'osm_c' AS source,* FROM v2.way_nodes
;
SELECT 'osm_py'AS source,* FROM v2.way_nodes
EXCEPT
SELECT 'osm_py'AS source,* FROM v1.way_nodes
;

.print 'diff in table \"way_tags\":'
SELECT 'osm_c' AS source,* FROM v1.way_tags
EXCEPT
SELECT 'osm_c' AS source,* FROM v2.way_tags
;
SELECT 'osm_py'AS source,* FROM v2.way_tags
EXCEPT
SELECT 'osm_py'AS source,* FROM v1.way_tags
;

.print 'diff in table \"relation_members\":'
SELECT 'osm_c' AS source,* FROM v1.relation_members
EXCEPT
SELECT 'osm_c' AS source,* FROM v2.relation_members
;
SELECT 'osm_py'AS source,* FROM v2.relation_members
EXCEPT
SELECT 'osm_py'AS source,* FROM v1.relation_members
;

.print 'diff in table \"relation_tags\":'
SELECT 'osm_c' AS source,* FROM v1.relation_tags
EXCEPT
SELECT 'osm_c' AS source,* FROM v2.relation_tags
;
SELECT 'osm_py'AS source,* FROM v2.relation_tags
EXCEPT
SELECT 'osm_py'AS source,* FROM v1.relation_tags
;

"
echo "$sql_shell" | sqlite3

# clean up
rm -f osm_c.db osm_py.db

