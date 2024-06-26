#!/bin/bash
#
# This file shows an example workflow
#
# Database
db=$HOME/osm/database/freiburg-regbez-latest.db
# OpenStreetMap PBF file
osm_pbf=$HOME/osm/pbf/freiburg-regbez-latest.osm.pbf
# Result directory
result=$HOME/osm/results
# String for file name Date
cdate=$(date '+%Y%m%d')
#
# Read the data into a database
#  - read from stdin
#  - create addr tables
#  - create R*Tree indexes
#  - create table 'graph'
#
rm $db
osmium cat $osm_pbf --output-format=osm --output=- | ../src/osm2sqlite $db - addr rtree graph
sqlite3 $db < ../src_py/map_def.sql
../src_py/fill_graph_permit.py $db
#
# Map Drawing
#
../src_py/map.py $db 7.807 47.982 16 1300 900 $result/$cdate-map_zoom16.svg
#
# Routing
#
../src_py/route.py $db 7.808 47.983 7.889 47.897 1 $result/freiburg_schauinsland.csv
../tools/map_csv.py $result/freiburg_schauinsland.csv $result/$cdate-map_route_freiburg_schauinsland.html
../tools/convert_csv2gpx.py $result/freiburg_schauinsland.csv $result/freiburg_schauinsland.gpx
#
# Create HTML file with a map of the addresses
#
../tools/map_addr.py $db 7.791 47.975 7.809 47.983 $result/$cdate-map_adressen_freiburg_st_georgen.html
