#!/bin/bash
#
# Test ./map.py
#
database="$HOME/osm/database/freiburg-regbez-latest.db"
lon=7.8001642
lat=47.979047
sqlite3 $database < map_def.sql 

time ./map.py $database $lon $lat 13  109   73 > tmp_zoom13.svg
time ./map.py $database $lon $lat 14  218  146 > tmp_zoom14.svg
time ./map.py $database $lon $lat 15  435  291 > tmp_zoom15.svg
time ./map.py $database $lon $lat 16  870  582 > tmp_zoom16.svg
time ./map.py $database $lon $lat 17 1740 1164 > tmp_zoom17.svg

# Calculate boundingbox in pixel:
# Zoomlevel 13: 109 x 73 pixel
# Zoomlevel 14: 218 x 146 pixel
# Zoomlevel 15: 435 x 291 pixel
# Zoomlevel 16: 870 x 582 pixel

