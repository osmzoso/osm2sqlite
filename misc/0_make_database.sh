#!/bin/bash
#
# Test
#
# Directories for the XML files, databases and evaluation results
dir_xml_bz2="$HOME/osm/xml"
dir_database="$HOME/osm/database"
dir_results="$HOME/osm/results"
# String for file name Date
cdate=$(date '+%Y%m%d')
#
# name of the xml data from geofabrik
#
name="freiburg-regbez-latest"
#name="saarland-latest"
#
# filenames
#
osm_xml_bz2_file="$dir_xml_bz2/$name.osm.bz2"
database_file="$dir_database/$name.db"
echo "file osm xml  : " $osm_xml_bz2_file
echo "file database : " $database_file
#
# read data
#
rm $database_file
time bzip2 -c -d $osm_xml_bz2_file | ../osm2sqlite - $database_file addr rtree-ways
#
# Routing (experimental table 'graph' is required)
#
./create_table_graph.py $database_file
# St. Georgen -> Halde
./route.py $database_file 7.808 47.983 7.889 47.897 > $dir_results/route.txt 
./leaflet/print_route_map_html.py $dir_results/route.txt > "$dir_results/$cdate-map_routing_path1.html"
#
# create an HTML file with a map of the addresses
#
./leaflet/print_addr_map_html.py $database_file 7.791 47.975 7.809 47.983 > "$dir_results/$cdate-map_adressen_freiburg_st_georgen.html"
#
# create an HTML file with a map of the routing graph
#
./leaflet/print_graph_map_html.py $database_file 7.81 47.97 7.83 47.98 > "$dir_results/$cdate-map_routing_graph_freiburg.html"
#
# check addr name (additional rtree index 'highway' is needed)
#
sqlite3 $database_file < ../query/add_rtree_highway.sql
./check_data_addr_highway.py $database_file 791% > "$dir_results/$cdate-error_addr_highway.html"
#
# show a simple interactive map
#
./draw_map_interactive.py $database_file 7.807 47.982

