#!/bin/bash
if [ $# = 0 ]
then
    echo "error: no filename specified"
    echo "Usage:"
    echo "$0 FILE_OSM_XML_BZ2 [nodelete]"
    exit 1
fi
file_osm_xml_bz2=$1

./test1_read_data.sh $file_osm_xml_bz2
./test2_compare_tables.py
./test3_table_graph.py osm_c.db
sqlite3 < test4_diff_floating_point.sql

# clean up
if [ "$2" != "nodelete" ]; then
    rm -f osm_c.db osm_py.db
else
    echo "Don't forget to delete the files 'osm_c.db' and 'osm_py.db'"
fi
