#!/usr/bin/env python
"""
Contains functions for converting coordinates

1. Systems
WGS84 (lon, lat)    - used in OpenStreetMap
Web Mercator (x, y) - Spherical projection
Pixel coordinates   - Bitmap coordinates


2. Restrictions Web Mercator

Polar areas with abs(latitude) bigger then 85.05112878 are clipped off.


3. Compare WGS84 - Web Mercator

                                           ^       right upper corner:
                                           |       lon: +180°0'0" (E), lat: 85°3'4.064" (N)
                                           |       x: 20037508.34, y: 20037508.34
                                           |
-------------------------------------------0------------------------------------------>
                                           |
left down corner:                          |
lon: -180°0'0" (W), lat: -85°3'4.064" (S)  |
x: -20037508.34,  y: -20037508.34          |

"""
#
# Formulas:
# https://gis.stackexchange.com/questions/120636/math-formula-for-transforming-from-epsg4326-to-epsg3857
# http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
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
    Return degrees, minutes, seconds of degrees decimal
    """
    degrees = int(degrees_decimal)
    x = (degrees_decimal - degrees) * 60
    minutes = int(x)
    seconds = (x - minutes) * 60
    return degrees, minutes, seconds


def zoom_sizes(zoomlevel):
    """
    Calculates sizes for given zoom level
    TODO
    meters_pixel : Resolution (meters/pixel) measured at Equator"
    """
    tile_size = 256     # tile 256px x 256px
    number_tiles = 4**zoomlevel
    pixel_world_map = int(tile_size * math.sqrt(number_tiles))
    degrees_pixel_x = 360 / pixel_world_map
    degrees_pixel_y = 180 / pixel_world_map
    const_webmercator = 20037508.342789244
    meters_pixel = const_webmercator * 2 / pixel_world_map
    return pixel_world_map, degrees_pixel_x, degrees_pixel_y, meters_pixel


def webmercator_to_pixel(x, y, pixel_world_map):
    """
    Transform Web Mercator to pixel coordinates
    Returns x_px, y_px
    """
    pixel_world_map -= 1
    const_webmercator = 20037508.342789244
    x += const_webmercator  # move origin to avoid negativ coordiantes
    y += const_webmercator
    x_px = int(round((x * pixel_world_map) / (const_webmercator * 2), 0))
    y_px = int(round((y * pixel_world_map) / (const_webmercator * 2), 0))
    return x_px, y_px


def pixel_to_webmercator(x_px, y_px, pixel_world_map):
    """
    Transform pixel coordinates to  Web Mercator
    Returns x, y
    """
    const_webmercator = 20037508.342789244
    x_px -= pixel_world_map / 2
    y_px -= pixel_world_map / 2
    x = (x_px / pixel_world_map) * (const_webmercator * 2)
    y = (y_px / pixel_world_map) * (const_webmercator * 2)
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


if __name__ == "__main__":
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

    Spherical Mercator


    ''')
    print('85°3\'4.064\"  ->', degree_minutes_to_decimal(85, 3, 4.064))
    print('85.05112878  ->', degree_decimal_to_minutes(85.05112878))
    print(wgs84_to_webmercator(180, 85.05112878))
    print(wgs84_to_webmercator(-180, -85.05112878))
    print(webmercator_to_wgs84(20037508.34, 20037508.34))
    print(webmercator_to_wgs84(-20037508.34, -20037508.34))

    print('''
    ********************************************************************************
    Test 3

    Zoomlevel

    ''')

    print('zoomlevel',
          '  pixel_world_map',
          '         degrees_pixel_x',
          '         degrees_pixel_y',
          '             meters_pixel_x')
    for zoomlevel in range(19):
        pixel_world_map, degrees_pixel_x, degrees_pixel_y, meters_pixel = zoom_sizes(zoomlevel)
        print(f'{zoomlevel:9}',
              f'{pixel_world_map:17}',
              f'{degrees_pixel_x:24.16f}',
              f'{degrees_pixel_y:24.16f}',
              f'{meters_pixel:27.16f}')

    print('''
    ********************************************************************************
    Test 4

    Transform WGS84 to pixel coordinates
    ''')
    def test_wgs84_to_pixel(lon, lat, pixel_world_map):
        x_px, y_px = wgs84_to_pixel(lon, lat, pixel_world_map)
        print(f'{pixel_world_map:12}',
              f'{lon:12.7f}',
              f'{lat:12.7f}',
              f'{x_px:13}',
              f'{y_px:13}')

    print('zoomlevel_px       lon           lat      x_px         y_px')
    for zoomlevel in range(19):
        pixel_world_map, degrees_pixel_x, degrees_pixel_y, meters_pixel = zoom_sizes(zoomlevel)
        print(f'zoomlevel {zoomlevel} (world map {pixel_world_map}px x {pixel_world_map}px):')
        test_wgs84_to_pixel( 180,  85.05112878,   pixel_world_map)
        test_wgs84_to_pixel(  90,  85.05112878/2, pixel_world_map)
        test_wgs84_to_pixel(   0,              0, pixel_world_map)
        test_wgs84_to_pixel( -90, -85.05112878/2, pixel_world_map)
        test_wgs84_to_pixel(-180, -85.05112878,   pixel_world_map)

    print('''
    ********************************************************************************
    Test 5

    Estimate size of boundingbox in www.openstreetmap.org
    ''')
    lon1 = 7.7908301
    lat1 = 47.9748670
    lon2 = 7.8094983
    lat2 = 47.9832267
    print('boundingbox:', lon1, lat1, lon2, lat2)
    print('''
    This boundingbox leads to the following pixel sizes (roughly estimated):
    Zoomlevel 13: 115 x 80 pixel
    Zoomlevel 14: 222 x 152 pixel
    Zoomlevel 15: 440 x 298 pixel
    Zoomlevel 16: 875 x 586 pixel
    ''')

    print('''
    ********************************************************************************
    Test 6

    Calculate boundingbox in pixel
    ''')
    lon1 = 7.7908301
    lat1 = 47.9748670
    lon2 = 7.8094983
    lat2 = 47.9832267
    print('boundingbox:', lon1, lat1, lon2, lat2)
    for zoomlevel in range(13, 17):
        pixel_world_map, degrees_pixel_x, degrees_pixel_y, meters_pixel = zoom_sizes(zoomlevel)
        x1_px, y1_px = wgs84_to_pixel(lon1, lat1, pixel_world_map)
        x2_px, y2_px = wgs84_to_pixel(lon2, lat2, pixel_world_map)
        size_x_px = x2_px - x1_px
        size_y_px = y2_px - y1_px
        print(f'Zoomlevel {zoomlevel}: {size_x_px} x {size_y_px} pixel')

    print('''
    ********************************************************************************
    Test 7

    Check transform Web Mercator to pixel and vice versa
    ''')

    lon = 7.1
    lat = 48.0
    zoomlevel = 17
    #
    pixel_world_map, degrees_pixel_x, degrees_pixel_y, meters_pixel = zoom_sizes(zoomlevel)
    print(f'lon: {lon}, lat: {lat}, zoomlevel: {zoomlevel}')
    x, y = wgs84_to_webmercator(lon, lat)
    print(f' -> x: {x}, y: {y}')
    x_px, y_px = webmercator_to_pixel(x, y, pixel_world_map)
    print(f' -> x_px: {x_px}, y_px: {y_px}')
    x, y = pixel_to_webmercator(x_px, y_px, pixel_world_map)
    print(f' -> x: {x}, y: {y}')
    lon, lat = webmercator_to_wgs84(x, y)
    print(f' -> lon: {lon}, lat: {lat}')

    print('''
    ********************************************************************************
    Test 8

    Check transform WGS84 to pixel and vice versa
    ''')

    lon = 7.1
    lat = 48.0
    zoomlevel = 17
    #
    pixel_world_map, degrees_pixel_x, degrees_pixel_y, meters_pixel = zoom_sizes(zoomlevel)
    print(f'lon: {lon}, lat: {lat}, zoomlevel: {zoomlevel}')
    x_px, y_px = wgs84_to_pixel(lon, lat, pixel_world_map)
    print(f' -> x_px: {x_px}, y_px: {y_px}')
    lon, lat = pixel_to_wgs84(x_px, y_px, pixel_world_map)
    print(f' -> lon: {lon}, lat: {lat}')

    # https://www.w3schools.com/graphics/svg_intro.asp
    # https://de.wikipedia.org/wiki/Scalable_Vector_Graphics

