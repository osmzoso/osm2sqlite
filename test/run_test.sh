#!/bin/bash
if [ $# != 2 ]; then
    echo "Test osm2sqlite C version and Python version"
    echo "Read OSM file (.osm.bz2 or .osm.pbf) and compare the databases"
    echo "Usage:"
    echo "$0 TEST_DIR OSM_FILE"
    exit 1
fi

test_dir=$1
test_osm_file=$2

echo "Test dir  : " $test_dir
echo "Test file : " $test_osm_file

./test1_read_data.sh $test_dir $test_osm_file
./test2_compare_databases.py $test_dir/osm_c.db $test_dir/osm_py.db
./test3_table_graph.py $test_dir/osm_c.db

./test5_map_proj.py
./test6_map.sh $test_dir
./test7_route.sh $test_dir
./test8_tools.sh $test_dir

