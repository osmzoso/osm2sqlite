#!/usr/bin/env python
import sys, sqlite3

if len(sys.argv)!=3:
    print('''
    Checks whether the street name of the address in this range also exists as a highway.
    Usage:
    check_addr_highway.py DATABASE POSTCODE
    ''')
    sys.exit(1)

db_connect = sqlite3.connect(sys.argv[1])
db = db_connect.cursor()   # new database cursor

print('street_id', 'postcode', 'city', 'street', sep='\t')

#
query = """
SELECT street_id,postcode,city,street,min_lon,min_lat,max_lon,max_lat
FROM addr_street
WHERE postcode LIKE '"""+sys.argv[2]+"""%'
ORDER BY postcode,city,street
"""
db.execute(query)
for (street_id,postcode,city,street,min_lon,min_lat,max_lon,max_lat) in db.fetchall():
    check_successful = False
    # Expand the search area a bit
    expand = 0.002
    min_lon = min_lon - expand
    max_lon = max_lon + expand
    min_lat = min_lat - expand
    max_lat = max_lat + expand
    # Searach all highway in the search area
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
        print(street_id, postcode, city, street, sep='\t')
