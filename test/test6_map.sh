#!/bin/bash
#
# Test map.py
#
db=$HOME/osm/database/freiburg-regbez-latest.db
result=$HOME/osm/results

sqlite3 $db < ../src_py/map_def.sql 

lon=7.8001642
lat=47.979047
time ../src_py/map.py $db $lon $lat 16 900 600 $result/map_zoom16.svg
time ../src_py/map.py $db $lon $lat 17 900 600 $result/map_zoom17.svg
time ../src_py/map.py $db $lon $lat 18 900 600 $result/map_zoom18.svg
time ../src_py/map.py $db $lon $lat 19 900 600 $result/map_zoom19.svg

# convert to png format with inkscape
inkscape $result/map_zoom16.svg -o $result/map_zoom16.png

# create HTML file with a map of the routing graph
../tools/html_map_table_graph.py $db 7.81 47.97 7.83 47.98 > $result/map_table_graph.html

# Profiler
python -m cProfile ../src_py/map.py $db $lon $lat 16 900 600 $result/map_profile.svg > $result/map_profile.txt
