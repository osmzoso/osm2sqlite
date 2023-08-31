#!/usr/bin/env python
#
#
#
import sys
import xml.etree.ElementTree as ET
import html_leaflet

if len(sys.argv) != 2:
    print(f'''
    Creates a map with the path from a gpx file.
    Output is HTML on stdout.
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
    return num_tracks, path_coordinates


def print_map(filename):
    num_tracks, path_coordinates = read_gpx_file(filename)
    # if no tracks are found then search without namespace
    if num_tracks == 0 and len(path_coordinates) == 0:
        num_tracks, path_coordinates = read_gpx_file(filename, '')
    num_trackpoints = len(path_coordinates)
    #
    m1 = html_leaflet.Leaflet()
    m1.print_html_header('Show GPX')
    print('<h1>Map Path</h1>')
    print(f'<p>\nFile: <b>{filename}</b> Tracks: <b>{num_tracks}</b> Trackpoints: <b>{num_trackpoints}</b>\n</p>\n')
    print('<p><div id="mapid" style="width: 1200px; height: 700px;"></div></p>')
    m1.print_script_start()
    m1.set_properties('#ff0000', 0.6, 6, '', '#00ffff', 0.7)
    m1.add_polyline(path_coordinates)
    m1.print_script_end()
    print('</body>\n</html>')

if __name__ == "__main__":
    filename = sys.argv[1]
    print_map(filename)
