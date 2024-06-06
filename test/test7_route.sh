#!/bin/bash
#
# Test route.py (table 'graph' is required)
#
db=$HOME/osm/database/freiburg-regbez-latest.db
result=$HOME/osm/test

# Test 0 : Visualize table graph
min_lon=7.79
min_lat=47.96
max_lon=7.874
max_lat=47.998
../tools/map_graph.py $db $min_lon $min_lat $max_lon $max_lat 1 course $result/route0_visualize_graph_foot.html
../tools/map_graph.py $db $min_lon $min_lat $max_lon $max_lat 2 course $result/route0_visualize_graph_bike_gravel.html
../tools/map_graph.py $db $min_lon $min_lat $max_lon $max_lat 4 course $result/route0_visualize_graph_bike_road.html
../tools/map_graph.py $db $min_lon $min_lat $max_lon $max_lat 8 course $result/route0_visualize_graph_car.html

# Test 1 : Route Freiburg - Schauinsland
time ../src_py/route.py $db 7.808 47.983 7.889 47.897 1 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route1_foot.html
time ../src_py/route.py $db 7.808 47.983 7.889 47.897 2 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route1_bike_gravel.html
time ../src_py/route.py $db 7.808 47.983 7.889 47.897 4 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route1_bike_road.html
time ../src_py/route.py $db 7.808 47.983 7.889 47.897 8 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route1_car.html

# Test 2 : Route Freiburg Talstraße - Schwabentor
time ../src_py/route.py $db 7.854 47.988 7.8566 47.9948 1 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route2_foot.html
time ../src_py/route.py $db 7.854 47.988 7.8566 47.9948 2 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route2_bike_gravel.html
time ../src_py/route.py $db 7.854 47.988 7.8566 47.9948 4 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route2_bike_road.html
time ../src_py/route.py $db 7.854 47.988 7.8566 47.9948 8 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route2_car.html

# Test 3 : Route Freiburg - Schlossberg
time ../src_py/route.py $db 7.853 47.995 7.862 47.995 1 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route3.html

# Test 4 : Route Hexental - Schweighof
time ../src_py/route.py $db 7.813 47.928 7.834 47.916 1 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route4.html

# Test 5 : Route Freiburg - Offenburg
time ../src_py/route.py $db 7.852 47.995 7.942 48.469 1 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route5_foot.html
time ../src_py/route.py $db 7.852 47.995 7.942 48.469 8 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route5_car.html

# Test 6 : Route Freiburg - Konstanz
time ../src_py/route.py $db 7.852 47.995 9.209 47.667 1 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route6.html
