#!/usr/bin/env python
"""
Map addresses
"""
import sys
import sqlite3
import html_leaflet


def map_addr_html(cur, min_lon, min_lat, max_lon, max_lat, html_filename):
    """Creates HTML file with map of addresses"""
    m = html_leaflet.Leaflet(html_filename)
    m.write_html_header('Map OSM addresses')
    m.write_html_code(f'''
<h2>Map of the OpenStreetMap addresses ({min_lon} {min_lat}) ({max_lon} {max_lat})</h2>
<p>
<div id="mapid" style="width: 100%; height: 700px;"></div>
</p>
''')
    m.write_script_start()
    query = '''
    SELECT way_id,node_id,postcode,city,street,housenumber,lon,lat
    FROM addr_view
    WHERE lon>=? AND lat>=? AND lon<=? AND lat<=?
    ORDER BY postcode,street,abs(housenumber)
    '''
    # 1. Map Marker
    cur.execute(query, (min_lon, min_lat, max_lon, max_lat))
    for (way_id, node_id, postcode, city, street, housenumber, lon, lat) in cur.fetchall():
        popup_text = '<pre>'
        popup_text += f'addr:postcode    : {postcode}<br>'
        popup_text += f'addr:city        : {city}<br>'
        popup_text += f'addr:street      : {street}<br>'
        popup_text += f'addr:housenumber : {housenumber}<br>'
        popup_text += '</pre>'
        m.add_marker(lon, lat, popup_text, False)
    m.set_property(
      {'color': '#000068', 'opacity': 1.0, 'weight': 2, 'dasharray': '5 5',
       'fillcolor': 'none', 'fillopacity': 1.0}
    )
    m.add_rectangle(m.bbox['min_lon'], m.bbox['min_lat'], m.bbox['max_lon'], m.bbox['max_lat'], '')
    m.write_script_end()
    # 2. Table of addresses
    m.write_html_code('<table>\n')
    m.write_html_code('<tr><th>way_id</th><th>node_id</th><th>addr:postcode</th><th>addr:city</th><th>addr:street</th><th>addr:housenumber</th><th>lon</th><th>lat</th></tr>\n')
    cur.execute(query, (min_lon, min_lat, max_lon, max_lat))
    for (way_id, node_id, postcode, city, street, housenumber, lon, lat) in cur.fetchall():
        m.write_html_code('<tr>')
        if way_id != -1:
            m.write_html_code(f'<td><a href="https://www.openstreetmap.org/way/{way_id}" target="_blank">{way_id}</a></td>')
        else:
            m.write_html_code(f'<td>{way_id}</td>')
        if node_id != -1:
            m.write_html_code(f'<td><a href="https://www.openstreetmap.org/node/{node_id}" target="_blank">{node_id}</a></td>')
        else:
            m.write_html_code(f'<td>{node_id}</td>')
        m.write_html_code(f'<td>{postcode}</td><td>{city}</td>')
        m.write_html_code(f'<td>{street}</td><td>{housenumber}</td><td>{lon}</td><td>{lat}</td></tr>\n')
    m.write_html_code('</table>\n')
    m.write_html_footer()


def main():
    """entry point"""
    if len(sys.argv) != 7:
        print('Creates an HTML file with a map of all addresses in a specific area.\n'
              'The addresses must exist in the "addr_view" table.\n\n'
              'Usage:\n'
              f'{sys.argv[0]} DATABASE MIN_LON MIN_LAT MAX_LON MAX_LAT HTML_FILE')
        sys.exit(1)
    min_lon = float(sys.argv[2])
    min_lat = float(sys.argv[3])
    max_lon = float(sys.argv[4])
    max_lat = float(sys.argv[5])
    html_filename = sys.argv[6]
    # connect to the database
    con = sqlite3.connect(sys.argv[1])
    cur = con.cursor()   # new database cursor
    #
    map_addr_html(cur, min_lon, min_lat, max_lon, max_lat, html_filename)
    # write data to database
    con.commit()
    con.close()


if __name__ == '__main__':
    main()
