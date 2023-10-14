#
# Testcase1
#
# Read compressed date with both versions
#
if [ $# = 0 ]
then
    echo "error: no filename specified"
    echo "Usage:"
    echo "$0 FILE_OSM_XML_BZ2"
    exit 1
fi
file_osm_xml_bz2=$1

echo "----------------------------------------------"
echo "Help Output C-Version"
echo "----------------------------------------------"
../osm2sqlite
echo "----------------------------------------------"
echo "Help Output Python-Version"
echo "----------------------------------------------"
../osm2sqlite.py

echo "----------------------------------------------"
echo "Test1: Read OSM XML $file_osm_xml_bz2"
echo "----------------------------------------------"
rm -f osm_c.db osm_py.db
set -x              # activate bash debugging mode
time bzip2 -c -d $file_osm_xml_bz2 | ../osm2sqlite - osm_c.db addr graph
time bzip2 -c -d $file_osm_xml_bz2 | ../osm2sqlite.py - osm_py.db addr graph
set +x              # stop bash debugging mode
echo "Size and MD5-Hash of the databases:"
ls -l *.db
md5sum *.db

