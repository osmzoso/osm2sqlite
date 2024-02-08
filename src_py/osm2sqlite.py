#!/usr/bin/env python
"""
osm2sqlite - Reads OpenStreetMap XML data into a SQLite database

Copyright (C) 2021-2024 Herbert Gläser
"""
import sys
import xml.sax
import sqlite3
import math

db_connect = None  # SQLite Database connection
db = None          # SQLite Database cursor


def show_help():
    """Show built-in help"""
    print('osm2sqlite.py 0.9.2\n'
          '\n'
          'Reads OpenStreetMap XML data into a SQLite database.\n'
          '\n'
          'Usage:\n'
          f'{sys.argv[0]} SQLITE_DATABASE OSM_XML_FILE [OPTION]...\n'
          '\n'
          'Options:\n'
          '  rtree         Add R*Tree indexes\n'
          '  addr          Add address tables\n'
          '  graph         Add graph table\n'
          '  noindex       Do not create indexes (not recommended)\n'
          '\n'
          'When OSM_XML_FILE is -, read standard input.')
    print('\n(SQLite '+sqlite3.sqlite_version+' is used)\n')


class OsmHandler(xml.sax.ContentHandler):
    """
    Read OpenStreetMap XML Data
    """
    def __init__(self):
        # element <node>
        self.element_node_active = False
        self.node_id = -1
        # element <way>
        self.element_way_active = False
        self.way_id = -1
        self.way_node_order = 0
        # element <relation>
        self.element_relation_active = False
        self.relation_id = -1
        self.relation_member_order = 0

    # call when an element starts
    def startElement(self, element, attrib):
        if element == 'node':
            self.element_node_active = True
            self.node_id = attrib['id']
            db.execute('INSERT INTO nodes (node_id,lon,lat) VALUES (?,?,?)',
                       (self.node_id, attrib['lon'], attrib['lat']))
        elif element == 'tag':
            if self.element_node_active:
                db.execute('INSERT INTO node_tags (node_id,key,value) VALUES (?,?,?)',
                           (self.node_id, attrib['k'], attrib['v']))
            elif self.element_way_active:
                db.execute('INSERT INTO way_tags (way_id,key,value) VALUES (?,?,?)',
                           (self.way_id, attrib['k'], attrib['v']))
            elif self.element_relation_active:
                db.execute('INSERT INTO relation_tags (relation_id,key,value) VALUES (?,?,?)',
                           (self.relation_id, attrib['k'], attrib['v']))
        elif element == 'way':
            self.element_way_active = True
            self.way_id = attrib['id']
        elif element == 'nd':
            self.way_node_order += 1
            db.execute('INSERT INTO way_nodes (way_id,node_id,node_order) VALUES (?,?,?)',
                       (self.way_id, attrib['ref'], self.way_node_order))
        elif element == 'relation':
            self.element_relation_active = True
            self.relation_id = attrib['id']
        elif element == 'member':
            self.relation_member_order += 1
            db.execute('INSERT INTO relation_members (relation_id,ref,ref_id,role,member_order) VALUES (?,?,?,?,?)',
                       (self.relation_id, attrib['type'], attrib['ref'], attrib['role'], self.relation_member_order))

    # call when an element ends
    def endElement(self, element):
        if element == 'node':
            self.element_node_active = False
            self.node_id = -1
        elif element == 'way':
            self.element_way_active = False
            self.way_id = -1
            self.way_node_order = 0
        elif element == 'relation':
            self.element_relation_active = False
            self.relation_id = -1
            self.relation_member_order = 0


def add_tables():
    db.execute('''
    CREATE TABLE nodes (
     node_id      INTEGER PRIMARY KEY,  -- node ID
     lon          REAL,                 -- longitude
     lat          REAL                  -- latitude
    )
    ''')
    db.execute('''
    CREATE TABLE node_tags (
     node_id      INTEGER,              -- node ID
     key          TEXT,                 -- tag key
     value        TEXT                  -- tag value
    )
    ''')
    db.execute('''
    CREATE TABLE way_nodes (
     way_id       INTEGER,              -- way ID
     node_id      INTEGER,              -- node ID
     node_order   INTEGER               -- node order
    )
    ''')
    db.execute('''
    CREATE TABLE way_tags (
     way_id       INTEGER,              -- way ID
     key          TEXT,                 -- tag key
     value        TEXT                  -- tag value
    )
    ''')
    db.execute('''
    CREATE TABLE relation_members (
     relation_id  INTEGER,              -- relation ID
     ref          TEXT,                 -- reference ('node','way','relation')
     ref_id       INTEGER,              -- node, way or relation ID
     role         TEXT,                 -- describes a particular feature
     member_order INTEGER               -- member order
    )
    ''')
    db.execute('''
    CREATE TABLE relation_tags (
     relation_id  INTEGER,              -- relation ID
     key          TEXT,                 -- tag key
     value        TEXT                  -- tag value
    )
    ''')


def add_index():
    db.execute('CREATE INDEX node_tags__node_id            ON node_tags (node_id)')
    db.execute('CREATE INDEX node_tags__key                ON node_tags (key)')
    db.execute('CREATE INDEX way_tags__way_id              ON way_tags (way_id)')
    db.execute('CREATE INDEX way_tags__key                 ON way_tags (key)')
    db.execute('CREATE INDEX way_nodes__way_id             ON way_nodes (way_id, node_order)')
    db.execute('CREATE INDEX way_nodes__node_id            ON way_nodes (node_id)')
    db.execute('CREATE INDEX relation_members__relation_id ON relation_members (relation_id, member_order)')
    db.execute('CREATE INDEX relation_members__ref_id      ON relation_members (ref_id)')
    db.execute('CREATE INDEX relation_tags__relation_id    ON relation_tags (relation_id)')
    db.execute('CREATE INDEX relation_tags__key            ON relation_tags (key)')
    db_connect.commit()


def add_rtree():
    db.execute('CREATE VIRTUAL TABLE rtree_way USING rtree(way_id, min_lat, max_lat, min_lon, max_lon)')
    db.execute('''
    INSERT INTO rtree_way (way_id, min_lat, max_lat, min_lon, max_lon)
    SELECT way_nodes.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)
    FROM way_nodes
    LEFT JOIN nodes ON way_nodes.node_id=nodes.node_id
    GROUP BY way_nodes.way_id
    ''')
    db.execute('CREATE VIRTUAL TABLE rtree_node USING rtree(node_id, min_lat, max_lat, min_lon, max_lon)')
    db.execute('''
    INSERT INTO rtree_node (node_id, min_lat, max_lat, min_lon, max_lon)
    SELECT DISTINCT nodes.node_id,nodes.lat,nodes.lat,nodes.lon,nodes.lon
    FROM nodes
    LEFT JOIN node_tags ON nodes.node_id=node_tags.node_id
    WHERE node_tags.node_id IS NOT NULL
    ''')
    db_connect.commit()


def add_addr():
    db.execute('BEGIN TRANSACTION')
    #
    # Create address tables 
    #
    db.execute('''
    CREATE TABLE addr_street (
     street_id   INTEGER PRIMARY KEY, -- street ID
     postcode    TEXT,                -- postcode
     city        TEXT,                -- city name
     street      TEXT,                -- street name
     min_lon     REAL,                -- boundingbox street min longitude
     min_lat     REAL,                -- boundingbox street min latitude
     max_lon     REAL,                -- boundingbox street max longitude
     max_lat     REAL                 -- boundingbox street max latitude
    )
    ''')
    db.execute('''
    CREATE TABLE addr_housenumber (
     housenumber_id INTEGER PRIMARY KEY, -- housenumber ID
     street_id      INTEGER,             -- street ID
     housenumber    TEXT,                -- housenumber
     lon            REAL,                -- longitude
     lat            REAL,                -- latitude
     way_id         INTEGER,             -- way ID
     node_id        INTEGER              -- node ID
    )
    ''')
    db.execute('''
    CREATE VIEW addr_view AS
    SELECT s.street_id,s.postcode,s.city,s.street,h.housenumber,h.lon,h.lat,h.way_id,h.node_id
    FROM addr_street AS s
    LEFT JOIN addr_housenumber AS h ON s.street_id=h.street_id
    ''')
    #
    # 1. Determine address data from way tags
    #
    db.execute('''
    CREATE TEMP TABLE tmp_addr_way (
     way_id      INTEGER PRIMARY KEY,
     postcode    TEXT,
     city        TEXT,
     street      TEXT,
     housenumber TEXT
    )
    ''')
    db.execute('''
    INSERT INTO tmp_addr_way
     SELECT way_id,value AS postcode,'','',''
     FROM way_tags WHERE key='addr:postcode'
     ON CONFLICT(way_id) DO UPDATE SET postcode=excluded.postcode
    ''')
    db.execute('''
    INSERT INTO tmp_addr_way
     SELECT way_id,'',value AS city,'',''
     FROM way_tags WHERE key='addr:city'
     ON CONFLICT(way_id) DO UPDATE SET city=excluded.city
    ''')
    db.execute('''
    INSERT INTO tmp_addr_way
     SELECT way_id,'','',value AS street,''
     FROM way_tags WHERE key='addr:street'
     ON CONFLICT(way_id) DO UPDATE SET street=excluded.street
    ''')
    db.execute('''
    INSERT INTO tmp_addr_way
     SELECT way_id,'','','',value AS housenumber
     FROM way_tags WHERE key='addr:housenumber'
     ON CONFLICT(way_id) DO UPDATE SET housenumber=excluded.housenumber
    ''')
    #
    # 2. Calculate coordinates of address data from way tags
    #
    db.execute('''
    CREATE TEMP TABLE tmp_addr_way_coordinates AS
    SELECT way.way_id AS way_id,round(avg(n.lon),7) AS lon,round(avg(n.lat),7) AS lat
    FROM tmp_addr_way AS way
    LEFT JOIN way_nodes AS wn ON way.way_id=wn.way_id
    LEFT JOIN nodes     AS n  ON wn.node_id=n.node_id
    GROUP BY way.way_id
    ''')
    db.execute('CREATE INDEX tmp_addr_way_coordinates_way_id ON tmp_addr_way_coordinates (way_id)')
    #
    # 3. Determine address data from node tags
    #
    db.execute('''
    CREATE TEMP TABLE tmp_addr_node (
     node_id     INTEGER PRIMARY KEY,
     postcode    TEXT,
     city        TEXT,
     street      TEXT,
     housenumber TEXT
    )
    ''')
    db.execute('''
    INSERT INTO tmp_addr_node
     SELECT node_id,value AS postcode,'','',''
     FROM node_tags WHERE key='addr:postcode'
     ON CONFLICT(node_id) DO UPDATE SET postcode=excluded.postcode
    ''')
    db.execute('''
    INSERT INTO tmp_addr_node
     SELECT node_id,'',value AS city,'',''
     FROM node_tags WHERE key='addr:city'
     ON CONFLICT(node_id) DO UPDATE SET city=excluded.city
    ''')
    db.execute('''
    INSERT INTO tmp_addr_node
     SELECT node_id,'','',value AS street,''
     FROM node_tags WHERE key='addr:street'
     ON CONFLICT(node_id) DO UPDATE SET street=excluded.street
    ''')
    db.execute('''
    INSERT INTO tmp_addr_node
     SELECT node_id,'','','',value AS housenumber
     FROM node_tags WHERE key='addr:housenumber'
     ON CONFLICT(node_id) DO UPDATE SET housenumber=excluded.housenumber
    ''')
    #
    # 4. Create temporary overall table with all addresses
    #
    db.execute('''
    CREATE TEMP TABLE tmp_addr (
     addr_id     INTEGER PRIMARY KEY,
     way_id      INTEGER,
     node_id     INTEGER,
     postcode    TEXT,
     city        TEXT,
     street      TEXT,
     housenumber TEXT,
     lon         REAL,
     lat         REAL
    )
    ''')
    db.execute('''
    INSERT INTO tmp_addr (way_id,node_id,postcode,city,street,housenumber,lon,lat)
     SELECT w.way_id,-1 AS node_id,w.postcode,w.city,w.street,w.housenumber,c.lon,c.lat
     FROM tmp_addr_way AS w
     LEFT JOIN tmp_addr_way_coordinates AS c ON w.way_id=c.way_id
    UNION ALL
     SELECT -1 AS way_id,n.node_id,n.postcode,n.city,n.street,n.housenumber,c.lon,c.lat
     FROM tmp_addr_node AS n
     LEFT JOIN nodes AS c ON n.node_id=c.node_id
    ORDER BY postcode,city,street,housenumber
    ''')
    #
    # 5. Fill tables 'addr_street' and 'addr_housenumber'
    #
    db.execute('''
    INSERT INTO addr_street (postcode,city,street,min_lon,min_lat,max_lon,max_lat)
     SELECT postcode,city,street,min(lon),min(lat),max(lon),max(lat)
     FROM tmp_addr
     GROUP BY postcode,city,street
    ''')
    db.execute('CREATE INDEX addr_street__postcode_city_street ON addr_street (postcode,city,street)')
    db.execute('''
    INSERT INTO addr_housenumber (street_id,housenumber,lon,lat,way_id,node_id)
     SELECT s.street_id,a.housenumber,a.lon,a.lat,a.way_id,a.node_id
     FROM tmp_addr AS a
     LEFT JOIN addr_street AS s ON a.postcode=s.postcode AND a.city=s.city AND a.street=s.street
    ''')
    db.execute('CREATE INDEX addr_housenumber__street_id ON addr_housenumber (street_id)')
    #
    # 6. Delete temporary tables
    #
    db.execute('DROP TABLE tmp_addr_way')
    db.execute('DROP TABLE tmp_addr_way_coordinates')
    db.execute('DROP TABLE tmp_addr_node')
    db.execute('DROP TABLE tmp_addr')
    db.execute('COMMIT TRANSACTION')


def distance(lon1, lat1, lon2, lat2):
    """Calculates great circle distance between two coordinates in degrees"""
    # Avoid a math.acos ValueError if the two points are identical
    if lon1 == lon2 and lat1 == lat2:
        return 0
    lon1 = math.radians(lon1)   # Conversion degree to radians
    lat1 = math.radians(lat1)
    lon2 = math.radians(lon2)
    lat2 = math.radians(lat2)
    # Use earth radius Europe 6371 km (alternatively radius equator 6378 km)
    dist = math.acos(
                math.sin(lat1) * math.sin(lat2) +
                math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
            ) * 6371000
    return dist     # distance in meters


def add_graph():
    db.execute('BEGIN TRANSACTION')
    db.execute('''
    CREATE TABLE graph (
     edge_id       INTEGER PRIMARY KEY,  -- edge ID
     start_node_id INTEGER,              -- edge start node ID
     end_node_id   INTEGER,              -- edge end node ID
     dist          INTEGER,              -- distance in meters
     way_id        INTEGER               -- way ID
    )
    ''')
    # Create a table with all nodes that are crossing points
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
    )
    GROUP BY node_id HAVING count(*)>1
    ''')
    #
    prev_lon = 0
    prev_lat = 0
    prev_way_id = -1
    prev_node_id = -1
    edge_active = False
    start_node_id = -1
    dist = 0
    db.execute('''
    SELECT
     wn.way_id,wn.node_id,
     ifnull(hnc.node_id,-1) AS node_id_crossing,
     n.lon,n.lat
    FROM way_tags AS wt
    LEFT JOIN way_nodes AS wn ON wt.way_id=wn.way_id
    LEFT JOIN highway_nodes_crossing AS hnc ON wn.node_id=hnc.node_id
    LEFT JOIN nodes AS n ON wn.node_id=n.node_id
    WHERE wt.key='highway'
    ORDER BY wn.way_id,wn.node_order
    ''')
    for (way_id, node_id, node_id_crossing, lon, lat) in db.fetchall():
        # If a new way is active but there are still remnants of the previous way, create a new edge.
        if way_id != prev_way_id and edge_active:
            db.execute('INSERT INTO graph (start_node_id,end_node_id,dist,way_id) VALUES (?,?,?,?)',
                       (start_node_id, prev_node_id, round(dist), prev_way_id))
            edge_active = False
        dist = dist + distance(prev_lon, prev_lat, lon, lat)
        edge_active = True
        # If way_id changes or crossing node is present then an edge begins or ends.
        if way_id != prev_way_id:
            start_node_id = node_id
            dist = 0
        if node_id_crossing > -1 and way_id == prev_way_id:
            if start_node_id != -1:
                db.execute('INSERT INTO graph (start_node_id,end_node_id,dist,way_id) VALUES (?,?,?,?)',
                           (start_node_id, node_id, round(dist), way_id))
                edge_active = False
            start_node_id = node_id
            dist = 0
        prev_lon = lon
        prev_lat = lat
        prev_way_id = way_id
        prev_node_id = node_id
    if edge_active:
        db.execute('INSERT INTO graph (start_node_id,end_node_id,dist,way_id) VALUES (?,?,?,?)',
                   (start_node_id, node_id, round(dist), way_id))
    db.execute('CREATE INDEX graph__way_id ON graph (way_id)')
    db.execute('COMMIT TRANSACTION')


def main():
    global db_connect, db
    if len(sys.argv) < 3:
        show_help()
        sys.exit(1)
    # check options
    index = True
    rtree = False
    addr = False
    graph = False
    if len(sys.argv) > 3:
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == 'noindex':
                index = False
            elif sys.argv[i] == 'rtree':
                rtree = True
            elif sys.argv[i] == 'addr':
                addr = True
            elif sys.argv[i] == 'graph':
                graph = True
            else:
                print("abort - option '"+sys.argv[i]+"' unknown")
                sys.exit(1)
    # connect to the database
    db_connect = sqlite3.connect(sys.argv[1])
    db = db_connect.cursor()   # new database cursor
    # tuning database
    db.execute('PRAGMA journal_mode = OFF')
    db.execute('PRAGMA page_size = 65536')
    # create all tables
    add_tables()
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContentHandler
    handler = OsmHandler()
    parser.setContentHandler(handler)
    # parse osm xml data
    if sys.argv[2] == '-':
        parser.parse(sys.stdin)
    else:
        parser.parse(sys.argv[2])
    # write data to database
    db_connect.commit()
    # create index
    if index:
        add_index()
    if rtree:
        add_rtree()
    if addr:
        add_addr()
    if graph:
        add_graph()
    db_connect.commit()


if __name__ == "__main__":
    main()
