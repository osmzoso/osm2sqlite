#!/usr/bin/env python
"""
Functions to convert GPX to CSV 
"""
import sys
import xml.etree.ElementTree as ET


def read_gpx_file(filename):
    """Read gpx file into list"""
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


def print_csv_file(path_coordinates):
    """Print list in csv format"""
    for (lon, lat) in path_coordinates:
        print(str(lon) + ',' + str(lat))


def main():
    """entry point"""
    if len(sys.argv) != 2:
        print('Converts a gpx file into a csv file.\n'
              'Output is stdout.\n'
              'Usage:\n'
              f'{sys.argv[0]} GPX_FILE')
        sys.exit(1)
    filename = sys.argv[1]
    path_coordinates, num_tracks = read_gpx_file(filename)
    print_csv_file(path_coordinates)


if __name__ == "__main__":
    main()
