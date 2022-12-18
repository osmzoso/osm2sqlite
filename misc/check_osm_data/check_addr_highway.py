#!/usr/bin/env python
import sys, sqlite3

if len(sys.argv)!=3:
    print('''
    Checks whether the street name of the address in this range also exists as a highway.
    Usage:
    check_addr_highway.py DATABASE POSTCODE
    ''')
    sys.exit(1)
database = sys.argv[1]
postcode = sys.argv[2]

db_connect = sqlite3.connect(database)
db = db_connect.cursor()   # new database cursor

#
query = """
SELECT street_id,postcode,city,street,min_lon,min_lat,max_lon,max_lat
FROM addr_street
WHERE street!='' AND postcode LIKE ?
ORDER BY postcode,city,street
"""
db.execute(query, (postcode,))
for (street_id,postcode,city,street,min_lon,min_lat,max_lon,max_lat) in db.fetchall():
    check_successful = False
    # Expand the search range a bit
    expand = 0.002
    min_lon = min_lon - expand
    max_lon = max_lon + expand
    min_lat = min_lat - expand
    max_lat = max_lat + expand
    # Search all highway in the search area
    query2 = '''
    SELECT way_id
    FROM highway
    WHERE max_lon>=? AND min_lon<=?
     AND  max_lat>=? AND min_lat<=?
    '''
    db.execute(query2, (min_lon, max_lon, min_lat, max_lat))
    for (way_id,) in db.fetchall():
        # Get the name of the highway
        query3 = '''
        SELECT value
        FROM way_tags
        WHERE way_id=? AND key='name'
        '''
        db.execute(query3, (way_id,))
        for (value,) in db.fetchall():
            # Name of highway==Name of address street?
            if street==value:
                check_successful = True
    #
    if not check_successful:
        print('------------------------------------------------------')
        print(postcode, city, street, '(street_id: '+str(street_id)+')', sep='\t')
        # Show all relevant nodes and ways
        query2 = 'SELECT node_id,way_id FROM addr_housenumber WHERE street_id=?'
        db.execute(query2, (street_id,))
        for (node_id, way_id,) in db.fetchall():
            if node_id!=-1:
                print('https://www.openstreetmap.org/node/' + str(node_id))
            if way_id!=-1:
                print('https://www.openstreetmap.org/way/' + str(way_id))

