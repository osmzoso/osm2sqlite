#!/usr/bin/env python
"""
Check OSM data
"""
import sys
import sqlite3
import map


def check_outer_ring_not_closed(cur):
    """
    Test outer ring not closed
    """
    number_multipolygons = 0
    ring_not_closed = 0
    cur.execute('''
    SELECT relation_id
    FROM relation_tags
    WHERE key='type' AND value='multipolygon'
    ''')
    for (relation_id,) in cur.fetchall():
        number_multipolygons += 1
        number_nodes = map.multipolygon_outer_nodes(cur, relation_id)
        print(f'relation {relation_id:>10} : {number_nodes:>10} nodes', end='')
        if number_nodes == 0:
            ring_not_closed += 1
            print(' -> outer ring not closed', end='')
        print()
    print(f'Number of multipolygons : {number_multipolygons}\n'
          f'Outer ring not closed   : {ring_not_closed}\n')


def main():
    """entry point"""
    if len(sys.argv) != 2:
        print('Check multipolygons\n\n'
              'Usage:\n'
              f'{sys.argv[0]} DATABASE')
        sys.exit(1)
    con = sqlite3.connect(sys.argv[1])  # connect to the database
    cur = con.cursor()                  # new database cursor
    check_outer_ring_not_closed(cur)
    con.close()


if __name__ == '__main__':
    main()
