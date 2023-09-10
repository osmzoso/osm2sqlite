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


def write_csv_file(path_coordinates):
    for (lon, lat) in path_coordinates:
        print(str(lon) + ',' + str(lat))


if __name__ == "__main__":
    filename = sys.argv[1]
    path_coordinates, num_tracks = read_gpx_file(filename)
    if len(path_coordinates) == 0:
        path_coordinates, num_tracks = read_gpx_file(filename, '')
    write_csv_file(path_coordinates)

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
