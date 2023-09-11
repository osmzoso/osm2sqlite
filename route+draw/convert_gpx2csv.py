#!/usr/bin/env python
#
#
#
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    print(f'''
    Converts a gpx file into a csv file.
    Output is stdout.
    Usage:
    {sys.argv[0]} GPX_FILE
    ''')
    sys.exit(1)


def read_gpx_file(filename):
    namespace = '{http://www.topografix.com/GPX/1/1}'
    path_coordinates = []
    num_tracks = 0
    tree = ET.parse(filename)
    for trk in tree.findall(namespace + 'trk'):
        num_tracks += 1
        for trkpt in trk.iter(namespace + 'trkpt'):
            lon = float(trkpt.attrib['lon'])
            lat = float(trkpt.attrib['lat'])
            path_coordinates.append((lon, lat))
    return path_coordinates, num_tracks


def write_csv_file(path_coordinates):
    for (lon, lat) in path_coordinates:
        print(str(lon) + ',' + str(lat))


if __name__ == "__main__":
    filename = sys.argv[1]
    path_coordinates, num_tracks = read_gpx_file(filename)
    write_csv_file(path_coordinates)
