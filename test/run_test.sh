#
#
#
if [ $# = 0 ]
then
    echo "error: no filename specified"
    echo "Usage:"
    echo "$0 FILE_OSM_XML [no-delete]"
    exit 1
fi
file_osm_xml=$1

./test1_read_data.sh $file_osm_xml
sqlite3 < test2_compare_tables.sql
sqlite3 < test3_diff_floating_point.sql

# clean up
if [ "$2" != "no-delete" ]; then
    rm -f osm_c.db osm_py.db
else
    echo "Don't forget to delete the files 'osm_c.db' and 'osm_py.db'"
fi

