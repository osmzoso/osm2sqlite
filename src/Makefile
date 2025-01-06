#
CC = gcc
CFLAGS = -Wall -Os -s
INC = -I/usr/include/libxml2

# compile
osm2sqlite: osm2sqlite.c
	$(CC) osm2sqlite.c -lsqlite3 -lxml2 -lm -o osm2sqlite $(CFLAGS) $(INC)

# install
install: osm2sqlite
	install -m755 osm2sqlite /usr/bin

# compile for windows
# The files sqlite3.c and sqlite3.h must be present in this directory
win32:
	i686-w64-mingw32-gcc \
     -static \
     -Os -s \
     -DSQLITE_THREADSAFE=0 -DSQLITE_OMIT_LOAD_EXTENSION -DSQLITE_ENABLE_RTREE \
     -DLIBXML_STATIC \
     -D_FORTIFY_SOURCE=2 \
     osm2sqlite.c \
     sqlite3.c \
     -o osm2sqlite_32bit.exe \
     -I. \
     -I/usr/i686-w64-mingw32/sys-root/mingw/include/libxml2 \
     -L/usr/i686-w64-mingw32/sys-root/mingw/lib \
     -lxml2 -lz -liconv -lpthread -lwinpthread -lws2_32 -lssp -lgcc

win64:
	x86_64-w64-mingw32-gcc \
     -static \
     -Os -s \
     -DSQLITE_THREADSAFE=0 -DSQLITE_OMIT_LOAD_EXTENSION -DSQLITE_ENABLE_RTREE \
     -DLIBXML_STATIC \
     -D_FORTIFY_SOURCE=2 \
     osm2sqlite.c \
     sqlite3.c \
     -o osm2sqlite.exe \
     -I. \
     -I/usr/x86_64-w64-mingw32/sys-root/mingw/include/libxml2 \
     -L/usr/x86_64-w64-mingw32/sys-root/mingw/lib \
     -lxml2 -lz -liconv -lpthread -lwinpthread -lws2_32 -lssp -lgcc

# remove binaries
clean:
	rm -f osm2sqlite
	rm -f osm2sqlite_32bit.exe
	rm -f osm2sqlite.exe
