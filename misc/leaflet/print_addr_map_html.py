#!/usr/bin/env python
import sys, sqlite3
import leaflet

if len(sys.argv) != 6:
    print('''
    Creates a map of all addresses in a given area.
    The addresses must be in table "addr_view".
    The file is written to stdout in HTML format.
    Usage:
    print_addr_map_html.py DATABASE MIN_LON MIN_LAT MAX_LON MAX_LAT
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
m1.print_html_header('Map OSM addresses')

print(f'<h2>Map of the OpenStreetMap addresses ({min_lon} {min_lat}) ({max_lon} {max_lat})</h2>')
print('''
<p>
<div id="mapid" style="width: 1200px; height: 800px;"></div>
</p>
''')

query = '''
SELECT way_id,node_id,postcode,city,street,housenumber,lon,lat
FROM addr_view
WHERE lon>=? AND lat>=? AND lon<=? AND lat<=?
ORDER BY postcode,street,abs(housenumber)
'''

#
# 1. Map Marker
#
m1.print_script_start()
db.execute(query, (min_lon, min_lat, max_lon, max_lat))
for (way_id,node_id,postcode,city,street,housenumber,lon,lat) in db.fetchall():
    popup_text = '<pre>'
    popup_text += f'addr:postcode    : {postcode}<br>'
    popup_text += f'addr:city        : {city}<br>'
    popup_text += f'addr:street      : {street}<br>'
    popup_text += f'addr:housenumber : {housenumber}<br>'
    popup_text += '</pre>'
    m1.add_marker(lon, lat, popup_text, False)
# Boundingbox
m1.set_properties( '#000068', 1.0, 2, '5 5', 'none', 1.0 )
m1.add_rectangle( m1.bbox_min_lon, m1.bbox_min_lat, m1.bbox_max_lon, m1.bbox_max_lat, '' )
m1.print_script_end()

#
# 2. Table of addresses
#
print('<table>')
print('<tr><th>way_id</th><th>node_id</th><th>addr:postcode</th><th>addr:city</th><th>addr:street</th><th>addr:housenumber</th><th>lon</th><th>lat</th></tr>')
db.execute(query, (min_lon, min_lat, max_lon, max_lat))
for (way_id,node_id,postcode,city,street,housenumber,lon,lat) in db.fetchall():
    print(f'<tr><td>{way_id}</td><td>{node_id}</td><td>{postcode}</td><td>{city}</td> \
    <td>{street}</td><td>{housenumber}</td><td>{lon}</td><td>{lat}</td></tr>')
print('</table>')

print('</body>')
print('</html>')

db_connect.commit()
db_connect.close()

