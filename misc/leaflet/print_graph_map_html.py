#!/usr/bin/env python
import sys, sqlite3
import leaflet

if len(sys.argv) != 6:
    print('''
    Creates a map of the routing graph in a given area.
    The file is written to stdout in HTML format.
    Usage:
    print_graph_html.py DATABASE MIN_LON MIN_LAT MAX_LON MAX_LAT
    ''')
    sys.exit(1)

database = sys.argv[1]
min_lon  = float(sys.argv[2])
min_lat  = float(sys.argv[3])
max_lon  = float(sys.argv[4])
max_lat  = float(sys.argv[5])

db_connect = sqlite3.connect(database)
db = db_connect.cursor()   # new database cursor

m1 = leaflet.Leaflet()
m1.print_html_header('Map Routing Graph')

print(f'<h2>Map Routing Graph ({min_lon} {min_lat}) ({max_lon} {max_lat})</h2>')
print('''
<p>
<div id="mapid" style="width: 1400px; height: 800px;"></div>
</p>
''')

query = '''
SELECT
 --g.node_id_from,g.node_id_to,g.dist,g.way_id,
 nf.lon,nf.lat,
 nt.lon,nt.lat
FROM graph AS g
LEFT JOIN nodes AS nf ON g.node_id_from=nf.node_id
LEFT JOIN nodes AS nt ON g.node_id_to=nt.node_id
WHERE
 nf.lon>=? AND
 nt.lon>=? AND
 nf.lon<=? AND
 nt.lon<=? AND
 nf.lat>=? AND
 nt.lat>=? AND
 nf.lat<=? AND
 nt.lat<=?
'''
# Faster query but less precise...
# WHERE g.way_id IN (
#     SELECT way_id
#     FROM rtree_way
#     WHERE max_lon>=? AND min_lon<=?
#     AND  max_lat>=? AND min_lat<=?

#
m1.print_script_start()
db.execute(query, (min_lon, min_lon, max_lon, max_lon, min_lat, min_lat, max_lat, max_lat))
for (from_lon,from_lat,to_lon,to_lat) in db.fetchall():
    m1.add_line(from_lon, from_lat, to_lon, to_lat)
#
m1.set_properties( '#ff0000', 1.0, 2, '5 5', 'none', 1.0 )
m1.add_rectangle(min_lon, min_lat, max_lon, max_lat, '')
#
m1.print_script_end()
#
print('</body>')
print('</html>')

db_connect.commit()
db_connect.close()

