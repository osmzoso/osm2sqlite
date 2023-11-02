#!/bin/bash
#
#
#
pandoc -V geometry:margin=0.6in osm2sqlite.md mapdrawing.md -o osm2sqlite.pdf

#
# manpages
# see https://jeromebelleman.gitlab.io/posts/publishing/manpages/
#
pandoc -s -f markdown -t man osm2sqlite.md mapdrawing.md -o osm2sqlite.1

