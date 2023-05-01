#
CC = gcc
CFLAGS = -Wall -Os -s
INC = -I/usr/include/libxml2

# compile
osm2sqlite: osm2sqlite.c
	$(CC) osm2sqlite.c -lsqlite3 -lxml2 -o osm2sqlite $(CFLAGS) $(INC)

# install
install: osm2sqlite
	install -m755 osm2sqlite /usr/bin

