#!/bin/bash
if [ $# != 1 ]; then
    echo "Test map.py"
    echo "Usage:"
    echo "$0 TEST_DIR"
    exit 1
fi
db=$HOME/osm/database/freiburg-regbez-latest.db
test_dir=$1

echo "-----------------------------------------------"
echo "Test 6: map.py"
echo "-----------------------------------------------"
echo "database: $db"

sqlite3 $db < ../tools/map_def.sql

rm -f $test_dir/test_map_*.*

lon=7.8250
lat=47.9913
../tools/map.py $db $lon $lat 16 900 600 $test_dir/map_zoom16.svg
firefox $test_dir/map_zoom16.svg
../tools/map.py $db $lon $lat 17 900 600 $test_dir/map_zoom17.svg
firefox $test_dir/map_zoom17.svg
../tools/map.py $db $lon $lat 18 900 600 $test_dir/map_zoom18.svg
firefox $test_dir/map_zoom18.svg
../tools/map.py $db $lon $lat 19 900 600 $test_dir/map_zoom19.svg
firefox $test_dir/map_zoom19.svg

# convert to png format with inkscape
inkscape $test_dir/map_zoom16.svg -o $test_dir/map_zoom16.png

# Profiler
python -m cProfile ../tools/map.py $db $lon $lat 16 900 600 $test_dir/map_profile.svg > $test_dir/map_profile.txt
