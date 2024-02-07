#!/usr/bin/env python
"""
Functions to convert CSV to GPX
"""
import sys
import xml.etree.ElementTree as ET


def read_coordinates_csv(filename):
    """Read coordinates from csv file"""
    path_coordinates = []
    with open(filename, mode='r', encoding='utf-8') as fobj:
        for line in fobj:
            columns = line.split(',')
            try:
                lon = float(columns[0])
                lat = float(columns[1])
                ele = float(columns[2])
            except ValueError:
                continue
            path_coordinates.append((lon, lat, ele))
    return path_coordinates


def write_gpx_file(path_coordinates):
    """Write gpx file"""
    print('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>')
    print('<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1"'
          f' creator="osm2sqlite {sys.argv[0]}">')
    print('  <metadata></metadata>')
    print('  <trk>')
    print('    <name>Track 1</name>')
    print('    <extensions>')
    print('    </extensions>')
    print('    <trkseg>')
    for (lon, lat, ele) in path_coordinates:
        print('      <trkpt lat="' + str(lat) + '" lon="' + str(lon) + '">')
        print('        <ele>' + str(ele) + '</ele>')
        print('      </trkpt>')
    print('    </trkseg>')
    print('  </trk>')
    print('</gpx>')


def write_gpx_file_v2():
    """Test Create gpx file with ElementTree"""
    # Create the root element of the GPX file
    gpx = ET.Element("gpx", version="1.1", creator="Your Python Script")
    # Create a waypoint element
    wpt = ET.SubElement(gpx, "wpt", lat="37.7749", lon="-122.4194")  # San Francisco coordinates
    # Add elements for the waypoint
    name = ET.SubElement(wpt, "name")
    name.text = "San Francisco"
    ele = ET.SubElement(wpt, "ele")
    ele.text = "5"  # Elevation in meters
    # Convert the Element object to a formatted string
    gpx_str = ET.tostring(gpx)
    print(gpx_str)
    # Write the GPX string to a file
    with open('example.gpx', 'w', encoding='utf-8') as gpx_file:
        gpx_file.write(gpx_str)


def main():
    "main entry point"
    if len(sys.argv) != 2:
        print('Converts a csv file into a gpx file.\n'
              'Output is stdout.\n'
              'Usage:\n'
              f'{sys.argv[0]} CSV_FILE')
        sys.exit(1)
    filename = sys.argv[1]
    path_coordinates = read_coordinates_csv(filename)
    write_gpx_file(path_coordinates)

if __name__ == "__main__":
    main()
