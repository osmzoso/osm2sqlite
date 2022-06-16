#!/usr/bin/env python
#
# Print a very simple map
#
from tkinter import *
from tkinter import ttk
import sys, sqlite3

if len(sys.argv)!=4:
    print('''
    Print a very simple map.
    Usage:
    show_map.py DATABASE LON LAT
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
map_lon =  7.80742505  # Freiburg, St. Georgen
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
    print('Error')
    map_lon =  7.807
    map_lat = 47.982

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
    map_lat = map_lat + 0.00015
    draw_map()

def move_left(*args):
    global map_lon
    map_lon = map_lon - 0.00015
    draw_map()

def move_right(*args):
    global map_lon
    map_lon = map_lon + 0.00015
    draw_map()

def move_down(*args):
    global map_lat
    map_lat = map_lat - 0.00015
    draw_map()

def draw_map(*args):
    print(map_lon, map_lat)
    calc_boundingbox()
    cv.delete("all")
    #
    # 1. Areas
    #
    query = """
    SELECT way_id
    FROM landuse
    WHERE max_lon>=? AND min_lon<=?
     AND  max_lat>=? AND min_lat<=?
    """
    db.execute(query, (min_lon, max_lon, min_lat, max_lat))
    for (way_id,) in db.fetchall():
        # landuse value
        query2 = "SELECT value FROM way_tags WHERE way_id=? AND key='landuse'"
        db.execute(query2, (way_id,))
        landuse_value = db.fetchone()[0]
        # coordinates of the way
        query3 = """
        SELECT n.lon,n.lat
        FROM way_nodes AS wn
        LEFT JOIN nodes AS n ON wn.node_id=n.node_id
        WHERE wn.way_id=?
        ORDER BY wn.node_order
        """
        db.execute(query3, (way_id,))
        coord_list = ()
        for (lon, lat) in db.fetchall():
            coord_list = coord_list + ( lon2px(lon), lat2px(lat) )
        # print polygon
        if landuse_value in ('grass', 'meadow'):
            cv.create_polygon(coord_list, fill='#cdebb0', outline='')
        elif landuse_value == 'farmland':
            cv.create_polygon(coord_list, fill='#eef0d5', outline='')
        elif landuse_value == 'orchard':
            cv.create_polygon(coord_list, fill='#aedfa3', outline='')
        elif landuse_value == 'forest':
            cv.create_polygon(coord_list, fill='#add19e', outline='')
        elif landuse_value == 'commercial':
            cv.create_polygon(coord_list, fill='#f2dad9', outline='')
        elif landuse_value == 'recreation_ground':
            cv.create_polygon(coord_list, fill='#dffce2', outline='#9dd5a1')
        elif landuse_value == 'construction':
            cv.create_polygon(coord_list, fill='#c7c7b4', outline='')
        elif landuse_value == 'residential':
            cv.create_polygon(coord_list, fill='#e0dfdf', outline='#cbcdc9')
        elif landuse_value == 'allotments':
            cv.create_polygon(coord_list, fill='#d5e4cb', outline='')
        elif landuse_value == 'industrial':
            cv.create_polygon(coord_list, fill='#ebdbe8', outline='#988e96')
        elif landuse_value == 'cemetery':
            cv.create_polygon(coord_list, fill='#aacbaf', outline='')
        elif landuse_value == 'vineyard':
            cv.create_polygon(coord_list, fill='#bddc9a', outline='')
        elif landuse_value == 'farmyard':
            cv.create_polygon(coord_list, fill='#f5dcba', outline='#d8be98')
        elif landuse_value == 'railway':
            cv.create_polygon(coord_list, fill='#e9dae7', outline='#aaa5a8')
        else:
            print("landuse_value '"+landuse_value+"' not yet defined")
            cv.create_polygon(coord_list, fill='#ff016a', outline='')
        #+---------+-------------------------+--------+
        #|   key   |          value          | number |
        #+---------+-------------------------+--------+
        #| landuse | meadow                  | 37102  | OK
        #| landuse | farmland                | 28351  | OK
        #| landuse | orchard                 | 13483  | OK
        #| landuse | forest                  | 13192  | OK
        #| landuse | grass                   | 11767  | OK
        #| landuse | vineyard                | 9093   | OK
        #| landuse | residential             | 6701   | OK
        #| landuse | farmyard                | 5312   | OK
        #| landuse | allotments              | 4184   | OK
        #| landuse | industrial              | 1397   | OK
        #| landuse | cemetery                | 949    | OK
        #| landuse | commercial              | 682    | OK
        #| landuse | recreation_ground       | 660    | OK
        #| landuse | basin                   | 589    |
        #| landuse | construction            | 502    | OK
        #| landuse | railway                 | 297    | OK
        #| landuse | quarry                  | 244    |
        #| landuse | greenhouse_horticulture | 193    |
        #| landuse | village_green           | 192    |
        #| landuse | plant_nursery           | 170    |
        #| landuse | retail                  | 133    |
        #| landuse | landfill                | 128    |
        #| landuse | brownfield              | 112    |
        #| landuse | reservoir               | 94     |
        #| landuse | animal_keeping          | 83     |
        #| landuse | flowerbed               | 65     |
        #| landuse | greenfield              | 58     |
        #| landuse | aquaculture             | 47     |
        #| landuse | garages                 | 40     |
        #| landuse | military                | 31     |
        #| landuse | religious               | 16     |
        #| landuse | yes                     | 10     |
        #| landuse | highway                 | 8      |
        #| landuse | piste                   | 6      |
        #| landuse | paddock                 | 4      |
        #| landuse | harbour                 | 3      |
        #| landuse | hedge                   | 3      |
        #| landuse | plaza                   | 3      |
        #| landuse | scrub                   | 3      |
        #| landuse | building_site           | 2      |
        #| landuse | education               | 2      |
        #| landuse | garage                  | 2      |
        #| landuse | garden                  | 2      |
        #| landuse | road                    | 2      |
        #| landuse | churchyard              | 1      |
        #| landuse | covered_basin           | 1      |
        #| landuse | depot                   | 1      |
        #| landuse | disused:quarry          | 1      |
        #| landuse | fishfarm                | 1      |
        #| landuse | grassland               | 1      |
        #| landuse | lifestock               | 1      |
        #| landuse | logging                 | 1      |
        #| landuse | meadow_orchard          | 1      |
        #| landuse | monastary               | 1      |
        #| landuse | natural                 | 1      |
        #| landuse | observatory             | 1      |
        #| landuse | park                    | 1      |
        #| landuse | pond                    | 1      |
        #| landuse | public                  | 1      |
        #| landuse | recycling               | 1      |
        #| landuse | school                  | 1      |
        #| landuse | shelter                 | 1      |
        #| landuse | storage                 | 1      |
        #| landuse | street                  | 1      |
        #| landuse | traffic_island          | 1      |
        #| landuse | unknown                 | 1      |
        #| landuse | water_wellfield         | 1      |
        #| landuse | winter_sports           | 1      |
        #| landuse | wood yard               | 1      |
        #+---------+-------------------------+--------+
    #
    # 2. Streets
    #
    query = """
    SELECT way_id
    FROM highway
    WHERE max_lon>=? AND min_lon<=?
     AND  max_lat>=? AND min_lat<=?
    """
    db.execute(query, (min_lon, max_lon, min_lat, max_lat))
    for (way_id,) in db.fetchall():
        # highway value
        query2 = "SELECT value FROM way_tags WHERE way_id=? AND key='highway'"
        db.execute(query2, (way_id,))
        highway_value = db.fetchone()[0]    # Wenn Rückgabe nur eine Zeile mit einer Spalte
        # coordinates of the way
        query3 = """
        SELECT n.lon,n.lat
        FROM way_nodes AS wn
        LEFT JOIN nodes AS n ON wn.node_id=n.node_id
        WHERE wn.way_id=?
        ORDER BY wn.node_order
        """
        db.execute(query3, (way_id,))
        coord_list = ()
        for (lon, lat) in db.fetchall():
            coord_list = coord_list + ( lon2px(lon), lat2px(lat) )
        # print line
        if highway_value == 'track':
            cv.create_line(coord_list, fill='#a5832c', width=2, dash='9 3')
        elif highway_value == 'service':
            cv.create_line(coord_list, fill='#cccccc', width=8)
            cv.create_line(coord_list, fill='#ffffff', width=6)
        elif highway_value in ('residential', 'unclassified'):
            cv.create_line(coord_list, fill='#cccccc', width=14)
            cv.create_line(coord_list, fill='#ffffff', width=12)
        elif highway_value in('living_street', 'pedestrian'):
            cv.create_line(coord_list, fill='#c4c4c4', width=14)
            cv.create_line(coord_list, fill='#ededed', width=12)
        elif highway_value in ('path', 'footway'):
            cv.create_line(coord_list, fill='#ffffff', width=2)
            cv.create_line(coord_list, fill='#fa8274', width=2, dash='4 4')
        elif highway_value == 'steps':
            cv.create_line(coord_list, fill='#ffffff', width=5)
            cv.create_line(coord_list, fill='#fa8274', width=5, dash='2 2')
        elif highway_value == 'cycleway':
            cv.create_line(coord_list, fill='#ffffff', width=2)
            cv.create_line(coord_list, fill='#0e0efe', width=2, dash='4 4')
        elif highway_value in ('tertiary', 'tertiary_link'):
            cv.create_line(coord_list, fill='#888888', width=18)
            cv.create_line(coord_list, fill='#ffffff', width=16)
        elif highway_value in ('secondary', 'secondary_link'):
            cv.create_line(coord_list, fill='#888888', width=18)
            cv.create_line(coord_list, fill='#f7fabf', width=16)
        elif highway_value in ('trunk', 'trunk_link'):
            cv.create_line(coord_list, fill='#888888', width=18)
            cv.create_line(coord_list, fill='#f9b29c', width=16)
        elif highway_value in ('primary', 'primary_link'):
            cv.create_line(coord_list, fill='#a26e04', width=14)
            cv.create_line(coord_list, fill='#fcd6a4', width=12)
        elif highway_value in ('motorway', 'motorway_link'):
            cv.create_line(coord_list, fill='#de3a71', width=18)
            cv.create_line(coord_list, fill='#e892a2', width=16)
        else:
            print("highway_value '"+highway_value+"' not yet defined")
            cv.create_line(coord_list, fill='#ff016a', width=4)
        # TODO Text Test
        #cv.create_text(300, 300, text='Streetname', anchor='nw', font='TkMenuFont', fill='red')
        # outline: https://stackoverflow.com/questions/23655029/tkinter-add-stroke-to-text
        #+---------+----------------+--------+
        #|   key   |     value      | number |
        #+---------+----------------+--------+
        #| highway | track          | 164099 | OK
        #| highway | service        | 83547  | OK
        #| highway | residential    | 58081  | OK
        #| highway | path           | 45078  | OK
        #| highway | footway        | 42081  | OK
        #| highway | tertiary       | 13730  | OK
        #| highway | secondary      | 13312  | OK
        #| highway | unclassified   | 12810  | OK
        #| highway | primary        | 9451   | OK
        #| highway | steps          | 8191   | OK
        #| highway | living_street  | 3133   | OK
        #| highway | cycleway       | 3064   | OK
        #| highway | pedestrian     | 2253   | OK
        #| highway | trunk          | 1484   | OK
        #| highway | motorway       | 1390   | OK
        #| highway | primary_link   | 1011   | OK
        #| highway | motorway_link  | 820    | OK
        #| highway | trunk_link     | 729    | OK
        #| highway | platform       | 613    |
        #| highway | secondary_link | 516    | OK
        #| highway | tertiary_link  | 349    | OK
        #| highway | construction   | 230    |
        #| highway | proposed       | 217    |
        #| highway | rest_area      | 98     |
        #| highway | bridleway      | 43     |
        #| highway | raceway        | 33     |
        #| highway | corridor       | 32     |
        #| highway | road           | 32     |
        #| highway | bus_stop       | 28     |
        #| highway | services       | 22     |
        #| highway | razed          | 9      |
        #| highway | elevator       | 6      |
        #| highway | via_ferrata    | 4      |
        #| highway | escape         | 3      |
        #| highway | passing_place  | 3      |
        #| highway | abandoned      | 2      |
        #| highway | turning_circle | 2      |
        #| highway | disused        | 1      |
        #| highway | emergency_bay  | 1      |
        #+---------+----------------+--------+

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
root.bind('<Up>', move_up)
root.bind('<Left>', move_left)
root.bind('<Right>', move_right)
root.bind('<Down>', move_down)

#
draw_map()

#
root.mainloop()

