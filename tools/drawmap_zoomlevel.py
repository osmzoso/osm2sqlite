#!/usr/bin/env python
"""
Show zoomlevel
"""
import drawmap


def deg_dec(degrees, minutes, seconds):
    "Converts degrees minutes seconds to degrees decimal"
    return (((seconds / 60) + minutes) / 60) + degrees


def deg_min_sec(degrees_decimal):
    "Converts degrees decimal to degrees minutes seconds"
    degrees = int(degrees_decimal)
    x = (degrees_decimal - degrees) * 60
    minutes = int(x)
    seconds = (x - minutes) * 60
    return degrees, minutes, seconds


def show_limit_web_mercator():
    "Show Limits Web Mercator"
    print('\n' + '*' * 60)
    print('Limits Web Mercator:')
    print('85°3\'4.0636\"  ->', deg_dec(85, 3, 4.0636))
    print('85.05112878  ->', deg_min_sec(85.05112878))
    print(drawmap.spherical_to_mercator(180, 85.05112878))
    print(drawmap.spherical_to_mercator(-180, -85.05112878))
    print(drawmap.mercator_to_spherical(20037508.343, 20037508.343))
    print(drawmap.mercator_to_spherical(-20037508.343, -20037508.343))


def show_zoomlevel():
    "Show zoomlevel size"
    print('\n' + '*' * 60)
    print('zoomlevel   size_world_map_in_pixel     meter_per_pixel')
    for zoomlevel in range(21):
        pixel_world_map, meters_pixel = drawmap.size_world_map(zoomlevel)
        print(f'{zoomlevel:5}     '
              f'{pixel_world_map:>12} x {pixel_world_map:<12} '
              f'{meters_pixel:>14.2f}')


if __name__ == '__main__':
    show_limit_web_mercator()
    show_zoomlevel()
