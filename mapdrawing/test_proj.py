#!/usr/bin/env python
#
# https://gis.stackexchange.com/questions/120636/math-formula-for-transforming-from-epsg4326-to-epsg3857
#
import math

# POINT(7.811239 48.016063)
# POINT(869543.114549 6109527.511962)
# POINT(0 0)
# POINT(111319.490793 111325.142866)
# POINT(20037508.342789 0)
# POINT(-20037508.342789 0)


def wgs84_to_webmercator(lon, lat):
    """
    Transform WGS84 (EPSG:4326) to Web Mercator (EPSG:3857)
    Returns x, y
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
    Returns lon, lat
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


#
# Test
#
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
