#!/usr/bin/env python
"""
Test5: Modul proj
"""
import sys
sys.path.append('../src_py')
import proj
import random
import sqlite3

SPATIALITE = "/usr/lib64/mod_spatialite.so"

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
db.execute("SELECT load_extension(?)", [SPATIALITE])
db.execute("SELECT InitSpatialMetadata(1)")

# round numbers to x decimal places
decimal_places = 3

#
#
#
print(f'Check conversion spherical coordinates into planar coordinates (decimal places: {decimal_places})')
number_correct = 0
number_wrong = 0
for i in range(10000):
    lon = random.uniform(-180.00, 180.00)
    lat = random.uniform(-90.00, 90.00)
    #
    x_spatialite, y_spatialite = db.execute(f'''
    SELECT X( Transform( MakePoint({lon}, {lat}, 4326), 3857) ),
           Y( Transform( MakePoint({lon}, {lat}, 4326), 3857) )
    ''').fetchone()
    x_spatialite = round(x_spatialite, decimal_places)
    y_spatialite = round(y_spatialite, decimal_places)
    #
    x_proj, y_proj = proj.wgs84_to_webmercator(lon, lat)
    x_proj = round(x_proj, decimal_places)
    y_proj = round(y_proj, decimal_places)
    #
    if x_spatialite == x_proj and y_spatialite == y_proj:
        number_correct += 1
    else:
        number_wrong += 1
        print('lon:', lon, 'lat:', lat)
        print(' -> Spatialite', x_spatialite, y_spatialite)
        print(' -> Proj      ', x_proj, y_proj)

print('number_correct :', number_correct)
print('number_wrong   :', number_wrong)

#
#
#
print(f'Check conversion planar coordinates into spherical coordinates (decimal places: {decimal_places})')
number_correct = 0
number_wrong = 0
for i in range(10000):
    x = random.uniform(-20037508.34, 20037508.34)
    y = random.uniform(-20037508.34, 20037508.34)
    #
    lon_spatialite, lat_spatialite = db.execute(f'''
    SELECT X( Transform( MakePoint({x}, {y}, 3857), 4326) ),
           Y( Transform( MakePoint({x}, {y}, 3857), 4326) )
    ''').fetchone()
    lon_spatialite = round(lon_spatialite, decimal_places)
    lat_spatialite = round(lat_spatialite, decimal_places)
    #
    lon_proj, lat_proj = proj.webmercator_to_wgs84(x, y)
    lon_proj = round(lon_proj, decimal_places)
    lat_proj = round(lat_proj, decimal_places)
    #
    if lon_spatialite == lon_proj and lat_spatialite == lat_proj:
        number_correct += 1
    else:
        number_wrong += 1
        print('x:', x, 'y:', y)
        print(' -> Spatialite', lon_spatialite, lat_spatialite)
        print(' -> Proj      ', lon_proj, lat_proj)

print('number_correct :', number_correct)
print('number_wrong   :', number_wrong)
