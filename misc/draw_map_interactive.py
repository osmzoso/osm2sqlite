#!/usr/bin/env python
#
# Print a very simple map
#
from tkinter import *
from tkinter import ttk
import sys
import sqlite3

if len(sys.argv) != 4:
    print(f'''
    Print a very simple map in a window.
    Usage:
    {sys.argv[0]} DATABASE LON LAT
    ''')
    sys.exit(1)

# database connection
db_connect = sqlite3.connect(sys.argv[1])
db = db_connect.cursor()   # new database cursor

#
# Public variable
#
# map size in pixels
map_width = 1200
map_height = 800
# Zentrale Koordinaten der Karte
map_lon = 7.80742505  # Freiburg, St. Georgen
map_lat = 47.98203435
# TODO Bereich berechnen aufgrund des Seitenverhältnis map_width/map_height
range_lon = 0.0029
range_lat = 0.0013
# Boundingbox
min_lon = 0
min_lat = 0
max_lon = 0
max_lat = 0
m_lon = 0
n_lon = 0
m_lat = 0
n_lat = 0

#
try:
    map_lon = float(sys.argv[2])
    map_lat = float(sys.argv[3])
except ValueError:
    print('error : lon lat not numeric')
    sys.exit(1)


def calc_boundingbox():
    global min_lon, max_lon, min_lat, max_lat, range_lon, range_lat
    global m_lon, n_lon, m_lat, n_lat
    min_lon = map_lon - range_lon
    max_lon = map_lon + range_lon
    min_lat = map_lat - range_lat
    max_lat = map_lat + range_lat
    # Werte für Umrechnung der Koordinaten in pixel mit Geradengleichung: y = mx+n
    m_lon = map_width / (max_lon - min_lon)     # lon: Steigung
    n_lon = -1 * m_lon * min_lon                # lon: Y-Achsenabschnitt
    m_lat = map_height / (max_lat - min_lat)    # lat: Steigung
    n_lat = -1 * m_lat * min_lat                # lat: Y-Achsenabschnitt


def exit_app(*args):
    root.destroy()


def lon2px(lon):
    return int(m_lon * lon + n_lon)


def lat2px(lat):
    return map_height - int(m_lat * lat + n_lat)


def move_up(*args):
    global map_lat
    map_lat = map_lat + 0.0002
    draw_map()


def move_left(*args):
    global map_lon
    map_lon = map_lon - 0.0002
    draw_map()


def move_right(*args):
    global map_lon
    map_lon = map_lon + 0.0002
    draw_map()


def move_down(*args):
    global map_lat
    map_lat = map_lat - 0.0002
    draw_map()


def draw_map(*args):
    # print(map_lon, map_lat)    # TEST
    calc_boundingbox()
    cv.delete("all")
    query = """
    SELECT way_id
    FROM rtree_way
    WHERE max_lon>=? AND min_lon<=?
     AND  max_lat>=? AND min_lat<=?
    """
    db.execute(query, (min_lon, max_lon, min_lat, max_lat))
    way_list = []
    way_unknown = 0
    for (way_id,) in db.fetchall():
        way1 = {}
        way2 = {}
        #
        db.execute("SELECT key,value FROM way_tags WHERE way_id=?", (way_id,))
        for (key, value) in db.fetchall():
            # Layer 1
            if key == 'landuse' and value == 'farmland':
                way1 = {'layer': 1, 'style': 'polygon', 'width': 0, 'fill': '#eef0d5', 'outline': '', 'dash': ''}
            elif key == 'landuse' and value == 'commercial':
                way1 = {'layer': 1, 'style': 'polygon', 'width': 0, 'fill': '#f2dad9', 'outline': '', 'dash': ''}
            elif key == 'natural' and value == 'grassland':
                way1 = {'layer': 1, 'style': 'polygon', 'width': 0, 'fill': '#cdebb0', 'outline': '', 'dash': ''}
            elif key == 'landuse' and value == 'residential':
                way1 = {'layer': 1, 'style': 'polygon', 'width': 0, 'fill': '#e0dfdf', 'outline': '#cbcdc9', 'dash': ''}
            elif key == 'landuse' and value == 'industrial':
                way1 = {'layer': 1, 'style': 'polygon', 'width': 0, 'fill': '#ebdbe8', 'outline': '#988e96', 'dash': ''}
            # Layer 2
            elif key == 'landuse' and value in ('grass', 'meadow'):
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#cdebb0', 'outline': '', 'dash': ''}
            elif key == 'landuse' and value == 'forest':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#add19e', 'outline': '', 'dash': ''}
            elif key == 'natural' and value == 'wood':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#add19e', 'outline': '', 'dash': ''}
            elif key == 'landuse' and value == 'vineyard':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#bddc9a', 'outline': '', 'dash': ''}
            elif key == 'landuse' and value == 'farmyard':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#f5dcba', 'outline': '#d8be98', 'dash': ''}
            elif key == 'landuse' and value == 'orchard':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#aedfa3', 'outline': '', 'dash': ''}
            elif key == 'landuse' and value == 'allotments':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#d5e4cb', 'outline': '', 'dash': ''}
            elif key == 'leisure' and value == 'park':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#c8facc', 'outline': '', 'dash': ''}
            elif key == 'landuse' and value == 'recreation_ground':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#dffce2', 'outline': '#9dd5a1', 'dash': ''}
            elif key == 'landuse' and value == 'construction':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#c7c7b4', 'outline': '', 'dash': ''}
            # Layer 3
            elif key == 'leisure' and value == 'playground':
                way1 = {'layer': 3, 'style': 'polygon', 'width': 0, 'fill': '#dffce2', 'outline': '#a1dea6', 'dash': ''}
            elif key == 'leisure' and value == 'pitch':
                way1 = {'layer': 3, 'style': 'polygon', 'width': 0, 'fill': '#aae0cb', 'outline': '#8ecfb5', 'dash': ''}
            # Layer 4
            elif key == 'natural' and value == 'water':
                way1 = {'layer': 4, 'style': 'polygon', 'width': 0, 'fill': '#aad3df', 'outline': '', 'dash': ''}
            elif key == 'waterway' and value == 'stream':
                way1 = {'layer': 4, 'style': 'line', 'width': 4, 'fill': '#aad3df', 'outline': '', 'dash': ''}
            elif key == 'barrier':
                way1 = {'layer': 4, 'style': 'line', 'width': 1, 'fill': '#9fb0a1', 'outline': '', 'dash': ''}
            #
            elif key == 'highway' and value == 'track':
                way1 = {'layer': 5, 'style': 'line', 'width': 2, 'fill': '#a5832c', 'outline': '', 'dash': '9 3'}
            elif key == 'highway' and value == 'service':
                way1 = {'layer': 5, 'style': 'line', 'width': 8, 'fill': '#cccccc', 'outline': '', 'dash': ''}
                way2 = {'layer': 7, 'style': 'line', 'width': 6, 'fill': '#ffffff', 'outline': '', 'dash': ''}
            elif key == 'highway' and value in ('residential', 'unclassified'):
                way1 = {'layer': 5, 'style': 'line', 'width': 14, 'fill': '#cccccc', 'outline': '', 'dash': ''}
                way2 = {'layer': 7, 'style': 'line', 'width': 12, 'fill': '#ffffff', 'outline': '', 'dash': ''}
            elif key == 'highway' and value in ('living_street', 'pedestrian'):
                way1 = {'layer': 5, 'style': 'line', 'width': 14, 'fill': '#c4c4c4', 'outline': '', 'dash': ''}
                way2 = {'layer': 6, 'style': 'line', 'width': 12, 'fill': '#ededed', 'outline': '', 'dash': ''}
            elif key == 'highway' and value in ('path', 'footway'):
                way1 = {'layer': 5, 'style': 'line', 'width': 2, 'fill': '#ffffff', 'outline': '', 'dash': ''}
                way2 = {'layer': 6, 'style': 'line', 'width': 2, 'fill': '#fa8274', 'outline': '', 'dash': '4 4'}
            elif key == 'highway' and value == 'steps':
                way1 = {'layer': 5, 'style': 'line', 'width': 5, 'fill': '#ffffff', 'outline': '', 'dash': ''}
                way2 = {'layer': 6, 'style': 'line', 'width': 5, 'fill': '#fa8274', 'outline': '', 'dash': '2 2'}
            elif key == 'highway' and value == 'cycleway':
                way1 = {'layer': 5, 'style': 'line', 'width': 2, 'fill': '#ffffff', 'outline': '', 'dash': ''}
                way2 = {'layer': 6, 'style': 'line', 'width': 2, 'fill': '#0e0efe', 'outline': '', 'dash': '4 4'}
            elif key == 'highway' and value in ('tertiary', 'tertiary_link'):
                way1 = {'layer': 5, 'style': 'line', 'width': 18, 'fill': '#888888', 'outline': '', 'dash': ''}
                way2 = {'layer': 8, 'style': 'line', 'width': 16, 'fill': '#ffffff', 'outline': '', 'dash': ''}
            elif key == 'highway' and value in ('secondary', 'secondary_link'):
                way1 = {'layer': 5, 'style': 'line', 'width': 18, 'fill': '#888888', 'outline': '', 'dash': ''}
                way2 = {'layer': 8, 'style': 'line', 'width': 16, 'fill': '#f7fabf', 'outline': '', 'dash': ''}
            elif key == 'highway' and value in ('trunk', 'trunk_link'):
                way1 = {'layer': 5, 'style': 'line', 'width': 18, 'fill': '#888888', 'outline': '', 'dash': ''}
                way2 = {'layer': 7, 'style': 'line', 'width': 16, 'fill': '#f9b29c', 'outline': '', 'dash': ''}
            elif key == 'highway' and value in ('primary', 'primary_link'):
                way1 = {'layer': 5, 'style': 'line', 'width': 18, 'fill': '#a26e04', 'outline': '', 'dash': ''}
                way2 = {'layer': 7, 'style': 'line', 'width': 16, 'fill': '#fcd6a4', 'outline': '', 'dash': ''}
            elif key == 'highway' and value in ('motorway', 'motorway_link'):
                way1 = {'layer': 5, 'style': 'line', 'width': 18, 'fill': '#de3a71', 'outline': '', 'dash': ''}
                way2 = {'layer': 7, 'style': 'line', 'width': 16, 'fill': '#e892a2', 'outline': '', 'dash': ''}
            elif key == 'railway' and value == 'rail':
                way1 = {'layer': 5, 'style': 'line', 'width': 5, 'fill': '#707070', 'outline': '', 'dash': ''}
                way2 = {'layer': 7, 'style': 'line', 'width': 3, 'fill': '#fefefe', 'outline': '', 'dash': '12 12'}
            elif key == 'railway' and value == 'tram':
                way1 = {'layer': 8, 'style': 'line', 'width': 4, 'fill': '#6e6e6e', 'outline': '', 'dash': ''}
            elif key == 'building':
                way1 = {'layer': 4, 'style': 'polygon', 'width': 0, 'fill': '#d9d0c9', 'outline': '#c2b5aa', 'dash': ''}
            elif key == 'amenity':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#eeeeee', 'outline': '#d8c3c2', 'dash': ''}
            elif key == 'landuse' and value == 'cemetery':
                way1 = {'layer': 1, 'style': 'polygon', 'width': 0, 'fill': '#aacbaf', 'outline': '', 'dash': ''}
            elif key == 'landuse' and value == 'railway':
                way1 = {'layer': 1, 'style': 'polygon', 'width': 0, 'fill': '#e9dae7', 'outline': '#aaa5a8', 'dash': ''}
            elif key == 'leisure' and value == 'swimming_pool':
                way1 = {'layer': 3, 'style': 'polygon', 'width': 0, 'fill': '#aad3df', 'outline': '#7dc7dc', 'dash': ''}
            elif key == 'natural' and value == 'scrub':
                way1 = {'layer': 2, 'style': 'polygon', 'width': 0, 'fill': '#c8d7ab', 'outline': '', 'dash': ''}
            elif key == 'natural' and value == 'tree_row':
                way1 = {'layer': 2, 'style': 'line', 'width': 4, 'fill': '#9cd79f', 'outline': '', 'dash': ''}    # opacity 0.5
            elif key == 'highway' and value == 'platform':
                way1 = {'layer': 3, 'style': 'polygon', 'width': 0, 'fill': '#bbbbbb', 'outline': '#929191', 'dash': ''}
        # no definition than mark with red line
        if way1 == {}:
            way1 = {'layer': 11, 'style': 'line', 'width': 2, 'fill': '#ff0000', 'outline': '', 'dash': ''}
        #
        # TODO
        # - key='bridge' und value='yes' -> Layer erhöhen (Python way1['layer'] = way1['layer'] + 3)
        # - key='area' und value='yes' -> dann polygon, Farbe/Layer??
        #
        way_list.append([way_id, way1['layer'], way1['style'], way1['width'], way1['fill'], way1['outline'], way1['dash']])
        if way2 != {}:
            way_list.append([way_id, way2['layer'], way2['style'], way2['width'], way2['fill'], way2['outline'], way2['dash']])
            way_unknown = way_unknown + 1
        #
        # way_list.append([way_id, 12, 'line', 2, '#ff0000', '', ''])
    # print(way_unknown, 'ways unknown') # TEST
    # draw layer 0-12
    for draw_layer in range(0, 12):
        for way_info in way_list:
            way_id = way_info[0]
            way_layer = way_info[1]
            if way_layer != draw_layer:
                continue
            way_style = way_info[2]
            way_width = way_info[3]
            way_fill = way_info[4]
            way_outline = way_info[5]
            way_dash = way_info[6]
            # coordinates of the way
            query3 = """
            SELECT nodes.lon,nodes.lat
            FROM way_nodes
            LEFT JOIN nodes ON way_nodes.node_id=nodes.node_id
            WHERE way_nodes.way_id=?
            ORDER BY way_nodes.node_order
            """
            db.execute(query3, (way_id,))
            coord_list = ()
            for (lon, lat) in db.fetchall():
                coord_list = coord_list + (lon2px(lon), lat2px(lat))
            #
            if way_style == 'line':
                cv.create_line(coord_list, fill=way_fill, width=way_width, dash=way_dash)
            elif way_style == 'polygon':
                cv.create_polygon(coord_list, fill=way_fill, outline=way_outline)


#
# Show map from database with GUI
#
root = Tk()
root.title("Show OSM Map")

# grid row 0 -> Canvas, span über mehrere Spalten
cv = Canvas(root, width=map_width, height=map_height)
cv.grid(column=0, row=0, columnspan=12)

# grid row 1 -> alle Buttons in dieser row
ttk.Button(root, text='\u2191', command=move_up).grid(column=0, row=1)
ttk.Button(root, text='\u2190', command=move_left).grid(column=1, row=1)
ttk.Button(root, text='\u2192', command=move_right).grid(column=2, row=1)
ttk.Button(root, text='\u2193', command=move_down).grid(column=3, row=1)
ttk.Button(root, text="Quit", command=exit_app).grid(column=4, row=1)

# bind keys
root.bind('<Escape>', exit_app)
root.bind('<q>', exit_app)
root.bind('<Q>', exit_app)
root.bind('<Up>', move_up)
root.bind('<Left>', move_left)
root.bind('<Right>', move_right)
root.bind('<Down>', move_down)

#
draw_map()

#
root.mainloop()
