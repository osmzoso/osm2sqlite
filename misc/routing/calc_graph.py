#!/usr/bin/env python
#
# Calculation of a simple graph for routing purposes
#
import sys, sqlite3, math

if len(sys.argv)!=2:
    print('''
    Calculate routing data.
    Usage:
    calc_graph.py DATABASE
    ''')
    sys.exit(1)

#
print("add experimental table 'graph'...")

def distance(lon1, lat1, lon2, lat2):
    """
    Calculates the great circle distance between two points on the Earth.
    Coordinates are to be given in degrees.
    Return is the distance in meters.
    """
    # Avoid a math.acos ValueError if the two points are identical
    if lon1 == lon2 and lat1 == lat2:
        return 0
    # Conversion degree to radians
    lon1 = math.radians(lon1)
    lat1 = math.radians(lat1)
    lon2 = math.radians(lon2)
    lat2 = math.radians(lat2)
    # Great circle with earth radius Europe 6371 km (alternatively radius equator 6378 km)
    dist =  math.acos(
                math.sin(lat1) * math.sin(lat2) +
                math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
            ) * 6371000
    return dist

# database connection
db_connect = sqlite3.connect(sys.argv[1])
db = db_connect.cursor()   # new database cursor

db.execute('''
/*
** 1. Determine all nodes of ways with key='highway'
*/
CREATE TEMP TABLE highway_nodes AS
SELECT wn.node_id,t.way_id
FROM way_tags AS t
LEFT JOIN way_nodes AS wn ON t.way_id=wn.way_id
WHERE t.key='highway';
''')

db.execute('''
/*
** 2. Create a table with all nodes that are crossing points
*/
CREATE TEMP TABLE highway_nodes_crossing AS
SELECT node_id
FROM highway_nodes
GROUP BY node_id HAVING count(*)>1;
''')
db.execute('''
CREATE INDEX hnc_tmp ON highway_nodes_crossing (node_id);
''')

db.execute('''
/*
** 3. Delete temporary table
*/
DROP TABLE highway_nodes;
''')

#
#
#
##db.execute('BEGIN TRANSACTION')
db.execute('DROP TABLE IF EXISTS graph')
db.execute('''
CREATE TABLE graph (
 node_id_from INTEGER,              -- node ID start
 node_id_to   INTEGER,              -- node ID end
 dist         INTEGER,              -- distance in meters
 way_id       INTEGER               -- way ID
)
''')

#
#
#
prev_lon = 0
prev_lat = 0
prev_way_id = -1
prev_node_id = -1

edge_active = False
node_id_from = -1
dist = 0

db.execute('''
SELECT DISTINCT
 wn.way_id,wn.node_id,wn.node_order,
 ifnull(hnc.node_id,0) AS node_id_crossing,
 n.lon,n.lat
FROM way_tags AS wt
LEFT JOIN way_nodes AS wn ON wt.way_id=wn.way_id
LEFT JOIN highway_nodes_crossing AS hnc ON wn.node_id=hnc.node_id
LEFT JOIN nodes AS n ON wn.node_id=n.node_id
WHERE wt.key='highway'
ORDER BY wn.way_id,wn.node_order
--LIMIT 1000
''')
debug = False                                                                                              # DEBUG CODE
for (way_id, node_id, node_order,
     node_id_crossing, lon, lat) in db.fetchall():
    #
    # Wenn neuer way aber noch Reste von vorigem way vorhanden sind dann neue Kante anlegen
    #
    if way_id != prev_way_id and edge_active:
        if debug:                                                                                          # DEBUG CODE
            print('=> edge rest:', node_id_from, prev_node_id, round(dist), prev_way_id)                   # DEBUG CODE
        db.execute('INSERT INTO graph (node_id_from,node_id_to,dist,way_id) VALUES (?,?,?,?)',
         (node_id_from, prev_node_id, round(dist), prev_way_id))
        edge_active = False
    #
    prev_dist = distance(prev_lon, prev_lat, lon, lat)
    dist = dist + prev_dist
    #                                                                                                      # DEBUG CODE
    if debug:                                                                                              # DEBUG CODE
        print("%12d" % (way_id), "%12d" % (node_id), "%5d" % (node_order),                                 # DEBUG CODE
              "%12d" % (node_id_crossing), "%12.7f" % (lon), "%12.7f" % (lat),                             # DEBUG CODE
              "prev_dist: %12.7f" % (prev_dist), sep=' ')                                                  # DEBUG CODE
    #
    edge_active = True
    #
    # Wenn sich way_id ändert oder crossing node vorhanden ist dann
    # beginnt oder endet eine Kante.
    #
    if way_id != prev_way_id:
        node_id_from = node_id
        dist = 0
        prev_dist = 0
    if node_id_crossing > 0 and way_id == prev_way_id:
        if node_id_from != -1:
            if debug:                                                                                      # DEBUG CODE
                print('=> edge:', node_id_from, node_id, round(dist), way_id)                              # DEBUG CODE
            db.execute('INSERT INTO graph (node_id_from,node_id_to,dist,way_id) VALUES (?,?,?,?)',
             (node_id_from, node_id, round(dist), way_id))
            edge_active = False
        node_id_from = node_id
        dist = 0
        prev_dist = 0
    #
    prev_lon = lon
    prev_lat = lat
    prev_way_id = way_id
    prev_node_id = node_id

if edge_active:
    if debug:                                                                                              # DEBUG CODE
        print('=> edge last:', node_id_from, node_id, round(dist), way_id)                                 # DEBUG CODE
    db.execute('INSERT INTO graph (node_id_from,node_id_to,dist,way_id) VALUES (?,?,?,?)',
     (node_id_from, node_id, round(dist), way_id))

# write data to database
##db.execute('COMMIT')
db_connect.commit()

