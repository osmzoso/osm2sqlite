#!/bin/bash
#
# Test route.py (table 'graph' is required)
#
db=$HOME/osm/database/freiburg-regbez-latest.db
result=$HOME/osm/results

time ../src_py/route.py $db 7.808 47.983 7.889 47.897 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route1.html

time ../src_py/route.py $db 7.853 47.995 7.862 47.995 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route2.html

time ../src_py/route.py $db 7.813 47.928 7.834 47.916 $result/route.csv
../tools/map_csv.py $result/route.csv $result/route3.html
