#!/usr/bin/env python
"""
Displays data from the osm2sqlite database
"""
import sys
import sqlite3


def show_node(cur, node_id):
    """
    Displays OSM data of a node
    """
    # Location
    cur.execute('SELECT lon,lat FROM nodes WHERE node_id=?', (node_id,))
    for (lon, lat) in cur.fetchall():
        print(f'node {node_id} location {lon} {lat}')
    # Tags
    cur.execute('SELECT key,value FROM node_tags WHERE node_id=?', (node_id,))
    for (key, value) in cur.fetchall():
        print(f'node {node_id} tag "{key}":"{value}"')
    # Part of relation
    cur.execute("""
    SELECT relation_id,role
    FROM relation_members
    WHERE ref_id=? AND ref='node'""", (node_id,))
    for (relation_id, role) in cur.fetchall():
        print(f'node {node_id} part_of_relation {relation_id} {role}')


def show_way(cur, way_id):
    """
    Displays OSM data of a way
    """
    # Tags
    cur.execute('SELECT key,value FROM way_tags WHERE way_id=?', (way_id,))
    for (key, value) in cur.fetchall():
        print(f'way {way_id} tag "{key}":"{value}"')
    # Part of relation
    cur.execute("""
    SELECT relation_id,role
    FROM relation_members
    WHERE ref_id=? AND ref='way'""", (way_id,))
    for (relation_id, role) in cur.fetchall():
        print(f'way {way_id} part_of_relation {relation_id:15d} {role}')
    # Nodes
    cur.execute('''
    SELECT wn.node_id,n.lat,n.lon
    FROM way_nodes AS wn
    LEFT JOIN nodes AS n ON wn.node_id=n.node_id
    WHERE wn.way_id=?
    ORDER BY wn.node_order''', (way_id,))
    for (node_id, lat, lon) in cur.fetchall():
        print(f'way {way_id} node {node_id:15d} {lat:12.7f} {lon:12.7f}')


def show_relation(cur, relation_id):
    """
    Displays OSM data of a relation
    """
    # Tags
    cur.execute('SELECT key,value FROM relation_tags WHERE relation_id=?',
                (relation_id,))
    for (key, value) in cur.fetchall():
        print(f'relation {relation_id} tag "{key}":"{value}"')
    # Part of relation
    cur.execute("""
    SELECT relation_id,role
    FROM relation_members
    WHERE ref_id=? AND ref='relation'""", (relation_id,))
    for (part_relation_id, role) in cur.fetchall():
        print(f'relation {relation_id} part_of_relation '
              f'{part_relation_id} {role}')
    # Members
    cur.execute('''
    SELECT ref,ref_id,role
    FROM relation_members
    WHERE relation_id=?
    ORDER BY member_order''', (relation_id,))
    for (ref, ref_id, role) in cur.fetchall():
        print(f'relation {relation_id} member {ref} {ref_id} {role}')


def main():
    "Check parameter"
    if len(sys.argv) != 4:
        print('Show OSM data on stdout.\n\n'
              'Usage:\n'
              f' {sys.argv[0]} DATABASE [node|way|relation] ID')
        sys.exit(1)
    con = sqlite3.connect(sys.argv[1])  # database connection
    cur = con.cursor()                  # new database cursor
    osm_id = int(sys.argv[3])
    if sys.argv[2] == 'node':
        show_node(cur, osm_id)
    elif sys.argv[2] == 'way':
        show_way(cur, osm_id)
    elif sys.argv[2] == 'relation':
        show_relation(cur, osm_id)
    else:
        print('parameter error')


if __name__ == '__main__':
    main()
