#!/usr/bin/python3
#
# Import of OpenStreetMap data in XML format into a SQLite database
#
import xml.sax, sqlite3, time, sys

class OsmHandler( xml.sax.ContentHandler ):
    def __init__(self):
        # tag <node>
        self.tag_node_active = 0
        self.node_id = ''
        self.node_lat = ''
        self.node_lon  = ''
        # tag <tag>
        self.tag_k = ''
        self.tag_v = ''
        # tag <way>
        self.tag_way_active = 0
        self.way_local_order = 0
        self.way_id = ''
        self.way_node_id = ''

    # call when an element starts
    def startElement(self, tag, attributes):
        if tag == 'node':
            self.tag_node_active = 1
            self.node_id  = attributes['id']
            self.node_lat = attributes['lat']
            self.node_lon = attributes['lon']
            db.execute('INSERT INTO nodes (node_id,lat,lon) VALUES (?,?,?)',
             (self.node_id,self.node_lat,self.node_lon))
        if tag == 'tag':
            self.tag_k =  attributes['k']
            self.tag_v =  attributes['v']
            if self.tag_node_active == 1:
                db.execute('INSERT INTO node_tags (node_id,key,value) VALUES (?,?,?)',
                 (self.node_id,self.tag_k,self.tag_v))
            elif self.tag_way_active == 1:
                db.execute('INSERT INTO way_tags (way_id,key,value) VALUES (?,?,?)',
                 (self.way_id,self.tag_k,self.tag_v))
        if tag == 'way':
            self.tag_way_active = 1
            self.way_id = attributes['id']
        if tag == 'nd':
            way_node_id = attributes['ref']
            self.way_local_order += 1
            db.execute('INSERT INTO way_nodes (way_id,local_order,node_id) VALUES (?,?,?)',
             (self.way_id,self.way_local_order,way_node_id))

    # call when an element ends
    def endElement(self, tag):
        if tag == 'node':
            self.tag_node_active = 0
        elif tag == 'way':
            self.tag_way_active = 0
            self.way_local_order = 0

#
# Main
#
if ( __name__ == "__main__"):

    # read filename
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print('No file name specified')
        sys.exit(1)
    # time measurement
    start_time = time.time()
    # connect to the database
    db_connect = sqlite3.connect('osm.sqlite3')
    db = db_connect.cursor()   # new database cursor
    # create all tables
    db.execute('DROP TABLE IF EXISTS nodes')
    db.execute('''
    CREATE TABLE nodes (
     node_id INTEGER PRIMARX KEY,  -- node ID
     lat     REAL,                 -- latitude
     lon     REAL                  -- longitude
    )
    ''')
    db.execute('DROP TABLE IF EXISTS node_tags')
    db.execute('''
    CREATE TABLE node_tags (
     node_id INTEGER,              --  node ID
     key     TEXT,                 -- tag key
     value   TEXT                  -- tag value
    )
    ''')
    db.execute('DROP TABLE IF EXISTS way_tags')
    db.execute('''
    CREATE TABLE way_tags (
     way_id INTEGER,               -- way ID
     key    TEXT,                  -- tag key
     value  TEXT                   -- tag value
    )
    ''')
    db.execute('DROP TABLE IF EXISTS way_nodes')
    db.execute('''
    CREATE TABLE way_nodes (
     way_id      INTEGER,          -- way ID
     local_order INTEGER,          -- nodes sorting
     node_id     INTEGER           -- node ID
    )
    ''')
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContentHandler
    handler = OsmHandler()
    parser.setContentHandler(handler)
    # parse osm data
    parser.parse(filename)
    # write data to database
    db_connect.commit()
    # create index
    db.execute('CREATE INDEX node_tags__node_id ON node_tags (node_id)')
    db.execute('CREATE INDEX node_tags__key     ON node_tags (key)')
    db.execute('CREATE INDEX way_tags__way_id   ON way_tags (way_id)')
    db.execute('CREATE INDEX way_tags__key      ON way_tags (key)')
    db.execute('CREATE INDEX way_nodes__way_id  ON way_nodes (way_id)')
    db.execute('CREATE INDEX way_nodes__node_id ON way_nodes (node_id)')
    #
    print('run time:', round((time.time() - start_time)/60,2), 'min' )
