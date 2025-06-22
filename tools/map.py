#!/usr/bin/env python
"""
Draw simple map

https://www.w3schools.com/graphics/svg_intro.asp
https://de.wikipedia.org/wiki/Scalable_Vector_Graphics
"""
import sys
import sqlite3
import math


def spherical_to_mercator(lon, lat):
    "Converts spherical coordinates into planar coordinates"
    r = 6378137.0
    x = r * math.radians(lon)
    y = r * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y


def mercator_to_spherical(x, y):
    "Converts planar coordinates into spherical coordinates"
    r = 6378137.0
    lon = math.degrees(x / r)
    lat = math.degrees(2 * math.atan(math.exp(y / r)) - math.pi / 2.0)
    return lon, lat


def size_world_map(zoomlevel):
    """
    Calculates the size of a square world map in pixels for a given zoom level
    """
    tile_size = 256     # tile 256px x 256px
    number_tiles = 4**zoomlevel
    pixel_world_map = int(tile_size * math.sqrt(number_tiles))
    return pixel_world_map


def meter_per_pixel(pixel_world_map):
    """
    Calculates the size of a pixel in meters for a given size of
    a square world map in pixels at the equator
    """
    webmercator = 20037508.342789244
    meters_pixel = webmercator * 2 / pixel_world_map
    return meters_pixel


def webmercator_to_pixel(x, y, pixel_world_map):
    """
    Transform Web Mercator to pixel coordinates
    Returns x_px, y_px
    """
    pixel_world_map -= 1
    webmercator = 20037508.342789244
    x += webmercator  # move origin to avoid negativ coordinates
    y += webmercator
    x_px = int(round((x * pixel_world_map) / (webmercator * 2), 0))
    y_px = int(round((y * pixel_world_map) / (webmercator * 2), 0))
    return x_px, y_px


def pixel_to_webmercator(x_px, y_px, pixel_world_map):
    """
    Transform pixel coordinates to Web Mercator
    Returns x, y
    """
    webmercator = 20037508.342789244
    x_px -= pixel_world_map / 2
    y_px -= pixel_world_map / 2
    x = (x_px / pixel_world_map) * (webmercator * 2)
    y = (y_px / pixel_world_map) * (webmercator * 2)
    return x, y


def spherical_to_pixel(lon, lat, pixel_world_map):
    """
    Transform spherical coordinates to pixel coordinates
    Returns x_px, y_px
    """
    x, y = spherical_to_mercator(lon, lat)
    x_px, y_px = webmercator_to_pixel(x, y, pixel_world_map)
    return x_px, y_px


def pixel_to_spherical(x_px, y_px, pixel_world_map):
    """
    Transform pixel coordinates to spherical coordinates
    Returns lon, lat
    """
    x, y = pixel_to_webmercator(x_px, y_px, pixel_world_map)
    lon, lat = mercator_to_spherical(x, y)
    return lon, lat


def pixel_boundingbox(lon, lat, pixel_world_map, size_x_px, size_y_px):
    """
    Calculate pixel boundingbox
    size_x_px, size_y_px: map size in pixel
    Return min_x_px, min_y_px, max_x_px, max_y_px
    """
    x_px, y_px = spherical_to_pixel(lon, lat, pixel_world_map)
    min_x_px = x_px - int(size_x_px / 2)
    min_y_px = y_px - int(size_y_px / 2)
    max_x_px = x_px + int(size_x_px / 2)
    max_y_px = y_px + int(size_y_px / 2)
    return min_x_px, min_y_px, max_x_px, max_y_px


def multipolygon_outer_ways(cur, relation_id, swap_nodes):
    """
    Determines all outer ways of a multipolygon.
    The direction of the first way must be specified as the 'swap_nodes' parameter.
    The result is written to the temporary table 'multipolygon_outer_ways'.
    It then checks whether the ways form a closed circle.
    The return value of this function is the result of this check.
    """
    cur.execute('DROP TABLE IF EXISTS multipolygon_outer_ways')
    cur.execute('''
    CREATE TEMP TABLE multipolygon_outer_ways (
     member_order  INTEGER,
     way_id        INTEGER,
     first_node    INTEGER,
     last_node     INTEGER,
     way_reversed  INTEGER
    );
    ''')
    start_node = -1
    prev_node = -1
    cur.execute('''
    SELECT DISTINCT member_order,way_id,
     first_value(node_id) OVER (PARTITION BY way_id) AS first_node,
     last_value(node_id) OVER (PARTITION BY way_id) AS last_node
    FROM (
      SELECT rm.member_order,wn.way_id,wn.node_id
      FROM relation_members AS rm
      LEFT JOIN way_nodes AS wn ON rm.ref_id=wn.way_id
      WHERE rm.relation_id=? AND ref='way' AND rm.role='outer'
      ORDER BY wn.node_order
    )
    ORDER BY member_order
    ''', (relation_id,))
    for (member_order, way_id, first_node, last_node) in cur.fetchall():
        if prev_node == -1:
            if not swap_nodes:
                start_node = first_node
                prev_node = last_node
            else:
                start_node = last_node
                prev_node = first_node
        else:
            if first_node == prev_node:
                swap_nodes = False
                prev_node = last_node
            else:
                swap_nodes = True
                prev_node = first_node
        #
        cur.execute('INSERT INTO multipolygon_outer_ways VALUES (?,?,?,?,?)',
                    (member_order, way_id, first_node, last_node, swap_nodes))
    # check if polygon is closed
    polygon_closed = False
    if start_node == prev_node:
        polygon_closed = True
    #
    return polygon_closed


def multipolygon_outer_nodes(cur, relation_id):
    """
    Creates a temporary table 'multipolygon_outer_nodes'.
    The table contains all nodes of the outer ways.
    Return value is the number of nodes.
    If the number is zero then the outer ring is not closed.
    """
    cur.execute('DROP TABLE IF EXISTS multipolygon_outer_nodes')
    cur.execute('CREATE TEMP TABLE multipolygon_outer_nodes (node_id INTEGER)')
    if not multipolygon_outer_ways(cur, relation_id, False):
        if not multipolygon_outer_ways(cur, relation_id, True):
            return 0
    prev_node_id = -1
    number_nodes = 0
    cur.execute('''
    SELECT way_id,way_reversed
    FROM multipolygon_outer_ways
    ORDER BY member_order
    ''')
    for (way_id, way_reversed) in cur.fetchall():
        query = '''
        SELECT node_id
        FROM way_nodes
        WHERE way_id=?
        ORDER BY node_order
        '''
        if way_reversed:
            query += ' DESC'
        cur.execute(query, (way_id,))
        for (node_id,) in cur.fetchall():
            if node_id != prev_node_id and prev_node_id != -1:
                cur.execute('INSERT INTO multipolygon_outer_nodes VALUES (?)',
                            (node_id,))
                number_nodes += 1
            prev_node_id = node_id
    return number_nodes


#
#
#
def dms_to_dec(dms: str) -> float:
    """
    Converts a string with degrees minutes seconds (e.g.'85°3'4.0636"')
    into a decimal value
    """
    dms = dms.replace('°', ' ').replace('\'', ' ').replace('"', ' ')
    s = dms.split()
    dec = (((float(s[2]) / 60) + int(s[1])) / 60) + int(s[0])
    return dec


def dec_to_dms(dec:float) -> str:
    """
    Converts a decimal value into a string with degrees minutes seconds
    """
    degrees = int(dec)
    x = (dec - degrees) * 60
    minutes = int(x)
    seconds = (x - minutes) * 60
    return f'{degrees}°{minutes}\'{seconds}"'


def show_zoomlevel():
    """
    Show zoomlevel size
    """
    print('zoomlevel       pixel_world_map          meters_pixel')
    for zoomlevel in range(21):
        pixel_world_map = size_world_map(zoomlevel)
        meters_pixel = meter_per_pixel(pixel_world_map)
        print(f'{zoomlevel:5}     '
              f'{pixel_world_map:>12} x {pixel_world_map:<12} '
              f'{meters_pixel:>14.2f}')
    #
    print('\nTest Mercator projection:')
    lon = 180
    lat = 85.05112878
    x, y = spherical_to_mercator(lon, lat)
    print(f'lon {lon:12.8f} -> x {x}')
    print(f'lat {lat:12.8f} -> y {y}')
    lat_dms = dec_to_dms(lat)
    print(f'lat_dms: {lat_dms} -> check:', dms_to_dec(lat_dms))


def draw_map(cur, lon, lat, zoomlevel, width, height, outfile, show_unknown=True):
    """
    Draw a map in SVG format.
    A table 'map_def' is required in the database.
    """
    # calculate pixel and sperical boundingboxes
    pixel_world_map = size_world_map(zoomlevel)
    x1, y1, x2, y2 = pixel_boundingbox(lon, lat, pixel_world_map, width, height)
    lon1, lat1 = pixel_to_spherical(x1, y1, pixel_world_map)
    lon2, lat2 = pixel_to_spherical(x2, y2, pixel_world_map)
    #
    f = open(outfile, 'w', encoding='utf-8')
    f.write(f'<svg height="{height}" width="{width}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')
    f.write('''
    <style type="text/css">
    <![CDATA[
      text {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 10;
        text-anchor: center;
        /* text-anchor: middle; */
        dominant-baseline: central;
        /* alignment-baseline: middle; */
      }
    ]]>
    </style>
    \n''')
    f.write('<!--\n'
            '************ map info ************\n'
           f'lon lat              : {lon} {lat}\n'
           f'zoomlevel            : {zoomlevel}\n'
           f'width height         : {width} {height}\n'
           f'boundingbox pixel    : {x1} {y1} - {x2} {y2}\n'
           f'boundingbox sperical : {lon1} {lat1} - {lon2} {lat2}\n'
            '-->\n')
    #
    f.write('<rect width="100%" height="100%" fill="#f2efe9" />\n')
    # 1. Determine all ways, nodes and relations in the area
    cur.execute('''
    CREATE TEMP TABLE bbox_ways AS
    SELECT way_id
    FROM rtree_way
    WHERE max_lon>=? AND min_lon<=?
      AND max_lat>=? AND min_lat<=?
    ''', (lon1, lon2, lat1, lat2))
    cur.execute('''
    CREATE TEMP TABLE bbox_nodes AS
    SELECT node_id
    FROM rtree_node
    WHERE max_lon>=? AND min_lon<=?
      AND max_lat>=? AND min_lat<=?
    ''', (lon1, lon2, lat1, lat2))
    cur.execute('''
    CREATE TEMP TABLE bbox_relations AS
    SELECT rm.relation_id
    FROM relation_members AS rm
    JOIN relation_tags AS rt ON rm.relation_id=rt.relation_id
        -- only relations with type=multipolygon
        AND rt.key='type' AND rt.value='multipolygon'
    WHERE (rm.ref='way' AND rm.ref_id IN (SELECT way_id FROM bbox_ways)) OR
          (rm.ref='node' AND rm.ref_id IN (SELECT node_id FROM bbox_nodes))
    GROUP BY rm.relation_id
    ''')
    # 2. Create table 'map_drawplan'
    cur.execute('''
    CREATE TEMP TABLE map_drawplan AS
      SELECT md.opcode,'way' AS ref,w.way_id AS ref_id,
        md.layer,md.width,md.fill,md.stroke,md.dash
      FROM bbox_ways AS w
      LEFT JOIN way_tags AS wt ON w.way_id=wt.way_id
      LEFT JOIN map_def AS md ON wt.key=md.key AND wt.value LIKE md.value
        AND md.zoomlevel=? AND md.way_node='way'
      WHERE md.opcode IS NOT NULL
    UNION ALL
      SELECT md.opcode,'node' AS ref,n.node_id AS ref_id,
        md.layer,md.width,md.fill,md.stroke,md.dash
      FROM bbox_nodes AS n
      LEFT JOIN node_tags AS nt ON n.node_id=nt.node_id
      LEFT JOIN map_def AS md ON nt.key=md.key AND nt.value LIKE md.value
        AND md.zoomlevel=? AND md.way_node='node'
      WHERE md.opcode IS NOT NULL
    UNION ALL
      SELECT md.opcode||'_mp','relation' AS ref,r.relation_id AS ref_id,
        md.layer,md.width,md.fill,md.stroke,md.dash
      FROM bbox_relations AS r
      LEFT JOIN relation_tags AS rt ON r.relation_id=rt.relation_id
      LEFT JOIN map_def AS md ON rt.key=md.key AND rt.value LIKE md.value
        AND md.zoomlevel=? AND md.way_node='way'
      WHERE md.opcode IS NOT NULL
    ''', (zoomlevel, zoomlevel, zoomlevel))
    # 3. Execute drawplan
    cur.execute('''
    SELECT opcode,ref,ref_id,layer,width,fill,stroke,dash
    FROM map_drawplan
    ORDER BY layer
    ''')
    for (opcode,ref,ref_id,layer,width,fill,stroke,dash) in cur.fetchall():
        f.write(f'<!-- {opcode} {ref} {ref_id} {layer} {width} {fill} {stroke} {dash} -->\n')
        if (opcode == 'line' or opcode == 'area') and ref == 'way':
            f.write(f'<path id="{ref}_{ref_id}" d="')
            command = 'M'
            cur.execute('''
            SELECT n.lon,n.lat
            FROM way_nodes AS wn
            LEFT JOIN nodes AS n ON wn.node_id=n.node_id
            WHERE wn.way_id=?
            ORDER BY wn.node_order
            ''', (ref_id,))
            for (lon, lat) in cur.fetchall():
                x, y = spherical_to_pixel(lon, lat, pixel_world_map)
                x -= x1
                y -= y1
                y = height - y
                f.write(f'{command}{x} {y} ')
                if command == 'M':
                    command = 'L'
            if opcode == 'line':
                f.write(f'" style="fill:none;stroke:{stroke};stroke-width:{width};stroke-linecap:round;stroke-dasharray:{dash}" />\n')
            elif opcode == 'area':
                f.write(f'Z" style="fill:{fill};stroke:{stroke};stroke-width:{width}" />\n')
        if opcode == 'area_mp' and ref == 'relation':
            # outer
            if multipolygon_outer_nodes(cur, ref_id) > 0:
                f.write(f'<path id="{ref}_{ref_id}" d="')
                command = 'M'
                cur.execute('''
                SELECT n.lon,n.lat
                FROM multipolygon_outer_nodes AS mn
                LEFT JOIN nodes AS n ON mn.node_id=n.node_id
                ORDER BY mn.rowid
                ''')
                for (lon, lat) in cur.fetchall():
                    x, y = spherical_to_pixel(lon, lat, pixel_world_map)
                    x -= x1
                    y -= y1
                    y = height - y
                    f.write(f'{command}{x} {y} ')
                    if command == 'M':
                        command = 'L'
                f.write(f'Z" style="fill:{fill};stroke:{stroke};stroke-width:{width}" />\n')
                # inner
                # TODO
                #f.write(f'    <!-- TEST \n')  # TEST
                #f.write(f'    -->\n')  # TEST
        if opcode == 'point' and ref == 'node':
            cur.execute('SELECT lon,lat FROM nodes WHERE node_id=?', (ref_id,))
            lon, lat = cur.fetchone()
            x, y = spherical_to_pixel(lon, lat, pixel_world_map)
            x -= x1
            y -= y1
            y = height - y
            f.write(f'<circle cx="{x}" cy="{y}" r="{width}" fill="{fill}" />\n')
    #
    f.write('</svg>')
    f.close()


def main():
    """entry point"""
    if len(sys.argv) == 1:
        print('Creates a simple map. Output is in SVG format.\n'
              'Usage:\n'
              f'{sys.argv[0]} DATABASE LON LAT ZOOMLEVEL WIDTH HEIGHT OUTFILE [debug]\n'
              f'{sys.argv[0]} zoomlevel\n')
        sys.exit(1)
    if len(sys.argv) >= 8:
        con = sqlite3.connect(sys.argv[1])  # database connection
        cur = con.cursor()                  # new database cursor
        lon = float(sys.argv[2])
        lat = float(sys.argv[3])
        zoomlevel = int(sys.argv[4])
        width = int(sys.argv[5])
        height = int(sys.argv[6])
        outfile = sys.argv[7]
        show_unknown = False
        if len(sys.argv) == 9 and sys.argv[8] == 'debug':
            show_unknown = True
        draw_map(cur, lon, lat, zoomlevel, width, height, outfile, show_unknown)
    if len(sys.argv) == 2 and sys.argv[1] == 'zoomlevel':
        show_zoomlevel()


if __name__ == '__main__':
    main()
