#!/usr/bin/env python
#
#
#
import sys
import html_leaflet

if len(sys.argv) != 2:
    print(f'''
    Creates a map from a csv file containing waypoints (lon,lat).
    Output is HTML on stdout.
    Usage:
    {sys.argv[0]} CSV_FILE
    ''')
    sys.exit(1)

filename = sys.argv[1]

path_coordinates = []
infotext = filename + '\n'

fobj = open(filename, "r")
for line in fobj:
    if line.startswith("# subgraph_boundingbox:"):
        bbox = line.split()
    if line.startswith("#"):
        infotext = infotext + line
        continue
    lonlat = line.split(',')
    try:
        lon = float(lonlat[0])
        lat = float(lonlat[1])
    except ValueError:
        continue
    path_coordinates.append((lon, lat))
fobj.close()

m1 = html_leaflet.Leaflet()
m1.print_html_header('Map Routing')
#
print('<h1>Map Routing Path</h1>')
print(f'<pre>{infotext}</pre>')
print('<p><div id="mapid" style="width: 100%; height: 700px;"></div></p>')
m1.print_script_start()
m1.set_properties('#ff0000', 0.6, 6, '', '#00ffff', 0.7)
m1.add_polyline(path_coordinates)
if 'bbox' in locals():
    m1.set_properties('#005588', 1.0, 2, '5 5', 'none', 1.0)
    m1.add_rectangle(float(bbox[2]), float(bbox[3]), float(bbox[4]), float(bbox[5]), '')
m1.print_script_end()
print('</body></html>')
