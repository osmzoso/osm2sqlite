#!/usr/bin/env python
"""
Generate a map to show the table 'graph'
"""
import sys
import sqlite3
import html_leaflet


def way_edge_points(cur, way_id, start_node_id, end_node_id):
    """Returns a list with all points (lon,lat) of the edge"""
    point_list = []
    cur.execute('''
    SELECT wn.way_id,wn.node_id,wn.node_order,n.lon,n.lat
    FROM way_nodes AS wn
    LEFT JOIN nodes AS n ON wn.node_id=n.node_id
    WHERE wn.way_id=?
    ORDER BY wn.node_order
    ''', (way_id,))
    add_point = False
    for (way_id, node_id, node_order, lon, lat) in cur.fetchall():
        if not add_point and node_id==start_node_id:
            add_point = True
        if add_point:
            point_list.append((lon, lat))
        if add_point and node_id==end_node_id:
            add_point = False
    if add_point:       # something wrong with start_node_id or end_node_id
        point_list = []
    return point_list


def node_point(cur, node_id):
    """Returns lon,lat for a given Node ID"""
    res = cur.execute('SELECT lon,lat FROM nodes WHERE node_id=?', (node_id,))
    return res.fetchone()


def html_map_table_graph(cur, min_lon, min_lat, max_lon, max_lat, html_filename):
    """TODO Beschreibung der Funktion..."""
    m = html_leaflet.Leaflet(html_filename)
    m.write_html_header('Map Routing Graph')
    m.write_html_code(f'''
    <h2>Map Routing Graph ({min_lon} {min_lat}) ({max_lon} {max_lat})</h2>
    <p>
    <div id="mapid" style="width: 100%; height: 700px;"></div>
    </p>
    ''')
    m.write_script_start()
    cur.execute('''
    SELECT way_id,start_node_id,end_node_id
    FROM graph
    WHERE way_id IN (
     SELECT way_id
     FROM rtree_way
     WHERE max_lon>=? AND min_lon<=?
       AND max_lat>=? AND min_lat<=?
    )
    ''', (min_lon, max_lon, min_lat, max_lat))
    for (way_id, start_node_id, end_node_id) in cur.fetchall():
        # 1. Simple line for the edge
        lon1, lat1 = node_point(cur, start_node_id)
        lon2, lat2 = node_point(cur, end_node_id)
        m.set_property({'color': '#0000ff'})
        m.add_line(lon1, lat1, lon2, lat2)
        # 2. Exact course of the edge
        point_list = way_edge_points(cur, way_id, start_node_id, end_node_id)
        m.set_property({'color': '#ff0000'})
        m.add_polyline(point_list)
    m.set_property(
      {'color': '#ff0000', 'opacity': 1.0, 'weight': 2, 'dasharray': '5 5',
       'fillcolor': 'none', 'fillopacity': 1.0}
    )
    m.add_rectangle(min_lon, min_lat, max_lon, max_lat, '')
    m.write_script_end()
    m.write_html_footer()


def main():
    """entry point"""
    if len(sys.argv) != 7:
        print('Creates a map with data from table "graph"\n\n'
              'Usage:\n'
              f'{sys.argv[0]} DATABASE MIN_LON MIN_LAT MAX_LON MAX_LAT HTML_FILE')
        sys.exit(1)
    #
    min_lon = float(sys.argv[2])
    min_lat = float(sys.argv[3])
    max_lon = float(sys.argv[4])
    max_lat = float(sys.argv[5])
    html_filename = sys.argv[6]
    # connect to the database
    con = sqlite3.connect(sys.argv[1])
    cur = con.cursor()   # new database cursor
    #
    html_map_table_graph(cur, min_lon, min_lat, max_lon, max_lat, html_filename)
    # write data to database
    con.commit()
    con.close()


if __name__ == '__main__':
    main()