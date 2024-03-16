#!/bin/bash
#
# Test ../src_py/info.py
#
db=$HOME/osm/database/freiburg-regbez-latest.db

../src_py/info.py $db node 1854272308
../src_py/info.py $db node 258017419
../src_py/info.py $db way 30405524 
../src_py/info.py $db relation 9926133 
# Relation Breisach
../src_py/info.py $db relation 1811567
# Relation Staudinger Gesamtschule
../src_py/info.py $db relation 4176098
# Relation Friedhof St. Georgen
../src_py/info.py $db relation 13923337
# Relation EuroVelo 6
../src_py/info.py $db relation 2938
