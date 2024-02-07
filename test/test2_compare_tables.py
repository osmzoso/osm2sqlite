#!/usr/bin/env python
"""
Test2: Compare tables
"""
import sys
import sqlite3

if len(sys.argv) != 1:
    print(f'''
    Compare tables.
    Usage:
    {sys.argv[0]}
    ''')
    sys.exit(1)


def compare_table(table, columns):
    """Compares the specified columns of a table"""
    print(f'compare table "{table}" ', end='', flush=True)
    diff_c2py = db.execute(f'''
    SELECT count(*) FROM
    (
      SELECT {columns} FROM db_c.{table}
      EXCEPT
      SELECT {columns} FROM db_py.{table}
    )
    ''').fetchone()[0]
    diff_py2c = db.execute(f'''
    SELECT count(*) FROM
    (
      SELECT {columns} FROM db_py.{table}
      EXCEPT
      SELECT {columns} FROM db_c.{table}
    )
    ''').fetchone()[0]
    if diff_c2py == 0 and diff_py2c == 0:
        print('\033[32m' + 'OK' + '\033[0m')
    else:
        print('\033[31m' + 'ERROR' + '\033[0m' +
              f' -> diff: c2py {diff_c2py}, py2c {diff_py2c}')


print("----------------------------------------------")
print("Test2: Compare tables")
print("----------------------------------------------")
# database connection
db_connect = sqlite3.connect(":memory:")
db = db_connect.cursor()   # new database cursor
db.execute("ATTACH DATABASE './osm_c.db'  AS db_c")
db.execute("ATTACH DATABASE './osm_py.db' AS db_py")

# for floating point columns CAST needed, see "show_diff_floating_point.sql"
compare_table('nodes', 'node_id,CAST(lon AS TEXT),CAST(lat AS TEXT)')
compare_table('node_tags', 'node_id,key,value')
compare_table('way_nodes', 'way_id,node_id,node_order')
compare_table('way_tags', 'way_id,key,value')
compare_table('relation_members', 'relation_id,ref,ref_id,role,member_order')
compare_table('relation_tags', 'relation_id,key,value')
compare_table('addr_street', 'street_id,postcode,city,street,'
              'CAST(min_lon AS TEXT),CAST(min_lat AS TEXT),'
              'CAST(max_lon AS TEXT),CAST(max_lat AS TEXT)')
compare_table('addr_housenumber', 'housenumber_id,street_id,housenumber,'
              'CAST(lon AS TEXT),CAST(lat AS TEXT),way_id,node_id')
compare_table('graph', 'edge_id,start_node_id,end_node_id,dist,way_id')
