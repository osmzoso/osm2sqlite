#!/bin/bash
#
#
#
dir_xml_bz2="$HOME/osm/xml"
dir_database="$HOME/osm/database"
dir_results="$HOME/osm/results"
##echo $dir_xml_bz2
##echo $dir_database
##echo $dir_results
#
#
#
cdate=$(date '+%Y%m%d')
##echo $cdate
#
# saarland-latest
#
name="freiburg-regbez-latest"
#
osm_xml_bz2_file="$dir_xml_bz2/$name.osm.bz2"
database_file="$dir_database/$name.db"
echo $osm_xml_bz2_file
echo $database_file
#
# read data
#
rm $database_file
time 7z e -so $osm_xml_bz2_file | ../../osm2sqlite - $database_file addr rtree-ways
time ../routing/calc_graph.py $database_file
#
# generate html doc with map addresses
#
../leaflet/print_addr_map_html.py $database_file 7.791 47.975 7.809 47.983 > "$dir_results/map_adressen_freiburg_st_georgen_$cdate.html"
#
# generate routing graph map
#
../leaflet/print_graph_map_html.py $database_file 7.81 47.97 7.83 47.98 > "$dir_results/map_routing_graph_freiburg_$cdate.html"
#
# check addr name (additional rtree index 'highway' is needed)
#
sqlite3 $database_file < ../../query/add_rtree_highway.sql
../check_osm_data/check_addr_highway.py $database_file 791% > "$dir_results/error_addr_highway_$cdate.txt"
#
# print a simple map
#
../print_map/print_map.py $database_file 7.807 47.982

