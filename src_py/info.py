#!/usr/bin/env python
"""
Displays data from the osm2sqlite database
"""
import sys
import sqlite3


def show_node(node_id):
    "Displays all data of a node"
    db.execute('SELECT lon,lat FROM nodes WHERE node_id=?', (node_id,))
    for (lon, lat) in db.fetchall():
        print(f'node {node_id} location {lon} {lat}')
    db.execute('SELECT key,value FROM node_tags WHERE node_id=?', (node_id,))
    for (key, value) in db.fetchall():
        print(f'node {node_id} tags {key:30} {value}')
    db.execute("SELECT relation_id FROM relation_members WHERE ref_id=? AND ref='node'", (node_id,))
    for (relation_id,) in db.fetchall():
        print(f'node {node_id} part_of_relation {relation_id}')


def show_way(way_id):
    "Displays all data of a way"
    db.execute('SELECT key,value FROM way_tags WHERE way_id=?', (way_id,))
    for (key, value) in db.fetchall():
        print(f'way {way_id} tags {key:30} {value}')
    db.execute('''SELECT wn.node_id,wn.node_order,n.lat,n.lon
                  FROM way_nodes AS wn
                  LEFT JOIN nodes AS n ON wn.node_id=n.node_id
                  WHERE wn.way_id=?
                  ORDER BY wn.node_order''', (way_id,))
    for (node_id, node_order, lat, lon) in db.fetchall():
        print(f"way {way_id} nodes {node_order:4d} {node_id:15d}"
              f"{lat:12.7f} {lon:12.7f}")
    db.execute("SELECT relation_id FROM relation_members WHERE ref_id=? AND ref='way'", (way_id,))
    for (relation_id,) in db.fetchall():
        print(f'way {way_id} part_of_relation {relation_id}')


def show_relation(relation_id):
    "Displays all data of a relation"
    db.execute('SELECT key,value FROM relation_tags WHERE relation_id=?', (relation_id,))
    for (key, value) in db.fetchall():
        print(f'relation {relation_id} tags {key:30} {value}')
    db.execute('''SELECT ref,ref_id,role FROM relation_members
                  WHERE relation_id=? ORDER BY member_order''', (relation_id,))
    for (ref, ref_id, role) in db.fetchall():
        print(f'relation {relation_id} member {ref} {ref_id} {role}')
    db.execute("""SELECT relation_id FROM relation_members
                  WHERE ref_id=? AND ref='relation'""", (relation_id,))
    for (part_relation_id,) in db.fetchall():
        print(f'relation {relation_id} part_of_relation {part_relation_id}')


def main():
    "Check parameter"
    global db
    if len(sys.argv) != 4:
        print('Show OSM data on stdout.\n'
              'Usage:\n'
              f' {sys.argv[0]} DATABASE [node|way|relation] OSM_ID')
        sys.exit(1)
    db_connect = sqlite3.connect(sys.argv[1])  # database connection
    db = db_connect.cursor()                   # new database cursor
    osm_id = int(sys.argv[3])
    if sys.argv[2] == 'node':
        show_node(osm_id)
    elif sys.argv[2] == 'way':
        show_way(osm_id)
    elif sys.argv[2] == 'relation':
        show_relation(osm_id)
    else:
        print('parameter error')


if __name__ == "__main__":
    main()
