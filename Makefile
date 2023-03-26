#
# compile osm2sqlite.c
#
CC = gcc
CFLAGS = -Wall -Os -s
DSQLITE = -DSQLITE_THREADSAFE=0 -DSQLITE_OMIT_LOAD_EXTENSION -DSQLITE_ENABLE_RTREE
INC = -I/usr/include/libxml2

# compile with the amalgamation
#osm2sqlite: osm2sqlite.c sqlite3.c
#	$(CC) osm2sqlite.c sqlite3.c -lxml2 -o osm2sqlite $(CFLAGS) $(DSQLITE) $(INC)

# compile
osm2sqlite: osm2sqlite.c
	$(CC) osm2sqlite.c -lsqlite3 -lxml2 -o osm2sqlite $(CFLAGS) $(INC)

# install
install: osm2sqlite
	install -m755 osm2sqlite /usr/bin

