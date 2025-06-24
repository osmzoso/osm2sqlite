#!/usr/bin/env python
"""
Test3: Check table graph
"""
import sys
import sqlite3

if len(sys.argv) != 2:
    print(f'''
    Simple check for table 'graph'.
    Usage:
    {sys.argv[0]} DATABASE
    ''')
    sys.exit(1)


def check_table_graph():
    """
    Compares the start and end of a way with
    the start and end of the edge sequence (rough test only)
    """
    errors = 0
    db.execute("SELECT DISTINCT way_id FROM way_tags WHERE key='highway'")
    for (way_id,) in db.fetchall():
        # get first and last node from way
        way_first_node = -1
        way_last_node = -1
        db.execute('''SELECT node_id
                      FROM way_nodes
                      WHERE way_id=?
                      ORDER BY node_order''', (way_id,))
        for (node_id, ) in db.fetchall():
            if way_first_node == -1:
                way_first_node = node_id
            way_last_node = node_id
        # get first and last node from edge sequence
        edge_first_node = -1
        edge_last_node = -1
        db.execute('''SELECT start_node_id,end_node_id
                      FROM graph
                      WHERE way_id=?
                      ORDER BY edge_id''', (way_id,))
        for (start_node_id, end_node_id) in db.fetchall():
            if edge_first_node == -1:
                edge_first_node = start_node_id
            edge_last_node = end_node_id
        #
        if way_first_node != edge_first_node or \
                way_last_node != edge_last_node:
            errors = errors + 1
            print('Error way_id', way_id)
    return errors


print("-----------------------------------------------")
print('Test 3: Check table "graph"')
print("-----------------------------------------------")
# database connection
print('check table "graph" ', end='', flush=True)
db_connect = sqlite3.connect(sys.argv[1])
db = db_connect.cursor()   # new database cursor
errors = check_table_graph()
if errors == 0:
    print('\033[32m' + 'OK' + '\033[0m')
else:
    print('\033[31m' + 'ERROR' + '\033[0m' + f' -> errors {errors}')
