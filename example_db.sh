#!/bin/bash
#
# This file shows an example workflow
#
# Directories for the XML files, databases and evaluation results
dir_xml_bz2="$HOME/osm/xml"
dir_database="$HOME/osm/database"
dir_results="$HOME/osm/results"
# String for file name Date
cdate=$(date '+%Y%m%d')
#
# name of the bz2 compressed xml file
name="freiburg-regbez-latest"
db="$dir_database/$name.db"
#
# Read data and create a new database
#
rm $db
time bzip2 -c -d "$dir_xml_bz2/$name.osm.bz2" | ./osm2sqlite - $db addr rtree-ways graph
#
# Routing (table 'graph' is required)
#
# Freiburg -> Schauinsland
./routing/route.py $db 7.808 47.983 7.889 47.897 > "$dir_results/freiburg_schauinsland.csv"
./tools/html_map_csv.py "$dir_results/freiburg_schauinsland.csv" > "$dir_results/$cdate-map_route_freiburg_schauinsland.html"
./tools/convert_csv2gpx.py "$dir_results/freiburg_schauinsland.csv" > "$dir_results/freiburg_schauinsland.gpx"
#
# Tilemaps with Leaflet.js
#
# create HTML file with a map of the addresses
./tools/html_map_addr.py $db 7.791 47.975 7.809 47.983 > "$dir_results/$cdate-map_adressen_freiburg_st_georgen.html"
# create HTML file with a map of the routing graph
./tools/html_map_table_graph.py $db 7.81 47.97 7.83 47.98 > "$dir_results/$cdate-map_table_graph_freiburg.html"
#
# Check data
#
# check addr name (additional rtree index 'rtree_highway' is needed)
sqlite3 $db < ./queries/add_rtree_highway.sql
./check_data/check_data_addr_highway.py $db 791% > "$dir_results/$cdate-error_addr_highway.html"
#
# Draw map
#
sqlite3 $db < ./mapdrawing/map_def.sql 
./mapdrawing/map.py $db 7.807 47.982 16 1300 900 > "$dir_results/$cdate-map_zoom16.svg"
