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
    Print a simple map to stdout.
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
    db.execute('CREATE TEMP TABLE map_draw_plan (ref,ref_id,layer,style,width,fill,stroke,dash)')
    db.execute('CREATE TEMP TABLE map_ways_unknown (way_id)')
    #
    print(f'<svg height="{bbox_y}" width="{bbox_x}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')
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
    db.execute('''
    SELECT way_id
    FROM rtree_way
    WHERE max_lon>=? AND min_lon<=?
     AND  max_lat>=? AND min_lat<=?
    ''', (bbox_min_lon, bbox_max_lon, bbox_min_lat, bbox_max_lat))
    for (way_id,) in db.fetchall():
        ###print('way_id', way_id)
        way_draw_plan = []
        name = ''
        addr_housenumber = ''
        bridge = False
        db.execute('''
        SELECT wt.way_id,wt.key,wt.value,
         md.layer,md.style,md.width,md.fill,md.stroke,md.dash
        FROM way_tags AS wt
        LEFT JOIN map_def AS md ON wt.key=md.key AND wt.value LIKE md.value AND md.zoomlevel=?
        WHERE wt.way_id=?
        ''', (zoomlevel, way_id))
        for (way_id, key, value, layer, style, width, fill, stroke, dash) in db.fetchall():
            ###print(f'  {key} # {value}')
            if layer is not None:
                way_draw_plan.append({'style': style, 'way_id': way_id, 'key': key, 'value': value,
                  'layer': layer, 'width': width, 'fill': fill, 'stroke': stroke, 'dash': dash, 'name': ''})
            if key == 'name':
                ###print('==merken==>', way_id, key, value)
                name = value
            elif key == 'addr:housenumber':   # TODO erst ab zoomlevel 17
                ###print('==merken==>', way_id, key, value)
                addr_housenumber = value
            elif key == 'bridge':
                bridge = True
            elif key == 'tracktype':
                pass
                # TODO https://wiki.openstreetmap.org/wiki/DE:Key:tracktype
        if len(way_draw_plan) > 0:
            # Daten modifizieren
            for d in way_draw_plan:
                ###print('orig:', d)
                d.update({'name': name})
                if bridge:
                    layer = d['layer']
                    layer += 2
                    d.update({'layer': layer})
            # Daten in Tabelle "map_draw_plan" einfügen
            for d in way_draw_plan:
                ###print('mod:',d)
                db.execute('INSERT INTO map_draw_plan VALUES (?,?,?,?,?,?,?,?)',
                  ('way', d['way_id'], d['layer'], d['style'], d['width'], d['fill'], d['stroke'], d['dash']))
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
                    db.execute('INSERT INTO map_draw_plan VALUES (?,?,?,?,?,?,?,?)',
                      ('relation', relation_id, layer, style, width, fill, stroke, dash))
                    db.execute('DELETE FROM map_ways_unknown WHERE way_id=?', (way_id,))
    #
    # Unbekannte Wege ggf. als rote Linien anzeigen
    #
    if show_unknown:
        db.execute('SELECT way_id FROM map_ways_unknown')
        for (way_id,) in db.fetchall():
            db.execute("INSERT INTO map_draw_plan VALUES ('way',?,99,'line',2,'None','#ff0000','')", (way_id,))
    #
    # Draw Plan abarbeiten
    #
    db.execute('''
    SELECT ref,ref_id,layer,style,width,fill,stroke,dash
    FROM map_draw_plan
    ORDER BY layer
    ''')
    for (ref, ref_id, layer, style, width, fill, stroke, dash) in db.fetchall():
        # print('<!-- DRAW_PLAN :',ref,ref_id,layer,style,width,fill,stroke,dash,'-->')
        path_id = ref + str(ref_id)
        print(f'<path id="{path_id}" d="', end='')
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
        #
        command = 'M'
        for (lon, lat) in db.fetchall():
            x, y = proj.wgs84_to_pixel(lon, lat, pixel_world_map)
            x -= bbox_min_x
            y -= bbox_min_y
            y = bbox_y - y
            # <path id="999" d="M150 400 L220 360 L400 400 L500 280 " style="fill:none;stroke:#aaaaaa;stroke-width:15" />
            print(f'{command}{x} {y} ', end='')
            if command == 'M':
                command = 'L'
        if style == 'line':
            #print(f'" style="fill:none;stroke:{stroke};stroke-width:{width};stroke-linecap:round" />')
            print(f'" style="fill:none;stroke:{stroke};stroke-width:{width};stroke-linecap:round;stroke-dasharray:{dash}" />')
        elif style == 'area':
            print(f'Z" style="fill:{fill};stroke:{stroke};stroke-width:{width}" />')
    print('</svg>')


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(f'''
Creates a simple map in SVG format on stdout.
Usage:
{sys.argv[0]} DATABASE LON LAT ZOOMLEVEL SIZE_X SIZE_Y
        ''')
        sys.exit(1)
    db_connect = sqlite3.connect(sys.argv[1])  # database connection
    db = db_connect.cursor()                   # new database cursor
    lon = float(sys.argv[2])
    lat = float(sys.argv[3])
    zoomlevel = int(sys.argv[4])
    bbox_x = int(sys.argv[5])
    bbox_y = int(sys.argv[6])
    draw_map(lon, lat, zoomlevel, bbox_x, bbox_y, True)
