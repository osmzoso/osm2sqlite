#!/bin/bash
#
# Test ./tools
#
db=$HOME/osm/database/freiburg-regbez-latest.db
result=$HOME/osm/test

#
# Convert
#
cat << EOF > $result/tools_test.csv
7.852,47.994,0
7.855,47.997,0
7.857,47.993,0
EOF

../tools/convert_csv2gpx.py $result/tools_test.csv $result/tools_test.gpx
../tools/map_gpx.py $result/tools_test.gpx $result/tools_map_gpx.html

#
# Map
#
../tools/map_addr.py $db 7.791 47.975 7.809 47.983 $result/tools_map_addr.html
# create HTML file with a map of the routing graph
min_lon=7.79
min_lat=47.96
max_lon=7.83
max_lat=47.99
../tools/map_graph.py $db $min_lon $min_lat $max_lon $max_lat 255 line $result/tools_map_graph.html
../tools/map_graph.py $db $min_lon $min_lat $max_lon $max_lat 1 course $result/tools_map_graph_1_foot.html
../tools/map_graph.py $db $min_lon $min_lat $max_lon $max_lat 2 course $result/tools_map_graph_2_bike_gravel.html
../tools/map_graph.py $db $min_lon $min_lat $max_lon $max_lat 4 course $result/tools_map_graph_4_bike_road.html
../tools/map_graph.py $db $min_lon $min_lat $max_lon $max_lat 8 course $result/tools_map_graph_8_car.html

#
# Info
#
../tools/info.py $db node 1854272308   > $result/tools_info.txt
../tools/info.py $db node 258017419   >> $result/tools_info.txt
../tools/info.py $db way 30405524     >> $result/tools_info.txt
../tools/info.py $db relation 9926133 >> $result/tools_info.txt
../tools/info.py $db relation 1811567  > $result/tools_info_relation_breisach.txt
../tools/info.py $db relation 4176098  > $result/tools_info_relation_staudinger_gesamtschule.txt
../tools/info.py $db relation 13923337 > $result/tools_info_relation_friedhof_st_georgen.txt
../tools/info.py $db relation 2938     > $result/tools_info_relation_eurovelo_6.txt
