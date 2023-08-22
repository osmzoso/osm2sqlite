#!/usr/bin/env python
#
#
#
import sys
# find module, see https://bic-berkeley.github.io/psych-214-fall-2016/sys_path.html
#from os.path import dirname, abspath, join
#this_dir = dirname(__file__)
#leaflet_dir = abspath(join(this_dir, '..', 'html_leaflet'))
#sys.path.append(leaflet_dir)
import html_leaflet

if len(sys.argv) != 2:
    print(f'''
    Creates a map with the path from a list of waypoints.
    Input is a FILE with a list of coordinates (lon lat).
    Output is HTML on stdout.
    Usage:
    {sys.argv[0]} FILE
    ''')
    sys.exit(1)

filename = sys.argv[1]

path = []
infotext = filename + '\n'

fobj = open(filename, "r")
for line in fobj:
    if line.startswith("## subgraph boundingbox"):
        bbox = line.split()
    if line.startswith("## "):
        infotext = infotext + line
    if line.startswith("#"):
        continue
    line = line.strip()
    list_lon_lat = line.split(" ")
    path.append( float(list_lon_lat[0]) )
    path.append( float(list_lon_lat[1]) )
fobj.close()

m1 = html_leaflet.Leaflet()
m1.print_html_header('Map Routing')
#
print('<h1>Map Routing Path</h1>')
print(f'<pre>{infotext}</pre>')
print('''
<p>
<div id="mapid" style="width: 1200px; height: 700px;"></div>
</p>
''')
m1.print_script_start()

m1.set_properties( '#ff0000', 0.6, 6, '', '#00ffff', 0.7 )
m1.add_polyline( path )

m1.set_properties( '#005588', 1.0, 2, '5 5', 'none', 1.0 )
m1.add_rectangle( float(bbox[3]), float(bbox[4]), float(bbox[5]), float(bbox[6]), '' )

m1.print_script_end()
print('''
</body>
</html>
''')

