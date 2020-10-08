#!/usr/bin/python3
#
# Reads OpenStreetMap data in XML format into a SQLite database
#
import xml.sax, sqlite3, time, sys, os

class OsmHandler( xml.sax.ContentHandler ):
    def __init__(self):
        # element <node>
        self.tag_node_active = 0
        self.node_id = ''
        self.node_lon  = ''
        self.node_lat = ''
        # element <tag>
        self.tag_k = ''
        self.tag_v = ''
        # element <way>
        self.tag_way_active = 0
        self.way_node_order = 0
        self.way_id = ''
        self.way_node_id = ''
        # element <relation>
        self.tag_relation_active = 0
        self.relation_member_order = 0
        self.relation_id = ''

    # call when an element starts
    def startElement(self, tag, attributes):
        if tag == 'node':
            self.tag_node_active = 1
            self.node_id  = attributes['id']
            self.node_lon = attributes['lon']
            self.node_lat = attributes['lat']
            db.execute('INSERT INTO nodes (node_id,lon,lat) VALUES (?,?,?)',
             (self.node_id,self.node_lon,self.node_lat))
        elif tag == 'tag':
            self.tag_k =  attributes['k']
            self.tag_v =  attributes['v']
            if self.tag_node_active == 1:
                db.execute('INSERT INTO node_tags (node_id,key,value) VALUES (?,?,?)',
                 (self.node_id,self.tag_k,self.tag_v))
            elif self.tag_way_active == 1:
                db.execute('INSERT INTO way_tags (way_id,key,value) VALUES (?,?,?)',
                 (self.way_id,self.tag_k,self.tag_v))
            elif self.tag_relation_active == 1:
                db.execute('INSERT INTO relation_tags (relation_id,key,value) VALUES (?,?,?)',
                 (self.relation_id,self.tag_k,self.tag_v))
        elif tag == 'way':
            self.tag_way_active = 1
            self.way_id = attributes['id']
        elif tag == 'nd':
            way_node_id = attributes['ref']
            self.way_node_order += 1
            db.execute('INSERT INTO way_nodes (way_id,node_id,node_order) VALUES (?,?,?)',
             (self.way_id,way_node_id,self.way_node_order))
        elif tag == 'relation':
            self.tag_relation_active = 1
            self.relation_id = attributes['id']
        elif tag == 'member':
            member_type = attributes['type']
            member_ref  = attributes['ref']
            member_role = attributes['role']
            self.relation_member_order += 1
            db.execute('INSERT INTO relation_members (relation_id,type,ref,role,member_order) VALUES (?,?,?,?,?)',
             (self.relation_id,member_type,member_ref,member_role,self.relation_member_order))

    # call when an element ends
    def endElement(self, tag):
        if tag == 'node':
            self.tag_node_active = 0
        elif tag == 'way':
            self.tag_way_active = 0
            self.way_node_order = 0
        elif tag == 'relation':
            self.tag_relation_active = 0
            self.relation_member_order = 0

#
# Main
#
if ( __name__ == "__main__"):
    # file name of the database
    filename_db = 'osm.sqlite3'
    # read the file name of the osm xml data
    if len(sys.argv) > 1:
        filename_xml = sys.argv[1]
    else:
        print('No file name specified')
        sys.exit(1)
    # delete old database file if exists
    if os.path.exists(filename_db):
        os.remove(filename_db)
        print('existing database file '+filename_db+' removed')
    # connect to the database
    db_connect = sqlite3.connect(filename_db)
    db = db_connect.cursor()   # new database cursor
    # start
    print( time.strftime('%H:%M:%S', time.localtime()), 'reading '+filename_xml+'...')
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
    print( time.strftime('%H:%M:%S', time.localtime()), 'creating index...')
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
    print( time.strftime('%H:%M:%S', time.localtime()), 'creating R*Tree "highway"...')
    db.execute('''
    CREATE VIRTUAL TABLE highway USING rtree( way_id,min_lat, max_lat,min_lon, max_lon )
    ''')
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
    # finish
    print( time.strftime('%H:%M:%S', time.localtime()), 'reading finished')

