#!/bin/bash
if [ $# != 1 ]; then
    echo "Test tools"
    echo "Usage:"
    echo "$0 TEST_DIR"
    exit 1
fi
db=$HOME/osm/database/freiburg-regbez-latest.db
test_dir=$1

echo "-----------------------------------------------"
echo "Test 8: tools"
echo "-----------------------------------------------"
echo "database: $db"

#rm -f $test_dir/*

#
# Convert
#
cat << EOF > $test_dir/tools_test.csv
7.852,47.994,0
7.855,47.997,0
7.857,47.993,0
EOF

../tools/convert_csv2gpx.py $test_dir/tools_test.csv $test_dir/tools_test.gpx
../tools/html_leaflet_gpx.py $test_dir/tools_test.gpx $test_dir/tools_map_gpx.html

#
# Create HTML files with the Leaflet.js library
#
../tools/html_leaflet_addr.py $db 7.791 47.975 7.809 47.983 $test_dir/tools_map_addr.html
# create HTML file with a map of the routing graph
min_lon=7.79
min_lat=47.96
max_lon=7.874
max_lat=47.99
../tools/html_leaflet_graph.py $db $min_lon $min_lat $max_lon $max_lat 255 line $test_dir/tools_map_graph.html
../tools/html_leaflet_graph.py $db $min_lon $min_lat $max_lon $max_lat 1 course $test_dir/tools_map_graph_1_foot.html
../tools/html_leaflet_graph.py $db $min_lon $min_lat $max_lon $max_lat 2 course $test_dir/tools_map_graph_2_bike_gravel.html
../tools/html_leaflet_graph.py $db $min_lon $min_lat $max_lon $max_lat 4 course $test_dir/tools_map_graph_4_bike_road.html
../tools/html_leaflet_graph.py $db $min_lon $min_lat $max_lon $max_lat 8 course $test_dir/tools_map_graph_8_car.html

#
# Info
#
../tools/info.py $db node 1854272308   > $test_dir/tools_info.txt
../tools/info.py $db node 258017419   >> $test_dir/tools_info.txt
../tools/info.py $db way 30405524     >> $test_dir/tools_info.txt
../tools/info.py $db relation 9926133 >> $test_dir/tools_info.txt
../tools/info.py $db relation 1811567  > $test_dir/tools_info_relation_breisach.txt
../tools/info.py $db relation 4176098  > $test_dir/tools_info_relation_staudinger_gesamtschule.txt
../tools/info.py $db relation 13923337 > $test_dir/tools_info_relation_friedhof_st_georgen.txt
../tools/info.py $db relation 2938     > $test_dir/tools_info_relation_eurovelo_6.txt
