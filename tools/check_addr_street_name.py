#!/usr/bin/env python
"""
Check OSM data
"""
import sys
import sqlite3


def check_addr_street_name(cur, postcode, html_filename):
    """Check names in addr:street"""
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write('<html>\n'
         '<p>Street names in addr:street that do not have the same name'
         ' in a neighbouring way.</p>\n')
        cur.execute('''
        SELECT street_id,
         postcode||' '||city AS city,street,
         min_lon,min_lat,max_lon,max_lat
        FROM addr_street
        WHERE street!='' AND postcode LIKE ?
        ORDER BY postcode,city,street
        ''', (postcode,))
        for (street_id, city, street, min_lon, min_lat, max_lon, max_lat) in cur.fetchall():
            check_successful = False
            # Expand the search range a bit
            expand = 0.002
            min_lon = min_lon - expand
            max_lon = max_lon + expand
            min_lat = min_lat - expand
            max_lat = max_lat + expand
            # Search all highway in the search area
            cur.execute('''
            SELECT way_id
            FROM rtree_way
            WHERE max_lon>=? AND min_lon<=?
             AND  max_lat>=? AND min_lat<=?
            ''', (min_lon, max_lon, min_lat, max_lat))
            for (way_id,) in cur.fetchall():
                # Get the name of the highway
                cur.execute('''
                SELECT value
                FROM way_tags
                WHERE way_id=? AND key='name'
                ''', (way_id,))
                for (value,) in cur.fetchall():
                    # Name of highway==Name of address street?
                    if street == value:
                        check_successful = True
            #
            if not check_successful:
                f.write(f'<hr>\n<h2>{city}, {street} (street_id: {street_id})</h2>\n')
                # Show all relevant nodes and ways
                cur.execute('''
                SELECT node_id,way_id
                FROM addr_housenumber
                WHERE street_id=?
                ''', (street_id,))
                for (node_id, way_id,) in cur.fetchall():
                    if node_id != -1:
                        f.write(f'<span>node </span><a href="https://www.openstreetmap.org/node/{node_id}" target="_blank">{node_id}</a><br>')
                    if way_id != -1:
                        f.write(f'<span>way </span><a href="https://www.openstreetmap.org/way/{way_id}" target="_blank">{way_id}</a><br>')
        f.write('</html>')


def main():
    """entry point"""
    if len(sys.argv) != 4:
        print('Check if street names in addr:street have the same name in a neighbouring way.\n\n'
              'Usage:\n'
              f'{sys.argv[0]} DATABASE POSTCODE HTML_FILENAME')
        sys.exit(1)
    #
    postcode = sys.argv[2]
    html_filename = sys.argv[3]
    # connect to the database
    con = sqlite3.connect(sys.argv[1])
    cur = con.cursor()   # new database cursor
    #
    check_addr_street_name(cur, postcode, html_filename)
    # write data to database
    con.commit()
    con.close()


if __name__ == '__main__':
    main()
