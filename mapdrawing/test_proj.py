#!/usr/bin/env python
#
# https://gis.stackexchange.com/questions/120636/math-formula-for-transforming-from-epsg4326-to-epsg3857
#
import math

def wgs84_to_webmercator(lon, lat):
    """
    Transform WGS84 (EPSG:4326) to Web Mercator (EPSG:3857)
    Returns x, y (meters)
    """
    a = 6378137.0
    # E = x = a * λ
    # N = y = a * ln[tan(π/4 + φ/2)]
    lambda_ = lon / 180 * math.pi
    phi_ = lat / 180 * math.pi
    x = a * lambda_
    y = a * math.log(math.tan(math.pi / 4 + phi_ / 2))
    return x, y


def webmercator_to_wgs84(x, y):
    """
    Transform Web Mercator (EPSG:3857) to WGS84 (EPSG:4326)
    Returns lon, lat (decimal degrees)
    """
    a = 6378137.0
    # D = -N / a
    # φ = π / 2 – 2 atan(e ^ D)
    # λ = E / a
    d = -1 * y / a
    phi_ = math.pi / 2 - 2 * math.atan(math.exp(d))
    lambda_ = x / a
    lat = phi_ / math.pi * 180
    lon = lambda_ / math.pi * 180
    return lon, lat


def degree_minutes_to_decimal(degrees, minutes, seconds):
    """
    Convert degrees minutes seconds to decimal degrees
    """
    return (((seconds / 60) + minutes) / 60) + degrees


def degree_decimal_to_minutes(degrees_decimal):
    """
    Convert degrees decimal to degrees minutes seconds
    """
    degrees = int(degrees_decimal)
    x = (degrees_decimal - degrees) * 60
    minutes = int(x)
    seconds = (x - minutes) * 60
    return degrees, minutes, seconds


print('''
********************************************************************************
Test 1
''')
print("WGS84 to Web Mercator:")
x, y = wgs84_to_webmercator(180, 0)
print(x, y)
x, y = wgs84_to_webmercator(1, 1)
print(x, y)
#
print("Web Mercator to WGS84:")
lon, lat = webmercator_to_wgs84(111319.49079327357, 111325.14286638486)
print(lon, lat)
lon, lat = webmercator_to_wgs84(20037508.342789244, -7.081154551613622e-10)
print(lon, lat)

print('''
********************************************************************************
Test 2
''')
lon1 = 7.7908301
lat1 = 47.9748670
lon2 = 7.8094983
lat2 = 47.9832267
print('boundingbox:', lon1, lat1, lon2, lat2)
x1, y1 = wgs84_to_webmercator(lon1, lat1)
x2, y2 = wgs84_to_webmercator(lon2, lat2)
print('webmercator x2-x1:', x2-x1)
print('webmercator y2-y1:', y2-y1)
print('''
This boundingbox leads to the following pixel sizes (roughly estimated):
Zoomlevel 13: 115 x 80 pixel
Zoomlevel 14: 222 x 152 pixel
Zoomlevel 15: 440 x 298 pixel
Zoomlevel 16: 875 x 586 pixel
''')

print('''
********************************************************************************
Test 3

Spherical Mercator
see http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/

Polar areas with abs(latitude) bigger then 85.05112878 are clipped off.

right upper corner:
lon: +180° (E)   lat: 85°3'4.064" (N)
-> x: 20037508.34  y: 20037508.34

left down corner:
lon: -180° (W)   lat: -85°3'4.064" (S)
-> x: -20037508.34  y: -20037508.34


''')
print('85°3\'4.064\"  ->', degree_minutes_to_decimal(85, 3, 4.064))
print('85.05112878  ->', degree_decimal_to_minutes(85.05112878))
print(wgs84_to_webmercator(180, 85.05112878))
print(wgs84_to_webmercator(-180, -85.05112878))
print(webmercator_to_wgs84(20037508.34, 20037508.34))
print(webmercator_to_wgs84(-20037508.34, -20037508.34))

