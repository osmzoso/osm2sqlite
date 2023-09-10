#!/usr/bin/env python
#
#
#
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    print(f'''
    Converts a csv file into a gpx file.
    Output is stdout.
    Usage:
    {sys.argv[0]} CSV_FILE
    ''')
    sys.exit(1)


def read_csv_file(filename):
    path_coordinates = []
    fobj = open(filename, "r")
    for line in fobj:
        lonlat = line.split(',')
        try:
            lon = float(lonlat[0])
            lat = float(lonlat[1])
        except ValueError:
            continue
        path_coordinates.append((lon, lat))
    fobj.close()
    return path_coordinates


def write_gpx_file(path_coordinates):
    print('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>')
    print(f'<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1" creator="osm2sqlite {sys.argv[0]}">')
    print('  <metadata></metadata>')
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


#
# Test Create gpx file with ElementTree
#
def write_gpx_file_v2():
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
    path_coordinates = read_csv_file(filename)
    write_gpx_file(path_coordinates)

#
# GPX XML structure
#
# 0: gpx [creator, version, {http://www.w3.org/2001/XMLSchema-instance}schemaLocation]
#     1: metadata [-]
#         2: link [href]
#             3: text [-]
#         2: time [-]
#         2: bounds [maxlat, maxlon, minlat, minlon]
#     1: wpt [lat, lon]
#         2: ele [-]
#         2: name [-]
#         2: cmt [-]
#         2: desc [-]
#         2: sym [-]
#         2: extensions [-]
#             3: gpxx:WaypointExtension [-]
#                 4: gpxx:DisplayMode [-]
#         2: time [-]
#     1: trk [-]
#         2: name [-]
#         2: extensions [-]
#             3: gpxx:TrackExtension [-]
#                 4: gpxx:DisplayColor [-]
#         2: trkseg [-]
#             3: trkpt [lat, lon]
#                 4: ele [-]
#                 4: time [-]
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
