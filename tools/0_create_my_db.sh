#!/bin/bash
#
# This file shows an example workflow
#
# database, OSM pbf file, result dir
db=$HOME/osm/database/freiburg-regbez-latest.db
osm_pbf=$HOME/osm/pbf/freiburg-regbez-latest.osm.pbf
result=$HOME/osm/results
# String for file name Date
cdate=$(date '+%Y%m%d')
#
# Read the data into a database
#  - read from stdin
#  - create addr tables, R*Tree indexes and table 'graph'
#
rm -f $db
osmium cat $osm_pbf -f osm -o - | osm2sqlite $db read - addr rtree graph
# create the table 'map_def' in the database
sqlite3 $db < map_def.sql
# fill field 'permit' in table 'graph' 
./fill_graph_permit.py $db
#
# Draw a simple map
#
./map.py $db 7.807 47.982 16 1300 900 $result/$cdate-map_zoom16.svg
#
# Find the shortest route
#
./route.py $db 7.808 47.983 7.889 47.897 1 $result/freiburg_schauinsland.csv
./html_leaflet_csv.py $result/freiburg_schauinsland.csv $result/$cdate-map_route_freiburg_schauinsland.html
./convert_csv2gpx.py $result/freiburg_schauinsland.csv $result/freiburg_schauinsland.gpx
#
# Create HTML file with a map of the addresses
#
./html_leaflet_addr.py $db 7.791 47.975 7.809 47.983 $result/$cdate-map_adressen_freiburg_st_georgen.html
