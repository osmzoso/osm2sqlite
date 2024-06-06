#!/bin/bash
#
# Test1: Read OSM data with C and Python version
#
if [ $# = 0 ]; then
    echo "error: no osm file specified"
    echo "Usage:"
    echo "$0 OSM_FILE"
    exit 1
fi
filename=$1

echo "----------------------------------------------"
echo "Test1: Read OSM data with C and Python version"
echo "----------------------------------------------"
rm -f osm_c.db osm_py.db
echo "filename  : $filename"
extension="${filename##*.}"

if [ "$extension" == "bz2" ]; then
    echo "bz2 extension"
    echo "read .osm.bz2 file with C version in database 'osm_c.db'..."
    time bzip2 -c -d $filename | ../src/osm2sqlite osm_c.db - addr graph rtree
    echo "read .osm.bz2 file with Python version in database 'osm_py.db'..."
    time bzip2 -c -d $filename | ../src_py/osm2sqlite.py osm_py.db - addr graph rtree
elif [ "$extension" == "pbf" ]; then
    echo "pbf extension"
    echo "read .osm.pbf file with C version in database 'osm_c.db'..."
    time osmium cat $filename -f osm -o - | ../src/osm2sqlite osm_c.db - addr graph rtree
    echo "read .osm.pbf file with Python version in database 'osm_py.db'..."
    time osmium cat $filename -f osm -o - | ../src_py/osm2sqlite.py osm_py.db - addr graph rtree
else
    echo "unknown extension"
fi
echo "compare size of databases:"
ls -l *.db
echo "compare MD5 hash values of the databases:"
md5sum *.db
