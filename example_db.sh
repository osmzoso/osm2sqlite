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
#
name="freiburg-regbez-latest"
#
# Read data and create a new database
#
rm "$dir_database/$name.db"
time bzip2 -c -d "$dir_xml_bz2/$name.osm.bz2" | ./osm2sqlite - "$dir_database/$name.db" addr rtree-ways graph
#
# Routing (table 'graph' is required)
#
# Freiburg -> Schauinsland
./routing/route.py "$dir_database/$name.db" 7.808 47.983 7.889 47.897 > "$dir_results/freiburg_schauinsland.csv"
./leaflet/html_map_csv.py "$dir_results/freiburg_schauinsland.csv" > "$dir_results/$cdate-map_route_freiburg_schauinsland.html"
./tools/convert_csv2gpx.py "$dir_results/freiburg_schauinsland.csv" > "$dir_results/freiburg_schauinsland.gpx"
#
# Tilemaps with Leaflet.js
#
# create HTML file with a map of the addresses
./leaflet/html_map_addr.py "$dir_database/$name.db" 7.791 47.975 7.809 47.983 > "$dir_results/$cdate-map_adressen_freiburg_st_georgen.html"
# create HTML file with a map of the routing graph
./leaflet/html_map_table_graph.py "$dir_database/$name.db" 7.81 47.97 7.83 47.98 > "$dir_results/$cdate-map_table_graph_freiburg.html"
#
# Check data
#
# check addr name (additional rtree index 'rtree_highway' is needed)
sqlite3 "$dir_database/$name.db" < ./queries/add_rtree_highway.sql
./check_data/check_data_addr_highway.py "$dir_database/$name.db" 791% > "$dir_results/$cdate-error_addr_highway.html"
#
# Draw own map
#
# show a simple interactive map
./mapdrawing/draw_map_interactive.py "$dir_database/$name.db" 7.807 47.982

