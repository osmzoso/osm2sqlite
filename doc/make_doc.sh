#!/bin/bash
#
# PDF
# see https://tex.stackexchange.com/questions/138651/pandoc-markdown-to-pdf-without-page-numbers
#
pandoc \
 -V geometry:margin=0.6in \
 -V pagestyle=empty \
 1_osm2sqlite.md \
 2_tables.md \
 3_options.md \
 4_mapdrawing.md \
 5_routing.md \
 9_appendix.md \
 -o osm2sqlite.pdf

#
# manpage
# see https://jeromebelleman.gitlab.io/posts/publishing/manpages/
#
rm osm2sqlite.1.gz
pandoc \
 -s -f markdown -t man \
 1_osm2sqlite.md \
 2_tables.md \
 3_options.md \
 4_mapdrawing.md \
 5_routing.md \
 9_appendix.md \
 -o osm2sqlite.1
gzip osm2sqlite.1
