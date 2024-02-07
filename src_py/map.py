#!/usr/bin/env python
#
# Print map
#
# https://www.w3schools.com/graphics/svg_intro.asp
# https://de.wikipedia.org/wiki/Scalable_Vector_Graphics
#
import sys
import proj
import sqlite3


def draw_map(lon, lat, zoomlevel, bbox_x, bbox_y, show_unknown=True):
    """
    Outputs a map in SVG format to stdout.
    A table 'map_def' is required.
    """
    # map size
    pixel_world_map, meters_pixel = proj.size_world_map(zoomlevel)
    # pixel boundingbox
    bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = proj.pixel_boundingbox(lon, lat, pixel_world_map, bbox_x, bbox_y)
    # wgs84 boundingbox
    bbox_min_lon, bbox_min_lat = proj.pixel_to_wgs84(bbox_min_x, bbox_min_y, pixel_world_map)
    bbox_max_lon, bbox_max_lat = proj.pixel_to_wgs84(bbox_max_x, bbox_max_y, pixel_world_map)
    #
    db.execute('''CREATE TEMP TABLE map_draw_plan (
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
    db.execute('CREATE TEMP TABLE map_ways_unknown (way_id)')
    #
    print(f'<svg height="{bbox_y}" width="{bbox_x}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')
    # TODO eventuell text-anchor="middle" ?
    print('''
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
    ''')
    print('<!-- ************ map info ************')
    print(f'lon       : {lon}\n' +
          f'lat       : {lat}\n' +
          f'zoomlevel : {zoomlevel}\n' +
          f'size_x    : {bbox_x} (= bbox_x)\n' +
          f'size_y    : {bbox_y} (= bbox_y)\n')
    print(f'pixel_world_map : {pixel_world_map}px x {pixel_world_map}px\n')
    print('pixel boundingbox:\n' +
          f'bbox_min_x, bbox_min_y : {bbox_min_x}, {bbox_min_y}\n' +
          f'bbox_max_x, bbox_max_y : {bbox_max_x}, {bbox_max_y}\n')
    print('wgs84 boundingbox:\n' +
          f'bbox_min_lon, bbox_min_lat : {bbox_min_lon}, {bbox_min_lat}\n' +
          f'bbox_max_lon, bbox_max_lat : {bbox_max_lon}, {bbox_max_lat}\n')
    print('check:')
    print('bbox_max_x - bbox_min_x = bbox_x = size_x : ', bbox_max_x - bbox_min_x)
    print('bbox_max_y - bbox_min_y = bbox_y = size_y : ', bbox_max_y - bbox_min_y)
    print('************ map info ************ -->')
    #
    print('<rect width="100%" height="100%" fill="#f2efe9" />')
    #
    draw_plan_id = 0
    db.execute('''
    SELECT way_id
    FROM rtree_way
    WHERE max_lon>=? AND min_lon<=?
     AND  max_lat>=? AND min_lat<=?
    ''', (bbox_min_lon, bbox_max_lon, bbox_min_lat, bbox_max_lat))
    for (way_id,) in db.fetchall():
        draw_plan_id += 1
        insert_draw_plan = False
        #
        name = ''
        highway = False
        addr_housenumber = ''
        bridge = False
        # check whether definitions exist for this key value zoomlevel
        db.execute('''
        SELECT wt.key,wt.value,
         md.layer,md.style,md.width,md.fill,md.stroke,md.dash
        FROM way_tags AS wt
        LEFT JOIN map_def AS md ON wt.key=md.key AND wt.value LIKE md.value AND md.zoomlevel=?
        WHERE wt.way_id=?
        ''', (zoomlevel, way_id))
        for (key, value, layer, style, width, fill, stroke, dash) in db.fetchall():
            if layer is not None:
                db.execute('INSERT INTO map_draw_plan VALUES (?,?,?,?,?,?,?,?,?,?,?)',
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
                db.execute('UPDATE map_draw_plan SET layer=layer+4 WHERE draw_plan_id=?', (draw_plan_id,))
            if not highway:
                db.execute("DELETE FROM map_draw_plan WHERE draw_plan_id=? AND style='text'", (draw_plan_id,))
        else:
            db.execute('INSERT INTO map_ways_unknown VALUES (?)', (way_id,))
    #
    # Alle noch unbekannten ways untersuchen ob sie Teil einer Relation sind
    #
    db.execute('''
    SELECT wu.way_id,rm.relation_id
    FROM map_ways_unknown AS wu
    LEFT JOIN relation_members AS rm ON wu.way_id=rm.ref_id AND rm.ref='way'
    ''')
    for (way_id, relation_id) in db.fetchall():
        draw_plan_id += 1
        if relation_id is not None:
            db.execute('''
            SELECT rt.relation_id,rt.key,rt.value,
             md.layer,md.style,md.width,md.fill,md.stroke,md.dash
            FROM relation_tags AS rt
            LEFT JOIN map_def AS md ON rt.key=md.key AND rt.value LIKE md.value AND md.zoomlevel=?
            WHERE rt.relation_id=?
            ''', (zoomlevel, relation_id))
            for (relation_id, key, value, layer, style, width, fill, stroke, dash) in db.fetchall():
                if layer is not None:
                    db.execute('INSERT INTO map_draw_plan VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                               (draw_plan_id, 'relation', relation_id, key, value, layer, style, width, fill, stroke, dash))
                    db.execute('DELETE FROM map_ways_unknown WHERE way_id=?', (way_id,))
    #
    # Unbekannte Wege ggf. als rote Linien anzeigen
    #
    if show_unknown:
        db.execute('SELECT way_id FROM map_ways_unknown')
        for (way_id,) in db.fetchall():
            db.execute("INSERT INTO map_draw_plan VALUES (1,'way',?,'xxx','xxx',99,'line',2,'None','#ff0000','')", (way_id,))
    #
    # Draw Plan abarbeiten
    #
    db.execute('''
    -- wichtig: '&' durch '&amp;' ersetzen
    SELECT ref,ref_id,key,replace(value,'&','&amp;'),layer,style,width,fill,stroke,dash
    FROM map_draw_plan
    ORDER BY layer
    ''')
    for (ref, ref_id, key, value, layer, style, width, fill, stroke, dash) in db.fetchall():
        # print('<!-- DRAW_PLAN :',ref,ref_id,key,value,layer,style,width,fill,stroke,dash,'-->')
        path_id = ref + str(ref_id)
        #
        if style == 'text':
            print(f'<text style="fill:{fill};" font-size="{width}">', end='')
            print('<textPath href="#' + path_id + '" startOffset="30%">' + value + '</textPath>', end='')
            print('</text>')
            continue
        #
        svg_path = []
        if ref == 'way':
            db.execute('''
            SELECT n.lon,n.lat
            FROM way_nodes AS wn
            LEFT JOIN nodes AS n ON wn.node_id=n.node_id
            WHERE wn.way_id=?
            ORDER BY wn.node_order
            ''', (ref_id,))
        elif ref == 'relation':
            db.execute('''
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
        for (lon, lat) in db.fetchall():
            x, y = proj.wgs84_to_pixel(lon, lat, pixel_world_map)
            x -= bbox_min_x
            y -= bbox_min_y
            y = bbox_y - y
            svg_path.append((x, y))
        #
        if len(svg_path) > 0:
            if svg_path[len(svg_path)-1][0] < svg_path[0][0]:
                svg_path.reverse()
            #
            print(f'<path id="{path_id}" d="', end='')
            command = 'M'
            for x, y in svg_path:
                print(f'{command}{x} {y} ', end='')
                if command == 'M':
                    command = 'L'
            #
            if style == 'line':
                print(f'" style="fill:none;stroke:{stroke};stroke-width:{width};stroke-linecap:round;stroke-dasharray:{dash}" />')
            elif style == 'area':
                print(f'Z" style="fill:{fill};stroke:{stroke};stroke-width:{width}" />')
    print('</svg>')


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Creates a simple map in SVG format on stdout.\n'
              'Usage:\n'
              f'{sys.argv[0]} DATABASE LON LAT ZOOMLEVEL SIZE_X SIZE_Y [debug]')
        sys.exit(1)
    db_connect = sqlite3.connect(sys.argv[1])  # database connection
    db = db_connect.cursor()                   # new database cursor
    lon = float(sys.argv[2])
    lat = float(sys.argv[3])
    zoomlevel = int(sys.argv[4])
    bbox_x = int(sys.argv[5])
    bbox_y = int(sys.argv[6])
    show_unknown = False
    if len(sys.argv) == 8:
        if sys.argv[7] == 'debug':
            show_unknown = True
    draw_map(lon, lat, zoomlevel, bbox_x, bbox_y, show_unknown)
