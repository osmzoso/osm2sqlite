#!/usr/bin/env python
"""
Contains functions for converting coordinates to draw a map
Spherical coordinates : WGS84 (EPSG:4326)
Planar coordinates    : Web Mercator (EPSG:3857)
"""
import math


def wgs84_to_webmercator(lon, lat):
    "Converts spherical coordinates into planar coordinates"
    r = 6378137.0
    x = r * math.radians(lon)
    y = r * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y


def webmercator_to_wgs84(x, y):
    "Converts planar coordinates into spherical coordinates"
    r = 6378137.0
    lon = math.degrees(x / r)
    lat = math.degrees(2 * math.atan(math.exp(y / r)) - math.pi / 2.0)
    return lon, lat


def dms_to_decimal(degrees, minutes, seconds):
    "Converts degrees minutes seconds to degrees decimal"
    return (((seconds / 60) + minutes) / 60) + degrees


def decimal_to_dms(degrees_decimal):
    "Converts degrees decimal to degrees minutes seconds"
    degrees = int(degrees_decimal)
    x = (degrees_decimal - degrees) * 60
    minutes = int(x)
    seconds = (x - minutes) * 60
    return degrees, minutes, seconds


def size_world_map(zoomlevel):
    """
    Calculates the size of the world map for a zoom level
    Return pixel_world_map, meters_pixel
    (resolution (meters/pixel) measured at Equator)"
    """
    tile_size = 256     # tile 256px x 256px
    number_tiles = 4**zoomlevel
    pixel_world_map = int(tile_size * math.sqrt(number_tiles))
    webmercator = 20037508.342789244
    meters_pixel = webmercator * 2 / pixel_world_map
    return pixel_world_map, meters_pixel


def webmercator_to_pixel(x, y, pixel_world_map):
    """
    Transform Web Mercator to pixel coordinates
    Returns x_px, y_px
    """
    pixel_world_map -= 1
    webmercator = 20037508.342789244
    x += webmercator  # move origin to avoid negativ coordinates
    y += webmercator
    x_px = int(round((x * pixel_world_map) / (webmercator * 2), 0))
    y_px = int(round((y * pixel_world_map) / (webmercator * 2), 0))
    return x_px, y_px


def pixel_to_webmercator(x_px, y_px, pixel_world_map):
    """
    Transform pixel coordinates to Web Mercator
    Returns x, y
    """
    webmercator = 20037508.342789244
    x_px -= pixel_world_map / 2
    y_px -= pixel_world_map / 2
    x = (x_px / pixel_world_map) * (webmercator * 2)
    y = (y_px / pixel_world_map) * (webmercator * 2)
    return x, y


def wgs84_to_pixel(lon, lat, pixel_world_map):
    """
    Transform WGS84 to pixel coordinates
    Returns x_px, y_px
    """
    x, y = wgs84_to_webmercator(lon, lat)
    x_px, y_px = webmercator_to_pixel(x, y, pixel_world_map)
    return x_px, y_px


def pixel_to_wgs84(x_px, y_px, pixel_world_map):
    """
    Transform pixel coordinates to WGS84
    Returns lon, lat
    """
    x, y = pixel_to_webmercator(x_px, y_px, pixel_world_map)
    lon, lat = webmercator_to_wgs84(x, y)
    return lon, lat


def pixel_boundingbox(lon, lat, pixel_world_map, size_x_px, size_y_px):
    """
    Calculate pixel boundingbox
    size_x_px, size_y_px: map size in pixel
    Return min_x_px, min_y_px, max_x_px, max_y_px
    """
    x_px, y_px = wgs84_to_pixel(lon, lat, pixel_world_map)
    min_x_px = x_px - int(size_x_px / 2)
    min_y_px = y_px - int(size_y_px / 2)
    max_x_px = x_px + int(size_x_px / 2)
    max_y_px = y_px + int(size_y_px / 2)
    return min_x_px, min_y_px, max_x_px, max_y_px


def test1():
    "Check Limit Web Mercator"
    print('\n' + '*' * 60)
    print('85°3\'4.0636\"  ->', dms_to_decimal(85, 3, 4.0636))
    print('85.05112878  ->', decimal_to_dms(85.05112878))
    print(wgs84_to_webmercator(180, 85.05112878))
    print(wgs84_to_webmercator(-180, -85.05112878))
    print(webmercator_to_wgs84(20037508.343, 20037508.343))
    print(webmercator_to_wgs84(-20037508.343, -20037508.343))


def test2():
    "Show zoomlevel size"
    print('\n' + '*' * 60)
    print('zoomlevel   size_world_map_in_pixel     meter_per_pixel')
    for zoomlevel in range(20):
        pixel_world_map, meters_pixel = size_world_map(zoomlevel)
        print(f'{zoomlevel:5}     '
              f'{pixel_world_map:>12} x {pixel_world_map:<12} '
              f'{meters_pixel:^20.2f}')


if __name__ == "__main__":
    test1()
    test2()
