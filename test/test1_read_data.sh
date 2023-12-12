#
# Test1: Read OSM XML data
#
if [ $# = 0 ]
then
    echo "error: no .osm.bz2 file specified"
    echo "Usage:"
    echo "$0 FILE_OSM_XML_BZ2"
    exit 1
fi
file_osm_xml_bz2=$1

echo "----------------------------------------------"
echo "Test1: Read OSM XML data"
echo "----------------------------------------------"
echo ".osm.bz2 file : " $file_osm_xml_bz2
rm -f osm_c.db osm_py.db
set -x              # activate bash debugging mode
time bzip2 -c -d $file_osm_xml_bz2 | ../src/osm2sqlite - osm_c.db addr graph
time bzip2 -c -d $file_osm_xml_bz2 | ../src_py/osm2sqlite.py - osm_py.db addr graph
set +x              # stop bash debugging mode
echo "compare size of databases:"
ls -l *.db
echo "compare MD5 hash values of the databases:"
md5sum *.db

