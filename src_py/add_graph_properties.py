#!/usr/bin/env python
"""
Klassifizierung:

car
bike_road
bike_gravel
foot

car_oneway
bike_oneway

------------------------------------------------------------
Wichtige Keys für die Klassifizierung:

highway
bicycle
surface
tracktype
cycleway:left
cycleway:right
sidewalk
oneway

Hildastraße way 27648305:
oneway            yes
oneway:bicycle    no

"""
import sys
import sqlite3

DEBUG = False


def graph_properties(db):
    db.executescript('''
    DROP TABLE IF EXISTS graph_properties;
    CREATE TABLE graph_properties (
     way_id        INTEGER PRIMARY KEY,  -- way ID
     --
     car_oneway    INTEGER,              -- 
     bike_oneway   INTEGER,              -- 
     car           INTEGER,              -- 
     bike_road     INTEGER,              -- 
     bike_gravel   INTEGER,              -- 
     foot          INTEGER,              -- 
     --
     properties    INTEGER               -- 
    );
    ''')
    db.execute('SELECT DISTINCT way_id FROM graph')
    for (way_id,) in db.fetchall():
        if DEBUG:
            print(70 * '*')
            print(way_id)
        # Flags zur Klassifizierung
        # https://stackoverflow.com/questions/12173774/how-to-modify-bits-in-an-integer
        car_oneway = False      # 2^5  32
        bike_oneway = False     # 2^4  16
        car = False             # 2^3   8
        bike_road = False       # 2^2   4
        bike_gravel = False     # 2^1   2
        foot = False            # 2^0   1
        #
        tags = []
        db.execute('SELECT key,value FROM way_tags WHERE way_id=?', (way_id,))
        for (key, value) in db.fetchall():
            tags.append(key + '=' + value)
            if DEBUG:
                print('  ', key, value)
        # print(tags)
        #
        if 'highway=motorway' in tags or \
           'highway=motorway_link' in tags or \
           'highway=trunk' in tags or \
           'highway=trunk_link' in tags:
            car = True
        if 'highway=primary' in tags or \
           'highway=primary_link' in tags or \
           'highway=secondary' in tags or \
           'highway=secondary_link' in tags or \
           'highway=tertiary' in tags or \
           'highway=tertiary_link' in tags or \
           'highway=unclassified' in tags or \
           'highway=residential' in tags:
            car = True
            bike_road = True
            bike_gravel = True
        if 'highway=residential' in tags or \
           'highway=living_street' in tags or \
           'highway=service' in tags or \
           'highway=cycleway' in tags or \
           'highway=track' in tags or \
           'highway=unclassified' in tags or \
           'bicycle=yes' in tags:
            bike_road = True
            bike_gravel = True
            foot = True
        if 'highway=pedestrian' in tags or \
           'highway=track' in tags or \
           'highway=footway' in tags or \
           'highway=steps' in tags or \
           'highway=path' in tags or \
           'sidewalk=both' in tags or \
           'sidewalk:both=yes' in tags or \
           'sidewalk=right' in tags or \
           'sidewalk:right=yes' in tags or \
           'sidewalk=left' in tags or \
           'sidewalk:left=yes' in tags or \
           'sidewalk=yes' in tags:
            foot = True
        #
        if 'surface=asphalt' not in tags:
            bike_road = False
        if 'sidewalk=separate' in tags:
            foot = False
        #
        if 'oneway=yes' in tags:
            car_oneway = True
            bike_oneway = True
        if 'oneway:bicycle=no' in tags:
            bike_oneway = False
        #
        #
        #
        properties = 2**0 * foot + \
                     2**1 * bike_gravel + \
                     2**2 * bike_road + \
                     2**3 * car + \
                     2**4 * bike_oneway + \
                     2**5 * car_oneway
        """
        Abfrage des Feld 'properties':
        foot        :    SELECT * FROM graph_properties WHERE properties & 1 = 1;
        bike_gravel :    SELECT * FROM graph_properties WHERE properties & 2 = 2;
        bike_road   :    SELECT * FROM graph_properties WHERE properties & 4 = 4;
        car         :    SELECT * FROM graph_properties WHERE properties & 4 = 4;
        """
        #
        if DEBUG:
            print(f'{"car":3} | {"bike_road":9} | {"bike_gravel":11} | {"foot":4} | {"car_oneway":10} | {"bike_oneway":11}')
            print(f'{car:3} | {bike_road:9} | {bike_gravel:11} | {foot:4} | {car_oneway:10} | {bike_oneway:11}')
        #
        db.execute('INSERT INTO graph_properties VALUES(?,?,?,?,?,?,?,?)',
                   (way_id,car_oneway,bike_oneway,car,bike_road,bike_gravel,foot,properties))


def main():
    """entry point"""
    if len(sys.argv) != 2:
        print('Erstellt eine Tabelle mit Eigenschaften der Kante für das Routing\n\n'
              'Usage:\n'
              f'{sys.argv[0]} DATABASE')
        sys.exit(1)
    # connect to the database
    db_connect = sqlite3.connect(sys.argv[1])
    db = db_connect.cursor()   # new database cursor
    #
    graph_properties(db)
    # write data to database
    db_connect.commit()
    db_connect.close()


if __name__ == "__main__":
    main()
