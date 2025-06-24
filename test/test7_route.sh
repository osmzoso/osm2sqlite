#!/bin/bash
if [ $# != 1 ]; then
    echo "Test route.py"
    echo "Usage:"
    echo "$0 TEST_DIR"
    exit 1
fi
db=$HOME/osm/database/freiburg-regbez-latest.db
test_dir=$1

echo "-----------------------------------------------"
echo "Test 7: route.py"
echo "-----------------------------------------------"
echo "database: $db"

echo "Visualize table graph..."
min_lon=7.79
min_lat=47.96
max_lon=7.874
max_lat=47.998
../tools/html_leaflet_graph.py $db $min_lon $min_lat $max_lon $max_lat 1 course $test_dir/route0_visualize_graph_foot.html
../tools/html_leaflet_graph.py $db $min_lon $min_lat $max_lon $max_lat 2 course $test_dir/route0_visualize_graph_bike_gravel.html
../tools/html_leaflet_graph.py $db $min_lon $min_lat $max_lon $max_lat 4 course $test_dir/route0_visualize_graph_bike_road.html
../tools/html_leaflet_graph.py $db $min_lon $min_lat $max_lon $max_lat 8 course $test_dir/route0_visualize_graph_car.html

echo "Route Freiburg - Schauinsland..."
../tools/route.py $db 7.808 47.983 7.889 47.897 1 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route1_foot.html
../tools/route.py $db 7.808 47.983 7.889 47.897 2 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route1_bike_gravel.html
../tools/route.py $db 7.808 47.983 7.889 47.897 4 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route1_bike_road.html
../tools/route.py $db 7.808 47.983 7.889 47.897 8 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route1_car.html

echo "Route Freiburg Talstraße - Schwabentor..."
../tools/route.py $db 7.854 47.988 7.8566 47.9948 1 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route2_foot.html
../tools/route.py $db 7.854 47.988 7.8566 47.9948 2 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route2_bike_gravel.html
../tools/route.py $db 7.854 47.988 7.8566 47.9948 4 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route2_bike_road.html
../tools/route.py $db 7.854 47.988 7.8566 47.9948 8 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route2_car.html

echo "Route Freiburg - Schlossberg..."
../tools/route.py $db 7.853 47.995 7.862 47.995 1 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route3.html
firefox $test_dir/route3.html

echo "Route Hexental - Schweighof..."
../tools/route.py $db 7.813 47.928 7.834 47.916 1 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route4.html

echo "Route Freiburg - Offenburg..."
time ../tools/route.py $db 7.852 47.995 7.942 48.469 1 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route5_foot.html
firefox $test_dir/route5_foot.html
time ../tools/route.py $db 7.852 47.995 7.942 48.469 8 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route5_car.html
firefox $test_dir/route5_car.html

echo "Route Freiburg - Konstanz..."
time ../tools/route.py $db 7.852 47.995 9.209 47.667 1 $test_dir/route.csv
../tools/html_leaflet_csv.py $test_dir/route.csv $test_dir/route6_foot.html
firefox $test_dir/route6_foot.html
