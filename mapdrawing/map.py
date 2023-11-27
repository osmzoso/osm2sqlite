#!/usr/bin/env python
#
# Print a map
#
# https://www.w3schools.com/graphics/svg_intro.asp
# https://de.wikipedia.org/wiki/Scalable_Vector_Graphics
#
import sys
import proj
import sqlite3

if len(sys.argv) != 7:
    print(f'''
Creates a simple map in SVG format on stdout.
Usage:
{sys.argv[0]} DATABASE LON LAT ZOOMLEVEL SIZE_X SIZE_Y
    ''')
    sys.exit(1)

db_connect = sqlite3.connect(sys.argv[1])  # database connection
db = db_connect.cursor()                   # new database cursor
lon = float(sys.argv[2])
lat = float(sys.argv[3])
zoomlevel = int(sys.argv[4])
bbox_x = int(sys.argv[5])
bbox_y = int(sys.argv[6])

#
# draw_map(lon, lat, zoomlevel, bbox_x, bbox_y)
#

# map size
pixel_world_map, meters_pixel = proj.size_world_map(zoomlevel)
# pixel boundingbox
bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = proj.pixel_boundingbox(lon, lat, pixel_world_map, bbox_x, bbox_y)
# wgs84 boundingbox
bbox_min_lon, bbox_min_lat = proj.pixel_to_wgs84(bbox_min_x, bbox_min_y, pixel_world_map)
bbox_max_lon, bbox_max_lat = proj.pixel_to_wgs84(bbox_max_x, bbox_max_y, pixel_world_map)
#
print(f'<svg height="{bbox_y}" width="{bbox_x}">')
print('<!-- ************ map info ************')
print(f'lon       : {lon}\n' +
      f'lat       : {lat}\n' +
      f'zoomlevel : {zoomlevel}\n' +
      f'size_x    : {bbox_x} (= bbox_x)\n' +
      f'size_y    : {bbox_y} (= bbox_y)\n')
print(f'pixel_world_map : {pixel_world_map}px x {pixel_world_map}px\n')
print('pixel boundingbox:\n' +
      f'bbox_min_x, bbox_min_y : {bbox_min_x}, {bbox_min_y}\n' +
      f'bbox_max_x, bbox_max_y : {bbox_max_x}, {bbox_max_y}\n')
print('wgs84 boundingbox:\n' +
      f'bbox_min_lon, bbox_min_lat : {bbox_min_lon}, {bbox_min_lat}\n' +
      f'bbox_max_lon, bbox_max_lat : {bbox_max_lon}, {bbox_max_lat}\n')
print('check:')
print('bbox_max_x - bbox_min_x = bbox_x = size_x : ', bbox_max_x - bbox_min_x)
print('bbox_max_y - bbox_min_y = bbox_y = size_y : ', bbox_max_y - bbox_min_y)
print('************ map info ************ -->')
#
print('<rect width="100%" height="100%" fill="#e0dfdf" />')
# Search all ways in boundingbox wgs84
db.execute('''
CREATE TEMP TABLE map_ways AS
SELECT way_id
FROM rtree_way
WHERE max_lon>=? AND min_lon<=?
 AND  max_lat>=? AND min_lat<=?
''', (bbox_min_lon, bbox_max_lon, bbox_min_lat, bbox_max_lat))
db.execute('''
CREATE TEMP TABLE map_parts AS
SELECT mw.way_id,wt.key,wt.value,
  md.layer,md.style,md.width,md.fill,md.stroke,md.dash
FROM map_ways AS mw
LEFT JOIN way_tags AS wt ON mw.way_id=wt.way_id
LEFT JOIN map_def AS md ON wt.key=md.key AND wt.value LIKE md.value AND md.zoomlevel=?
''', (zoomlevel,))
#
db.execute('''
-- drawing plan
SELECT way_id,layer,style,width,fill,stroke,dash
FROM map_parts
WHERE layer IS NOT NULL
ORDER BY layer
''')
for (way_id,layer,style,width,fill,stroke,dash) in db.fetchall():
    # coordinates of the way
    if style == 'line':
        print('<polyline points="', end='')
    elif style == 'area':
        print('<polygon points="', end='')
    db.execute('''
    SELECT nodes.lon,nodes.lat
    FROM way_nodes AS wn
    LEFT JOIN nodes ON wn.node_id=nodes.node_id
    WHERE wn.way_id=?
    ORDER BY wn.node_order
    ''', (way_id,))
    for (lon, lat) in db.fetchall():
        x, y = proj.wgs84_to_pixel(lon, lat, pixel_world_map)
        x -= bbox_min_x
        y -= bbox_min_y
        y = bbox_y - y
        print(f' {x},{y}', end='')
    if style == 'line':
        #print(f'" style="fill:none;stroke:{stroke};stroke-width:{width};stroke-linecap:round" />')
        print(f'" style="fill:none;stroke:{stroke};stroke-width:{width};stroke-linecap:round;stroke-dasharray:{dash}" />')
    elif style == 'area':
        print(f'" style="fill:{fill};stroke:{stroke};stroke-width:{width}" />')

# draw unknown ways
db.execute('''
SELECT way_id
FROM map_ways
WHERE way_id NOT IN (SELECT DISTINCT way_id FROM map_parts WHERE layer IS NOT NULL)
''')
for (way_id,) in db.fetchall():
    print('<polyline points="', end='')
    db.execute('''
    SELECT nodes.lon,nodes.lat
    FROM way_nodes AS wn
    LEFT JOIN nodes ON wn.node_id=nodes.node_id
    WHERE wn.way_id=?
    ORDER BY wn.node_order
    ''', (way_id,))
    for (lon, lat) in db.fetchall():
        x, y = proj.wgs84_to_pixel(lon, lat, pixel_world_map)
        x -= bbox_min_x
        y -= bbox_min_y
        y = bbox_y - y
        print(f' {x},{y}', end='')
    print(f'" style="fill:none;stroke:red;stroke-width:1" />')

print('</svg>')

