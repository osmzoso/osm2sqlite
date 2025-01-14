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
    Calculates the size of the world map for a zoom level
    Return pixel_world_map, meters_pixel
    (resolution (meters/pixel) measured at Equator)"
    """
    tile_size = 256     # tile 256px x 256px
    number_tiles = 4**zoomlevel
    pixel_world_map = int(tile_size * math.sqrt(number_tiles))
    webmercator = 20037508.342789244
    meters_pixel = webmercator * 2 / pixel_world_map
    return pixel_world_map, meters_pixel


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


def drawmap(cur, lon, lat, zoomlevel, bbox_x, bbox_y, svgfile, show_unknown=True):
    """
    Outputs a map in SVG format to stdout.
    A table 'map_def' is required.
    """
    f = open(svgfile, 'w', encoding="utf-8")
    # map size
    pixel_world_map, meters_pixel = size_world_map(zoomlevel)
    # pixel boundingbox
    bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = pixel_boundingbox(lon, lat, pixel_world_map, bbox_x, bbox_y)
    # spherical boundingbox
    bbox_min_lon, bbox_min_lat = pixel_to_spherical(bbox_min_x, bbox_min_y, pixel_world_map)
    bbox_max_lon, bbox_max_lat = pixel_to_spherical(bbox_max_x, bbox_max_y, pixel_world_map)
    #
    cur.execute('''CREATE TEMP TABLE map_draw_plan (
     draw_plan_id,
     ref,
     ref_id,
     key,
     value,
     layer,
     style,
     width,
     fill,
     stroke,
     dash
     )''')
    cur.execute('CREATE TEMP TABLE map_ways_unknown (way_id)')
    #
    f.write(f'<svg height="{bbox_y}" width="{bbox_x}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')
    # TODO eventuell text-anchor="middle" ?
    f.write('''
    <style type="text/css">
    <![CDATA[
      text {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 10;
        text-anchor: center;
        dominant-baseline: central;
        /* alignment-baseline: middle; */
      }
    ]]>
    </style>
    \n''')
    f.write('<!-- ************ map info ************\n')
    f.write(f'lon       : {lon}\n' +
          f'lat       : {lat}\n' +
          f'zoomlevel : {zoomlevel}\n' +
          f'size_x    : {bbox_x} (= bbox_x)\n' +
          f'size_y    : {bbox_y} (= bbox_y)\n')
    f.write(f'pixel_world_map : {pixel_world_map} x {pixel_world_map} pixel\n')
    f.write('pixel boundingbox:\n' +
          f'bbox_min_x, bbox_min_y : {bbox_min_x}, {bbox_min_y}\n' +
          f'bbox_max_x, bbox_max_y : {bbox_max_x}, {bbox_max_y}\n')
    f.write('spherical boundingbox:\n' +
          f'bbox_min_lon, bbox_min_lat : {bbox_min_lon}, {bbox_min_lat}\n' +
          f'bbox_max_lon, bbox_max_lat : {bbox_max_lon}, {bbox_max_lat}\n')
    f.write('check:\n' +
          f'bbox_max_x - bbox_min_x = bbox_x = size_x : {bbox_max_x - bbox_min_x}\n' +
          f'bbox_max_y - bbox_min_y = bbox_y = size_y : {bbox_max_y - bbox_min_y}\n')
    f.write('************ map info ************ -->\n')
    #
    f.write('<rect width="100%" height="100%" fill="#f2efe9" />\n')
    #
    draw_plan_id = 0
    cur.execute('''
    SELECT way_id
    FROM rtree_way
    WHERE max_lon>=? AND min_lon<=?
     AND  max_lat>=? AND min_lat<=?
    ''', (bbox_min_lon, bbox_max_lon, bbox_min_lat, bbox_max_lat))
    for (way_id,) in cur.fetchall():
        draw_plan_id += 1
        insert_draw_plan = False
        #
        name = ''
        highway = False
        addr_housenumber = ''
        bridge = False
        # check whether definitions exist for this key value zoomlevel
        cur.execute('''
        SELECT wt.key,wt.value,
         md.layer,md.style,md.width,md.fill,md.stroke,md.dash
        FROM way_tags AS wt
        LEFT JOIN map_def AS md ON wt.key=md.key AND wt.value LIKE md.value AND md.zoomlevel=?
        WHERE wt.way_id=?
        ''', (zoomlevel, way_id))
        for (key, value, layer, style, width, fill, stroke, dash) in cur.fetchall():
            if layer is not None:
                cur.execute('INSERT INTO map_draw_plan VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                           (draw_plan_id, 'way', way_id, key, value, layer, style, width, fill, stroke, dash))
                insert_draw_plan = True
            # Modifieres ggf. merken
            if key == 'name':
                name = value
            elif key == 'highway' and value != 'platform':
                highway = True
            elif key == 'addr:housenumber':   # TODO erst ab zoomlevel 17
                addr_housenumber = value
            elif key == 'bridge':
                bridge = True
            elif key == 'tracktype':
                pass
                # TODO https://wiki.openstreetmap.org/wiki/DE:Key:tracktype
        # Daten modifizieren
        if insert_draw_plan:
            if bridge and zoomlevel >= 16:
                cur.execute('UPDATE map_draw_plan SET layer=layer+4 WHERE draw_plan_id=?', (draw_plan_id,))
            if not highway:
                cur.execute("DELETE FROM map_draw_plan WHERE draw_plan_id=? AND style='text'", (draw_plan_id,))
        else:
            cur.execute('INSERT INTO map_ways_unknown VALUES (?)', (way_id,))
    #
    # Alle noch unbekannten ways untersuchen ob sie Teil einer Relation sind
    #
    cur.execute('''
    SELECT wu.way_id,rm.relation_id
    FROM map_ways_unknown AS wu
    LEFT JOIN relation_members AS rm ON wu.way_id=rm.ref_id AND rm.ref='way'
    ''')
    for (way_id, relation_id) in cur.fetchall():
        draw_plan_id += 1
        if relation_id is not None:
            cur.execute('''
            SELECT rt.relation_id,rt.key,rt.value,
             md.layer,md.style,md.width,md.fill,md.stroke,md.dash
            FROM relation_tags AS rt
            LEFT JOIN map_def AS md ON rt.key=md.key AND rt.value LIKE md.value AND md.zoomlevel=?
            WHERE rt.relation_id=?
            ''', (zoomlevel, relation_id))
            for (relation_id, key, value, layer, style, width, fill, stroke, dash) in cur.fetchall():
                if layer is not None:
                    cur.execute('INSERT INTO map_draw_plan VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                               (draw_plan_id, 'relation', relation_id, key, value, layer, style, width, fill, stroke, dash))
                    cur.execute('DELETE FROM map_ways_unknown WHERE way_id=?', (way_id,))
    #
    # Unbekannte Wege ggf. als rote Linien anzeigen
    #
    if show_unknown:
        cur.execute('SELECT way_id FROM map_ways_unknown')
        for (way_id,) in cur.fetchall():
            cur.execute("INSERT INTO map_draw_plan VALUES (1,'way',?,'xxx','xxx',99,'line',2,'None','#ff0000','')", (way_id,))
    #
    # Draw Plan abarbeiten
    #
    cur.execute('''
    -- wichtig: '&' durch '&amp;' ersetzen
    SELECT ref,ref_id,key,replace(value,'&','&amp;'),layer,style,width,fill,stroke,dash
    FROM map_draw_plan
    ORDER BY layer
    ''')
    for (ref, ref_id, key, value, layer, style, width, fill, stroke, dash) in cur.fetchall():
        # f.write('<!-- DRAW_PLAN :',ref,ref_id,key,value,layer,style,width,fill,stroke,dash,'-->')
        path_id = ref + str(ref_id)
        #
        if style == 'text':
            f.write(f'<text style="fill:{fill};" font-size="{width}">\n')
            f.write('<textPath href="#' + path_id + '" startOffset="30%">' + value + '</textPath>\n')
            f.write('</text>\n')
            continue
        #
        svg_path = []
        if ref == 'way':
            cur.execute('''
            SELECT n.lon,n.lat
            FROM way_nodes AS wn
            LEFT JOIN nodes AS n ON wn.node_id=n.node_id
            WHERE wn.way_id=?
            ORDER BY wn.node_order
            ''', (ref_id,))
        elif ref == 'relation':
            cur.execute('''
            SELECT
             DISTINCT
             --rm.relation_id,rm.ref,rm.ref_id,rm.role,rm.member_order,
             --wn.node_id,wn.node_order,
             n.lon,n.lat
            FROM relation_members AS rm
            LEFT JOIN way_nodes AS wn ON rm.ref_id=wn.way_id
            LEFT JOIN nodes AS n ON wn.node_id=n.node_id
            WHERE rm.relation_id=? AND rm.ref='way' AND rm.role='outer'
            ORDER BY rm.member_order,wn.node_order
            ''', (ref_id,))
        else:
            print('Error draw plan - abort')
            sys.exit(1)
        for (lon, lat) in cur.fetchall():
            x, y = spherical_to_pixel(lon, lat, pixel_world_map)
            x -= bbox_min_x
            y -= bbox_min_y
            y = bbox_y - y
            svg_path.append((x, y))
        #
        if len(svg_path) > 0:
            if svg_path[len(svg_path)-1][0] < svg_path[0][0]:
                svg_path.reverse()
            #
            f.write(f'<path id="{path_id}" d="')
            command = 'M'
            for x, y in svg_path:
                f.write(f'{command}{x} {y} ')
                if command == 'M':
                    command = 'L'
            #
            if style == 'line':
                f.write(f'" style="fill:none;stroke:{stroke};stroke-width:{width};stroke-linecap:round;stroke-dasharray:{dash}" />\n')
            elif style == 'area':
                f.write(f'Z" style="fill:{fill};stroke:{stroke};stroke-width:{width}" />\n')
    f.write('</svg>')
    f.close()


def main():
    """entry point"""
    if len(sys.argv) == 1:
        print('Creates a simple map in SVG format.\n'
              'Usage:\n'
              f'{sys.argv[0]} DATABASE LON LAT ZOOMLEVEL SIZE_X SIZE_Y SVG_FILE [debug]')
        sys.exit(1)
    con = sqlite3.connect(sys.argv[1])  # database connection
    cur = con.cursor()                  # new database cursor
    lon = float(sys.argv[2])
    lat = float(sys.argv[3])
    zoomlevel = int(sys.argv[4])
    bbox_x = int(sys.argv[5])
    bbox_y = int(sys.argv[6])
    svgfile = sys.argv[7]
    show_unknown = False
    if len(sys.argv) == 9:
        if sys.argv[8] == 'debug':
            show_unknown = True
    drawmap(cur, lon, lat, zoomlevel, bbox_x, bbox_y, svgfile, show_unknown)


if __name__ == "__main__":
    main()
