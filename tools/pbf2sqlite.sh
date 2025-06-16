#!/bin/bash
if [ $# != 2 ]; then
    echo "Wrapper to read .osm.pbf files with osm2sqlite and osmium"
    echo "Usage:"
    echo "$0 DATABASE OSM_PBF_FILE"
    exit 1
fi

RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
echo -e "read file ${RED}$2${NC} in database ${CYAN}$1${NC}..."

time osmium cat $2 -f osm -o - | osm2sqlite $1 read -
