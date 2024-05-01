#!/bin/bash
#
# Test map.py
#
db=$HOME/osm/database/freiburg-regbez-latest.db
result=$HOME/osm/test

sqlite3 $db < ../src_py/map_def.sql 

lon=7.8001642
lat=47.979047
time ../src_py/map.py $db $lon $lat 16 900 600 $result/map_zoom16.svg
time ../src_py/map.py $db $lon $lat 17 900 600 $result/map_zoom17.svg
time ../src_py/map.py $db $lon $lat 18 900 600 $result/map_zoom18.svg
time ../src_py/map.py $db $lon $lat 19 900 600 $result/map_zoom19.svg

# convert to png format with inkscape
inkscape $result/map_zoom16.svg -o $result/map_zoom16.png

# Profiler
python -m cProfile ../src_py/map.py $db $lon $lat 16 900 600 $result/map_profile.svg > $result/map_profile.txt
