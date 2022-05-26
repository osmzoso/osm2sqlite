#
# Testcase1
#
# Compare tables between C-Version and Python-Version
#
if [ $# = 0 ]
then
    echo "error: no filename specified"
    echo "Usage:"
    echo "$0 FILE_OSM_XML"
    exit 1
fi
file_osm_xml=$1

echo "----------------------------------------------"
echo "Help Output C-Version"
echo "----------------------------------------------"
../osm2sqlite
echo "----------------------------------------------"
echo "Help Output Python-Version"
echo "----------------------------------------------"
../osm2sqlite.py

echo "----------------------------------------------"
echo "Test1: Read OSM XML $file_osm_xml"
echo "----------------------------------------------"
rm -f osm_c.db osm_py.db
set -x              # activate bash debugging mode
../osm2sqlite $file_osm_xml osm_c.db
python ../osm2sqlite.py $file_osm_xml osm_py.db
set +x              # stop bash debugging mode
echo "Size and MD5-Hash of the databases:"
ls -l *.db
md5sum *.db

