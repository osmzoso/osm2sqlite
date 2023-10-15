#!/usr/bin/env python
#
# https://til.simonwillison.net/spatialite/minimal-spatialite-database-in-python
#
# libspatialite must be installed
# Fedora: sudo dnf install libspatialite.x86_64
#
import sqlite3

SPATIALITE = "/usr/lib64/mod_spatialite.so"

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
db.execute("SELECT load_extension(?)", [SPATIALITE])
db.execute("SELECT InitSpatialMetadata(1)")
db.execute("CREATE TABLE places_spatialite (id integer primary key, name text)")
db.execute(
    "SELECT AddGeometryColumn('places_spatialite', 'geometry', 4326, 'POINT', 'XY');"
)
# Then to add a spatial index:
db.execute(
    "SELECT CreateSpatialIndex('places_spatialite', 'geometry');"
)


print(db.execute('SELECT spatialite_version()').fetchone()[0])

print(db.execute('SELECT AsText( MakePoint(7.8112387, 48.0160627, 4326) )').fetchone()[0])

# WGS84 EPSG:4326 -> Web Mercator EPSG:3857
print(db.execute('SELECT AsText( Transform( MakePoint(7.8112387, 48.0160627, 4326), 3857) )').fetchone()[0])
print(db.execute('SELECT AsText( Transform( MakePoint(0.0000000,  0.0000000, 4326), 3857) )').fetchone()[0])
print(db.execute('SELECT AsText( Transform( MakePoint(1.0000000,  1.0000000, 4326), 3857) )').fetchone()[0])
print(db.execute('SELECT AsText( Transform( MakePoint(180.0000000,  0.0000000, 4326), 3857) )').fetchone()[0])
print(db.execute('SELECT AsText( Transform( MakePoint(-180.0000000,  0.0000000, 4326), 3857) )').fetchone()[0])

# distance Freiburg-Konstanz (ellipsoid, slower but precise)
print(db.execute('SELECT Distance( MakePoint(7.8118613,48.015983), MakePoint(9.1808754,47.6716953), 1 )').fetchone()[0])
# distance Freiburg-Konstanz (great circle, faster but less precise)
print(db.execute('SELECT Distance( MakePoint(7.8118613,48.015983), MakePoint(9.1808754,47.6716953), 0 )').fetchone()[0])
