#
# Makefile osm2sqlite
#
# Compiler:
CC = gcc
CFLAGS = -ansi -Wall -Os -s
CDSQLITE = -DSQLITE_THREADSAFE=0 -DSQLITE_OMIT_LOAD_EXTENSION

# compile
osm2sqlite: osm2sqlite.c
	$(CC) osm2sqlite.c sqlite3.c -lxml2 -o osm2sqlite $(CFLAGS) $(CDSQLITE)

# install
install: osm2sqlite
	install -m 644 osm2sqlite /usr/bin

