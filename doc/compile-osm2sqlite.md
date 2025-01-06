# Compiling osm2sqlite on Linux


## Dynamic binary for Linux

Required packages (Fedora):
```
sqlite-libs
sqlite-devel
libxml2
libxml2-devel
```

The dynamic libs are in the following directory:
```
/usr/lib64/libsqlite3.so.0
/usr/lib64/libxml2.so.2
```

A simple `make` should do the job.

Show shared object dependencies for osm2sqlite: `ldd osm2sqlite`


## Static binaries (32bit and 64bit) for Windows

First the SQLite amalgamation files **sqlite3.c** and **sqlite3.h** must exist
in the directory `./src`, see <https://www.sqlite.org/amalgamation.html>.

Compilation for Windows systems with Linux and crosscompiler MinGW.

### 32 Bit

Required packages (Fedora):
```
mingw32-gcc
mingw32-libxml2
mingw32-libxml2-static
mingw32-zlib
mingw32-zlib-static
mingw32-win-iconv
mingw32-win-iconv-static
```

The static libs are in the following directories:
```
/usr/i686-w64-mingw32/sys-root/mingw/lib/libxml2.a
/usr/i686-w64-mingw32/sys-root/mingw/lib/libwinpthread.a
/usr/i686-w64-mingw32/sys-root/mingw/lib/libz.a
/usr/i686-w64-mingw32/sys-root/mingw/lib/libws2_32.a
/usr/lib/gcc/i686-w64-mingw32/12.2.1/libgcc.a
```

`make win32` should do the job.

### 64 Bit

Required packages (Fedora):
```
mingw64-gcc
mingw64-libxml2
mingw64-libxml2-static
mingw64-zlib
mingw64-zlib-static
mingw64-win-iconv
mingw64-win-iconv-static
mingw64-winpthreads
mingw64-winpthreads-static
```

The static libs are in the following directories:
```
/usr/x86_64-w64-mingw32/sys-root/mingw/lib/libxml2.a
/usr/x86_64-w64-mingw32/sys-root/mingw/lib/libwinpthread.a
/usr/x86_64-w64-mingw32/sys-root/mingw/lib/libz.a
/usr/x86_64-w64-mingw32/sys-root/mingw/lib/libws2_32.a
/usr/lib/gcc/x86_64-w64-mingw32/12.2.1/libgcc.a
```

`make win64` should do the job.
