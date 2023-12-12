#!/usr/bin/env python
import sys
import sqlite3

if len(sys.argv) != 3:
    print(f'''
    Check if street names in addr:street have the same name in a neighbouring way.
    Usage:
    {sys.argv[0]} DATABASE POSTCODE
    ''')
    sys.exit(1)
database = sys.argv[1]
postcode = sys.argv[2]

db_connect = sqlite3.connect(database)
db = db_connect.cursor()   # new database cursor

print('<html>')
print('''
<p>
Street names in addr:street that do not have the same name in a neighbouring way.
</p>
''')
#
query = """
SELECT street_id,postcode,city,street,min_lon,min_lat,max_lon,max_lat
FROM addr_street
WHERE street!='' AND postcode LIKE ?
ORDER BY postcode,city,street
"""
db.execute(query, (postcode,))
for (street_id, postcode, city, street, min_lon, min_lat, max_lon, max_lat) in db.fetchall():
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
    FROM rtree_way
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
            if street == value:
                check_successful = True
    #
    if not check_successful:
        print('<hr>')
        print(f'<h2>{postcode} {city}, {street} (street_id: {street_id})</h2>')
        # Show all relevant nodes and ways
        query2 = 'SELECT node_id,way_id FROM addr_housenumber WHERE street_id=?'
        db.execute(query2, (street_id,))
        for (node_id, way_id,) in db.fetchall():
            if node_id != -1:
                print(f'<span>node </span><a href="https://www.openstreetmap.org/node/{node_id}" target="_blank">{node_id}</a><br>')
            if way_id != -1:
                print(f'<span>way </span><a href="https://www.openstreetmap.org/way/{way_id}" target="_blank">{way_id}</a><br>')
print('</html>')
