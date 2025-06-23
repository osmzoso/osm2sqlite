#!/bin/bash
#
# Test map.py
#
db=$HOME/osm/database/freiburg-regbez-latest.db
test_dir=$HOME/osm

sqlite3 $db < ../tools/map_def.sql

rm -f $test_dir/test_map_*.*

lon=7.8250
lat=47.9913
time ../tools/map.py $db $lon $lat 16 900 600 $test_dir/test_map_zoom16.svg
time ../tools/map.py $db $lon $lat 17 900 600 $test_dir/test_map_zoom17.svg
time ../tools/map.py $db $lon $lat 18 900 600 $test_dir/test_map_zoom18.svg
time ../tools/map.py $db $lon $lat 19 900 600 $test_dir/test_map_zoom19.svg

# convert to png format with inkscape
inkscape $test_dir/test_map_zoom16.svg -o $test_dir/test_map_zoom16.png

# Profiler
python -m cProfile ../tools/map.py $db $lon $lat 16 900 600 $test_dir/map_profile.svg > $test_dir/test_map_profile.txt
