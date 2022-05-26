#!/usr/bin/env python
import sys, sqlite3

if len(sys.argv) != 6:
    print('''
    Creates a map of all addresses in a given area.
    The addresses must be in table "addr_view".
    The file is written to stdout in HTML format.
    Usage:
    addr_map.py DATABASE MIN_LON MIN_LAT MAX_LON MAX_LAT
    ''')
    sys.exit(1)

database = sys.argv[1]
min_lon  = sys.argv[2]
min_lat  = sys.argv[3]
max_lon  = sys.argv[4]
max_lat  = sys.argv[5]

db_connect = sqlite3.connect(database)
db = db_connect.cursor()   # new database cursor

print('''
<!DOCTYPE html>
<html>
<head>
<title>Karte OSM Adressen</title>
<style>
body {
 font-family: Verdana, Arial;
 font-size: 1.0em;
}
table {
 border: 2px solid #bbbbbb;
 border-collapse: collapse;
}
th {
 border: 1px solid #cccccc;
 font-size: 0.8em;
}
td {
 border: 1px solid #aaaaaa;
 font-size: 0.8em;
}
</style>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>
</head>
<body>''')
print(f'<h2>Karte OpenStreetMap Adressen ({min_lon} {min_lat}) ({max_lon} {max_lat})</h2>')
print('''
<p>
<div id="mapid" style="width: 1200px; height: 800px;"></div>
</p>

<script>
''')
print(f'var map_boundingbox = [ [ {min_lat}, {min_lon} ], [ {max_lat}, {max_lon} ] ];')
print('''
// init map with given boundingbox
var mymap = L.map('mapid').fitBounds( map_boundingbox, {padding: [0,0], maxZoom: 19} );

// init tile server
var tile_server = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';  // OpenStreetMap's Standard tile layer
//var tile_server = 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png';  // Wikimedia Maps
L.tileLayer( tile_server, {
   maxZoom: 19,
   attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(mymap);
''')

query = '''
SELECT way_id,node_id,postcode,city,street,housenumber,lon,lat
FROM addr_view
WHERE lon>=? AND lat>=? AND lon<=? AND lat<=?
ORDER BY postcode,street,abs(housenumber)
'''

# 1. Leaflet marker
db.execute(query, (min_lon, min_lat, max_lon, max_lat))
for (way_id,node_id,postcode,city,street,housenumber,lon,lat) in db.fetchall():
    popup_text = '<pre>'
    popup_text += f'addr:postcode    : {postcode}<br>'
    popup_text += f'addr:city        : {city}<br>'
    popup_text += f'addr:street      : {street}<br>'
    popup_text += f'addr:housenumber : {housenumber}<br>'
    popup_text += '</pre>'
    print(f"L.marker([{lat}, {lon}]).bindPopup('{popup_text}').addTo(mymap);")

# Rechteck Boundingbox
print(f'L.rectangle( [ [ {min_lat}, {min_lon} ], [ {max_lat}, {max_lon} ] ]'+", { color:'#000068', fill:false, dashArray:'5 5', weight:3 } ).addTo(mymap);")

print('</script>')

# 2. Table of addresses
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

