#!/usr/bin/env python
import sys
import sqlite3
import html_leaflet

if len(sys.argv) != 6:
    print(f'''
    Creates a map of the routing graph in table "graph" in a given area.
    Output is HTML on stdout.
    Usage:
    {sys.argv[0]} DATABASE MIN_LON MIN_LAT MAX_LON MAX_LAT
    ''')
    sys.exit(1)

database = sys.argv[1]
min_lon = float(sys.argv[2])
min_lat = float(sys.argv[3])
max_lon = float(sys.argv[4])
max_lat = float(sys.argv[5])

db_connect = sqlite3.connect(database)
db = db_connect.cursor()   # new database cursor

m1 = html_leaflet.Leaflet()
m1.print_html_header('Map Routing Graph')

print(f'<h2>Map Routing Graph ({min_lon} {min_lat}) ({max_lon} {max_lat})</h2>')
print('''
<p>
<div id="mapid" style="width: 100%; height: 700px;"></div>
</p>
''')

m1.print_script_start()

db.execute('''
SELECT ns.lon,ns.lat,ne.lon,ne.lat
FROM graph AS g
LEFT JOIN nodes AS ns ON g.start_node_id=ns.node_id
LEFT JOIN nodes AS ne ON g.end_node_id=ne.node_id
WHERE g.way_id IN (
 SELECT way_id
 FROM rtree_way
 WHERE max_lon>=? AND min_lon<=?
  AND  max_lat>=? AND min_lat<=?
)
''', (min_lon, max_lon, min_lat, max_lat))
for (lon_start, lat_start, lon_end, lat_end) in db.fetchall():
    m1.add_line(lon_start, lat_start, lon_end, lat_end)
#
m1.set_properties('#ff0000', 1.0, 2, '5 5', 'none', 1.0)
m1.add_rectangle(min_lon, min_lat, max_lon, max_lat, '')
#
m1.print_script_end()
#
print('</body>')
print('</html>')

db_connect.commit()
db_connect.close()
