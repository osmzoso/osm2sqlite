#
# Compile osm2sqlite.c for Linux and Windows
#

#
# Dynamic binary for Linux
#
gcc osm2sqlite.c -lsqlite3 -lxml2 -o osm2sqlite -Wall -O2 -s -I/usr/include/libxml2
ldd osm2sqlite

#
# Static binary (32 Bit) for Windows
#

# Crosscompiler MinGW, installed packages (Fedora 37):
#  i686-w64-mingw32-gcc.x86_64
#  mingw32-libxml2.noarch
#  mingw32-libxml2-static.noarch
#  mingw32-zlib.noarch
#  mingw32-zlib-static.noarch
#  mingw32-win-iconv.noarch
#  mingw32-win-iconv-static.noarch

#dnf repoquery -l mingw32-libxml2.noarch
#dnf repoquery -l mingw32-libxml2-static.noarch
#dnf repoquery -l mingw32-zlib.noarch
#dnf repoquery -l mingw32-zlib-static.noarch
#dnf repoquery -l mingw32-win-iconv.noarch
#dnf repoquery -l mingw32-win-iconv-static.noarch

#
# The SQLite amalgamation files sqlite3.c and sqlite3.h must exist in this directory
# see https://www.sqlite.org/amalgamation.html
#
if [[ -f "sqlite3.c" && -f "sqlite3.h"  ]]; then
  echo "SQLite amalgamation files sqlite3.c and sqlite3.h exists -> OK"
else
  echo "SQLite amalgamation files sqlite3.c and sqlite3.h missing -> abort"
  exit
fi

#
# create sqlite3.dll (at least it compiles, not tested under windows)
# see https://sqlite.org/forum/forumpost/5cc24065c4d9029d
#
#i686-w64-mingw32-gcc -shared -static-libgcc sqlite3.c -o sqlite3.dll

#
# /usr/i686-w64-mingw32/sys-root/mingw/lib/libxml2.a
# /usr/i686-w64-mingw32/sys-root/mingw/lib/libwinpthread.a
# /usr/i686-w64-mingw32/sys-root/mingw/lib/libz.a
# /usr/i686-w64-mingw32/sys-root/mingw/lib/libws2_32.a
# /usr/lib/gcc/i686-w64-mingw32/12.2.1/libgcc.a
# nm libxml2.a
#i686-w64-mingw32-nm /usr/i686-w64-mingw32/sys-root/mingw/lib/libxml2.a
#
i686-w64-mingw32-gcc \
 -static \
 -O2 \
 -DSQLITE_THREADSAFE=0 -DSQLITE_OMIT_LOAD_EXTENSION -DSQLITE_ENABLE_RTREE \
 -DLIBXML_STATIC \
 -D_FORTIFY_SOURCE=2 \
 osm2sqlite.c \
 sqlite3.c \
 -o osm2sqlite.exe \
 -I. \
 -I/usr/i686-w64-mingw32/sys-root/mingw/include/libxml2 \
 -L/usr/i686-w64-mingw32/sys-root/mingw/lib \
 -L/usr/lib/gcc/i686-w64-mingw32/12.2.1 \
 -lxml2 -lz -liconv -lpthread -lwinpthread -lws2_32 -lssp -lgcc

# Maybe some helpful links...
# http://xmlsoft.org/html/
# https://github.com/msys2/MINGW-packages/issues/4528
# https://stackoverflow.com/questions/3283021/compile-a-standalone-static-executable
# https://stackoverflow.com/questions/14842268/how-to-create-static-binary-which-runs-on-every-distro
# https://stackoverflow.com/questions/48149507/linking-static-libraries-instead-of-shared-using-g
# https://stackoverflow.com/questions/15852677/static-and-dynamic-shared-linking-with-mingw
# https://sourceware.org/binutils/docs/ld/WIN32.html
# https://stackoverflow.com/questions/725472/static-link-of-shared-library-function-in-gcc
# gcc -o executablename objectname.o -Wl,-Bstatic -l:libnamespec.so
# https://helloacm.com/how-to-link-static-library-in-cc-using-gcc-compiler/
# https://stackoverflow.com/questions/10137937/merge-dll-into-exe
# https://sourceforge.net/p/mingw-w64/support-requests/148/
# xml2-config script:
# xml2-config  --libs    -> output:    -lxml2 -lz -llzma -lm
# xml2-config  --cflags  -> output:    -I/usr/include/libxml2

