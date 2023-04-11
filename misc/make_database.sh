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
# add experimental table 'graph'
#
time ./routing/calc_graph.py $database_file
sqlite3 $database_file < ./routing/graph_stats.sql
#
# create an HTML file with a map of the addresses
#
./leaflet/print_addr_map_html.py $database_file 7.791 47.975 7.809 47.983 > "$dir_results/map_adressen_freiburg_st_georgen_$cdate.html"
#
# create an HTML file with a map of the routing graph
#
./leaflet/print_graph_map_html.py $database_file 7.81 47.97 7.83 47.98 > "$dir_results/map_routing_graph_freiburg_$cdate.html"
#
# check addr name (additional rtree index 'highway' is needed)
#
sqlite3 $database_file < ../query/add_rtree_highway.sql
./check_osm_data/check_addr_highway.py $database_file 791% > "$dir_results/error_addr_highway_$cdate.html"
#
# show a simple interactive map
#
./print_map/print_map.py $database_file 7.807 47.982

