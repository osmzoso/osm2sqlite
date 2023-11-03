#!/bin/bash
#
# PDF
# see https://tex.stackexchange.com/questions/138651/pandoc-markdown-to-pdf-without-page-numbers
# see https://stackoverflow.com/questions/22601053/pagebreak-in-markdown-while-creating-pdf
#
pandoc \
 -V geometry:margin=0.6in \
 -V pagestyle=empty \
 1_osm2sqlite.md \
 2_tables.md \
 3_options.md \
 4_mapdrawing.md \
 5_routing.md \
 6_check_data.md \
 7_tools.md \
 8_test.md \
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
 6_check_data.md \
 7_tools.md \
 8_test.md \
 9_appendix.md \
 -o osm2sqlite.1
gzip osm2sqlite.1
