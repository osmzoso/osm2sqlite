#!/bin/bash
#
# https://pandoc.org/MANUAL.html
# see https://tex.stackexchange.com/questions/138651/pandoc-markdown-to-pdf-without-page-numbers
# see https://stackoverflow.com/questions/22601053/pagebreak-in-markdown-while-creating-pdf
# see https://jeromebelleman.gitlab.io/posts/publishing/manpages/
#

#
# PDF
#
pandoc \
 -V geometry:margin=0.6in \
 osm2sqlite.md \
 --pdf-engine=xelatex \
 --toc \
 -o osm2sqlite.pdf

#
# HTML
#
pandoc \
 --standalone \
 --embed-resources \
 --metadata title="osm2sqlite" \
 --toc \
 --css=custom.css \
 osm2sqlite.md \
 -o osm2sqlite.html

#
# manpage
#
rm -f osm2sqlite.1.gz
pandoc \
 -s -f markdown -t man \
 osm2sqlite.md \
 -o osm2sqlite.1
gzip osm2sqlite.1
