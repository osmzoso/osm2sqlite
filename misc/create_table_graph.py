#!/usr/bin/env python
#
# Calculation of a simple graph for routing purposes
#
import sys, sqlite3, math

if len(sys.argv)!=2:
    print(f'''
    Creates a table 'graph' in the database.
    The table contains all the edges of the graph.
    Usage:
    {sys.argv[0]} DATABASE
    ''')
    sys.exit(1)

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

def add_graph():
    db.execute('''
    CREATE TABLE graph (
     edge_id    INTEGER PRIMARY KEY,  -- edge ID
     edge_start INTEGER,              -- edge start node ID
     edge_end   INTEGER,              -- edge end node ID
     dist       INTEGER,              -- distance in meters
     way_id     INTEGER               -- way ID
    )
    ''')
    #
    # Create a table with all nodes that are crossing points
    #
    db.execute('''
    CREATE TEMP TABLE highway_nodes_crossing
    (
     node_id INTEGER PRIMARY KEY
    )
    ''')
    db.execute('''
    INSERT INTO highway_nodes_crossing
    SELECT node_id FROM
    (
     SELECT wn.node_id
     FROM way_tags AS wt
     LEFT JOIN way_nodes AS wn ON wt.way_id=wn.way_id
     WHERE wt.key='highway'
    ) AS t1
    GROUP BY node_id HAVING count(*)>1
    ''')
    #
    db.execute('''
    SELECT
     wn.way_id,wn.node_id,wn.node_order,
     ifnull(hnc.node_id,-1) AS node_id_crossing,
     n.lon,n.lat
    FROM way_tags AS wt
    LEFT JOIN way_nodes AS wn ON wt.way_id=wn.way_id
    LEFT JOIN highway_nodes_crossing AS hnc ON wn.node_id=hnc.node_id
    LEFT JOIN nodes AS n ON wn.node_id=n.node_id
    WHERE wt.key='highway'
    ORDER BY wn.way_id,wn.node_order
    ''')
    prev_lon = 0
    prev_lat = 0
    prev_way_id = -1
    prev_node_id = -1
    edge_active = False
    edge_start = -1
    dist = 0
    for (way_id, node_id, node_order, node_id_crossing, lon, lat) in db.fetchall():
        #print(format(way_id, '12d'),
        #      format(node_id, '12d'),
        #      format(node_order, '5d'),
        #      format(node_id_crossing, '12d'),
        #      format(lon,'15.7f'),
        #      format(lat,'15.7f'))
        #
        # If a new way is active but there are still remnants of the previous way, create a new edge.
        #
        if way_id != prev_way_id and edge_active:
            db.execute('INSERT INTO graph (edge_start,edge_end,dist,way_id) VALUES (?,?,?,?)',
             (edge_start, prev_node_id, round(dist), prev_way_id))
            edge_active = False
        #
        dist = dist + distance(prev_lon, prev_lat, lon, lat)
        #
        edge_active = True
        #
        # If way_id changes or crossing node is present then an edge begins or ends.
        #
        if way_id != prev_way_id:
            edge_start = node_id
            dist = 0
        if node_id_crossing > -1 and way_id == prev_way_id:
            if edge_start != -1:
                db.execute('INSERT INTO graph (edge_start,edge_end,dist,way_id) VALUES (?,?,?,?)',
                 (edge_start, node_id, round(dist), way_id))
                edge_active = False
            edge_start = node_id
            dist = 0
        #
        prev_lon = lon
        prev_lat = lat
        prev_way_id = way_id
        prev_node_id = node_id
    #
    if edge_active:
        db.execute('INSERT INTO graph (edge_start,edge_end,dist,way_id) VALUES (?,?,?,?)',
         (edge_start, node_id, round(dist), way_id))
    #
    db.execute('CREATE INDEX graph__way_id ON graph (way_id)')
    # write data to database
    db_connect.commit()

# database connection
db_connect = sqlite3.connect(sys.argv[1])
db = db_connect.cursor()   # new database cursor

print("add experimental table 'graph'...")
db.execute('DROP TABLE IF EXISTS graph')
add_graph()

