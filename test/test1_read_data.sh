#!/bin/bash
#
# Test1: Read OSM data with C and Python version
#
if [ $# != 2 ]; then
    echo "error: no test directory and osm file specified"
    echo "Usage:"
    echo "$0 TEST_DIR TEST_OSM_FILE"
    exit 1
fi
test_dir=$1
test_osm_file=$2

echo "----------------------------------------------"
echo "Test1: Read OSM data with C and Python version"
echo "----------------------------------------------"
echo "Test dir  : $test_dir"
echo "Test file : $test_osm_file"

rm -f $test_dir/osm_c.db $test_dir/osm_py.db

extension="${test_osm_file##*.}"
if [ "$extension" == "bz2" ]; then
    echo "bz2 extension"
    echo "read .osm.bz2 file with C version in database 'osm_c.db'..."
    time bzip2 -c -d $test_dir/$test_osm_file | ../src/osm2sqlite $test_dir/osm_c.db read - addr graph rtree
    echo "read .osm.bz2 file with Python version in database 'osm_py.db'..."
    time bzip2 -c -d $test_dir/$test_osm_file | ./osm2sqlite.py $test_dir/osm_py.db read - addr graph rtree
elif [ "$extension" == "pbf" ]; then
    echo "pbf extension"
    echo "read .osm.pbf file with C version in database 'osm_c.db'..."
    time osmium cat $test_dir/$test_osm_file -f osm -o - | ../src/osm2sqlite $test_dir/osm_c.db read - addr graph rtree
    echo "read .osm.pbf file with Python version in database 'osm_py.db'..."
    time osmium cat $test_dir/$test_osm_file -f osm -o - | ./osm2sqlite.py $test_dir/osm_py.db read - addr graph rtree
else
    echo "unknown extension"
fi
echo "compare size of databases:"
ls -l $test_dir/*.db
echo "compare MD5 hash values of the databases:"
md5sum $test_dir/*.db
