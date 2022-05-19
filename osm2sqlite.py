#!/usr/bin/env python
#
# osm2sqlite - Reads OpenStreetMap XML data into a SQLite database
#
# Copyright (C) 2021-2022 Herbert Gläser
#
import xml.sax, sqlite3, sys

help = '''osm2sqlite.py 0.7.2

Reads OpenStreetMap XML data into a SQLite database.

Usage:
python osm2sqlite.py FILE_OSM_XML FILE_SQLITE_DB [INDEX]

Index control:
 -n, --no-index       No indexes are created
 -s, --spatial-index  Indexes and spatial index are created'''

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
        if   element == 'node':
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
            db.execute('INSERT INTO relation_members (relation_id,type,ref,role,member_order) VALUES (?,?,?,?,?)',
             (self.relation_id, attrib['type'], attrib['ref'], attrib['role'], self.relation_member_order))

    # call when an element ends
    def endElement(self, element):
        if   element == 'node':
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

#
# Main
#
if __name__ == '__main__':
    # flag creating index
    flag_create_index = True
    flag_create_sindex = False
    # read argv parameter
    if len(sys.argv)==3 or len(sys.argv)==4:
        # filename of the osm xml file
        filename_xml = sys.argv[1]
        filename_db  = sys.argv[2]
        # omit creating index
        if len(sys.argv)==4:
            if sys.argv[3] in ('-n','--no-index'):
                flag_create_index = False
            if sys.argv[3] in ('-s','--spatial-index'):
                flag_create_index = True
                flag_create_sindex = True
    else:
        print(help)
        sys.exit(1)
    # connect to the database
    db_connect = sqlite3.connect(filename_db)
    db = db_connect.cursor()   # new database cursor
    # tuning database
    db.execute('PRAGMA journal_mode = OFF');
    db.execute('PRAGMA page_size = 65536');
    # create all tables
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
     type         TEXT,                 -- type ('node','way','relation')
     ref          INTEGER,              -- node, way or relation ID
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
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContentHandler
    handler = OsmHandler()
    parser.setContentHandler(handler)
    # parse osm xml data
    parser.parse(filename_xml)
    # write data to database
    db_connect.commit()
    # create index
    if flag_create_index:
        db.execute('CREATE INDEX node_tags__node_id ON node_tags (node_id)')
        db.execute('CREATE INDEX node_tags__key     ON node_tags (key)')
        db.execute('CREATE INDEX way_tags__way_id   ON way_tags (way_id)')
        db.execute('CREATE INDEX way_tags__key      ON way_tags (key)')
        db.execute('CREATE INDEX way_nodes__way_id  ON way_nodes (way_id)')
        db.execute('CREATE INDEX way_nodes__node_id ON way_nodes (node_id)')
        db.execute('CREATE INDEX relation_members__relation_id ON relation_members ( relation_id )')
        db.execute('CREATE INDEX relation_members__type        ON relation_members ( type, ref )')
        db.execute('CREATE INDEX relation_tags__relation_id    ON relation_tags ( relation_id )')
        db.execute('CREATE INDEX relation_tags__key            ON relation_tags ( key )')
        db_connect.commit()
    # create spatial index
    if flag_create_sindex:
        db.execute('CREATE VIRTUAL TABLE highway USING rtree( way_id, min_lat, max_lat, min_lon, max_lon )')
        db.execute('''
        INSERT INTO highway (way_id,min_lat,       max_lat,       min_lon,       max_lon)
        SELECT      way_tags.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)
        FROM      way_tags
        LEFT JOIN way_nodes ON way_tags.way_id=way_nodes.way_id
        LEFT JOIN nodes     ON way_nodes.node_id=nodes.node_id
        WHERE way_tags.key='highway'
        GROUP BY way_tags.way_id
        ''')
        db_connect.commit()

