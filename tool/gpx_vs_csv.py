#!/usr/bin/env python
#
# https://de.wikipedia.org/wiki/GPS_Exchange_Format
#
# https://www.gpsbabel.org/htmldoc-development/The_Formats.html
# https://www.gpsbabel.org/htmldoc-development/fmt_gpx.html
# https://www.topografix.com/gpx.asp
#
# https://www.j-berkemeier.de/ShowGPX.html
#
# Problem Namespaces...
# https://gis.stackexchange.com/questions/228966/how-to-properly-get-coordinates-from-gpx-file-in-python
# https://stackoverflow.com/questions/14853243/parsing-xml-with-namespace-in-python-via-elementtree
# https://docs.python.org/3/library/xml.etree.elementtree.html#parsing-xml-with-namespaces
#
# https://mygeodata.cloud/converter/
#
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    print(f'''
    Converts a gpx file into a csv file and vice versa.
    The format is recognised by the file extension.
    Output is stdout.
    Usage:
    {sys.argv[0]} FILE
    ''')
    sys.exit(1)


def read_gpx_file(filename, namespace='{http://www.topografix.com/GPX/1/1}'):
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


def read_csv_file(filename):
    path_coordinates = []
    fobj = open(filename, "r")
    for line in fobj:
        lonlat = line.split(',')
        try:
            lon = float(lonlat[0])
            lat = float(lonlat[1])
        except:
            continue
        path_coordinates.append((lon, lat))
    fobj.close()
    return path_coordinates


def write_gpx_file(path_coordinates):
    print('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>')
    print('<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1" creator="osm2sqlite">')
    print('<metadata></metadata>')
    print('  <trk>')
    print('    <name>Track 1</name>')
    print('    <extensions>')
    print('    </extensions>')
    print('    <trkseg>')
    for (lon, lat) in path_coordinates:
        print('      <trkpt lat="' + str(lat) + '" lon="' + str(lon) + '">' + '</trkpt>')
    print('    </trkseg>')
    print('  </trk>')
    print('</gpx>')


def write_csv_file(path_coordinates):
    for (lon, lat) in path_coordinates:
        print(str(lon) + ',' + str(lat))


#
# Test Create gpx file with ElementTree
#
def create_gpx_file():
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
    with open("example.gpx", "w") as gpx_file:
        gpx_file.write(gpx_str)


if __name__ == "__main__":
    filename = sys.argv[1]
    if filename.endswith('.gpx'):
        path_coordinates, num_tracks = read_gpx_file(filename)
        if len(path_coordinates) == 0:
            path_coordinates, num_tracks = read_gpx_file(filename, '')
        write_csv_file(path_coordinates)
    if filename.endswith('.csv'):
        path_coordinates = read_csv_file(filename)
        write_gpx_file(path_coordinates)
