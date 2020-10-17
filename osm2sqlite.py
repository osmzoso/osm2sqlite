#!/usr/bin/python3
#
# Reads OpenStreetMap data in XML format into a SQLite database
#
import xml.sax, sqlite3, time, sys, os

class OsmHandler( xml.sax.ContentHandler ):
    """
    Read OSM XML Data
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
if ( __name__ == "__main__"):
    # filename of the database
    filename_db = 'osm.sqlite3'
    # flags creating index
    flag_create_index   = True
    flag_create_spatial = True
    # read argv parameter
    if len(sys.argv) > 1:
        # filename of the osm xml file
        filename_xml = sys.argv[1]
        # omit creating index
        if len(sys.argv) > 2:
            if sys.argv[2] in ('--omit_spatial','-os'):
                flag_create_spatial = False
            if sys.argv[2] in ('--omit_index','-oi'):
                flag_create_index   = False
                flag_create_spatial = False
    else:
        # print help and exit
        print(__file__, '\n')
        print('Reads OpenStreetMap data in XML format into a SQLite database.', '\n')
        print('usage:')
        print('python', __file__, 'input.osm')
        print('python', __file__, 'input.osm', '[--omit_spatial|-os]')
        print('python', __file__, 'input.osm', '[--omit_index|-oi]')
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
    if flag_create_index:
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
    if flag_create_spatial:
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

