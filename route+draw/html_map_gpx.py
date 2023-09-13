#!/usr/bin/env python
#
#
#
import sys
import xml.etree.ElementTree as ET
import html_leaflet
# from random import shuffle

if len(sys.argv) == 1:
    print(f'''
    Creates a map with all paths from the specified GPX files.
    Output is HTML on stdout.
    Usage:
    {sys.argv[0]} GPX_FILE ...
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


if __name__ == "__main__":
    # https://www.graphviz.org/doc/info/colors.html
    # color_scheme = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d']
    color_scheme = ['#e60000', '#e67300', '#e6e600', '#73e600', '#00e6e6', '#0073e6', '#0000e6']
    # shuffle(color_scheme)
    color_number = 0
    m1 = html_leaflet.Leaflet()
    m1.print_html_header('Map GPX Files')
    print('<h1>Map GPX Files</h1>')
    print('<p><div id="mapid" style="width: 100%; height: 700px;"></div></p>')
    m1.print_script_start()
    infotext = '<tr><th>file</th><th>tracks</th><th>trackpoints</th></tr>\n'
    for filename in sys.argv:
        if filename == sys.argv[0]:
            continue
        path_coordinates, num_tracks = read_gpx_file(filename)
        num_trackpoints = len(path_coordinates)
        color = color_scheme[color_number]
        color_number = color_number + 1
        if color_number == len(color_scheme):
            color_number = 0
        m1.set_color(color)
        m1.set_opacity(0.7)
        m1.add_polyline(path_coordinates)
        infotext = infotext + f'<tr><td>{filename}</td><td bgcolor="{color}">{num_tracks}</td><td>{num_trackpoints}</td></tr>\n'
    m1.print_script_end()
    print('<table>\n' + infotext + '</table>\n')
    print('</body>\n</html>')
