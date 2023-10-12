#
# Compile osm2sqlite.c for Linux and Windows
#

#
# Dynamic binary for Linux
#
# Required packages (Fedora 37):
#
# sqlite-libs.x86_64
# sqlite-devel.x86_64
# libxml2.x86_64
# libxml2-devel.x86_64
#
# The dynamic libs are in the following directory:
#
# /usr/lib64/libsqlite3.so.0
# /usr/lib64/libxml2.so.2
#
gcc osm2sqlite.c -lsqlite3 -lxml2 -lm -o osm2sqlite -Wall -Os -s -I/usr/include/libxml2
# show shared object dependencies for osm2sqlite
ldd osm2sqlite

#
# Static binaries (32bit and 64bit) for Windows
#

# First the SQLite amalgamation files sqlite3.c and sqlite3.h must exist in this directory
# see https://www.sqlite.org/amalgamation.html
if [[ -f "sqlite3.c" && -f "sqlite3.h"  ]]; then
  echo "build binaries for Windows..."
else
  echo "SQLite amalgamation files sqlite3.c and sqlite3.h missing -> abort"
  exit
fi

#
# Compilation for Windows systems with Linux and crosscompiler MinGW
#

#
# 32 Bit
#
# Required packages (Fedora 37):
#
# mingw32-gcc.x86_64
# mingw32-libxml2.noarch
# mingw32-libxml2-static.noarch
# mingw32-zlib.noarch
# mingw32-zlib-static.noarch
# mingw32-win-iconv.noarch
# mingw32-win-iconv-static.noarch
#
# The static libs are in the following directories:
#
# /usr/i686-w64-mingw32/sys-root/mingw/lib/libxml2.a
# /usr/i686-w64-mingw32/sys-root/mingw/lib/libwinpthread.a
# /usr/i686-w64-mingw32/sys-root/mingw/lib/libz.a
# /usr/i686-w64-mingw32/sys-root/mingw/lib/libws2_32.a
# /usr/lib/gcc/i686-w64-mingw32/12.2.1/libgcc.a
#
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
 -L/usr/lib/gcc/i686-w64-mingw32/12.2.1 \
 -lxml2 -lz -liconv -lpthread -lwinpthread -lws2_32 -lssp -lgcc

#
# 64 Bit
#
# Required packages (Fedora 37):
#
# mingw64-gcc.x86_64
# mingw64-libxml2.noarch
# mingw64-libxml2-static.noarch
# mingw64-zlib.noarch
# mingw64-zlib-static.noarch
# mingw64-win-iconv.noarch
# mingw64-win-iconv-static.noarch
# mingw64-winpthreads.noarch
# mingw64-winpthreads-static.noarch
#
# The static libs are in the following directories:
#
# /usr/x86_64-w64-mingw32/sys-root/mingw/lib/libxml2.a
# /usr/x86_64-w64-mingw32/sys-root/mingw/lib/libwinpthread.a
# /usr/x86_64-w64-mingw32/sys-root/mingw/lib/libz.a
# /usr/x86_64-w64-mingw32/sys-root/mingw/lib/libws2_32.a
# /usr/lib/gcc/x86_64-w64-mingw32/12.2.1/libgcc.a
#
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
 -L/usr/lib/gcc/x86_64-w64-mingw32/12.2.1 \
 -lxml2 -lz -liconv -lpthread -lwinpthread -lws2_32 -lssp -lgcc

