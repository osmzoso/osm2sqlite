#!/bin/bash
#
# This file shows an example workflow
#
db="$HOME/osm/database/freiburg-regbez-latest.db"
#osm_bz2="$HOME/osm/xml/freiburg-regbez-latest.osm.bz2"
osm_pbf="$HOME/osm/xml/freiburg-regbez-latest.osm.pbf"
# String for file name Date
cdate=$(date '+%Y%m%d')
#
# Read the data into a database
#
rm $db
#time bzip2 -c -d $osm_bz2 | ./src/osm2sqlite $db - addr rtree graph
time osmium cat $osm_pbf --output-format=osm --output=- | ./src/osm2sqlite $db - addr rtree graph
sqlite3 $db < ./src_py/map_def.sql
#
# Routing (table 'graph' is required)
#
./src_py/route.py $db 7.808 47.983 7.889 47.897 > "$HOME/osm/results/freiburg_schauinsland.csv"
./tools/html_map_csv.py "$HOME/osm/results/freiburg_schauinsland.csv" > "$HOME/osm/results/$cdate-map_route_freiburg_schauinsland.html"
./tools/convert_csv2gpx.py "$HOME/osm/results/freiburg_schauinsland.csv" > "$HOME/osm/results/freiburg_schauinsland.gpx"
#
# Tilemaps with Leaflet.js
#
# create HTML file with a map of the addresses
./tools/html_map_addr.py $db 7.791 47.975 7.809 47.983 > "$HOME/osm/results/$cdate-map_adressen_freiburg_st_georgen.html"
# create HTML file with a map of the routing graph
./tools/html_map_table_graph.py $db 7.81 47.97 7.83 47.98 > "$HOME/osm/results/$cdate-map_table_graph_freiburg.html"
#
# Check addr:street name
#
./src_py/check_addr_street_name.py $db 791% > "$HOME/osm/results/$cdate-error_addr_street_name.html"
#
# Draw map
#
./src_py/map.py $db 7.807 47.982 16 1300 900 > "$HOME/osm/results/$cdate-map_zoom16.svg"

