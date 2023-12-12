#!/usr/bin/env python
#
# Print map Next Generation
#
# https://www.w3schools.com/graphics/svg_intro.asp
# https://de.wikipedia.org/wiki/Scalable_Vector_Graphics
#
import sys
import proj
import sqlite3

def draw_map(lon, lat, zoomlevel, bbox_x, bbox_y):
    """
    TODO
    """
    # map size
    pixel_world_map, meters_pixel = proj.size_world_map(zoomlevel)
    # pixel boundingbox
    bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = proj.pixel_boundingbox(lon, lat, pixel_world_map, bbox_x, bbox_y)
    # wgs84 boundingbox
    bbox_min_lon, bbox_min_lat = proj.pixel_to_wgs84(bbox_min_x, bbox_min_y, pixel_world_map)
    bbox_max_lon, bbox_max_lat = proj.pixel_to_wgs84(bbox_max_x, bbox_max_y, pixel_world_map)
    #
    db.execute('CREATE TEMP TABLE map_draw_plan (type,type_id,layer,style,width,fill,stroke,dash)')
    db.execute('CREATE TEMP TABLE map_ways_unknown (way_id)')
    #
    print(f'<svg height="{bbox_y}" width="{bbox_x}">')
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
    print('<rect width="100%" height="100%" fill="#e0dfdf" />')
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
            if layer != None:
                ###print('==draw_plan==>', way_id, key, value, layer, style, width, fill, stroke, dash)
                way_draw_plan.append({'style':style, 'way_id':way_id, 'key':key, 'value':value,
                  'layer':layer, 'width':width, 'fill':fill, 'stroke':stroke, 'dash':dash, 'name':''})
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
                d.update({'name':name})
                if bridge:
                    layer = d['layer']
                    layer += 2
                    d.update({'layer':layer})
            # Daten in Tabelle "map_draw_plan" einfügen
            for d in way_draw_plan:
                ###print('mod:',d)
                db.execute('INSERT INTO map_draw_plan VALUES (?,?,?,?,?,?,?,?)',
                  ('way',d['way_id'],d['layer'],d['style'],d['width'],d['fill'],d['stroke'],d['dash']))
        else:
            db.execute('INSERT INTO map_ways_unknown VALUES (?)', (way_id,))
    #
    # Alle Relationen ermitteln die ways ohne draw_plan haben
    #
    db.execute('''
    SELECT rm.relation_id
    FROM relation_members AS rm
    WHERE rm.ref IN (SELECT way_id FROM map_ways_unknown)
    ''')
    for (relation_id,) in db.fetchall():
        ###print('relation_id', relation_id)
        db.execute('''
        SELECT rt.relation_id,rt.key,rt.value,
         md.layer,md.style,md.width,md.fill,md.stroke,md.dash
        FROM relation_tags AS rt
        LEFT JOIN map_def AS md ON rt.key=md.key AND rt.value LIKE md.value AND md.zoomlevel=?
        WHERE rt.relation_id=?
        ''', (zoomlevel, relation_id))
        for (relation_id, key, value, layer, style, width, fill, stroke, dash) in db.fetchall():
            ###print(f'  {key} # {value}')
            if layer != None:
                ###print('==draw_plan==>', relation_id, key, value, layer, style, width, fill, stroke, dash)
                db.execute('INSERT INTO map_draw_plan VALUES (?,?,?,?,?,?,?,?)',
                  ('relation',relation_id,layer,style,width,fill,stroke,dash))
    #
    # Draw Plan abarbeiten
    #
    db.execute('''
    SELECT type,type_id,layer,style,width,fill,stroke,dash
    FROM map_draw_plan
    ORDER BY layer
    ''')
    for (type,type_id,layer,style,width,fill,stroke,dash) in db.fetchall():
        print('<!-- DRAW PLAN',type,type_id,layer,style,width,fill,stroke,dash,'-->')
        # TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST
        print('<path id="" d="', end='')
        if type == 'way':
            db.execute('''
            SELECT n.lon,n.lat
            FROM way_nodes AS wn
            LEFT JOIN nodes AS n ON wn.node_id=n.node_id
            WHERE wn.way_id=?
            ORDER BY wn.node_order
            ''', (type_id,))
        elif type == 'relation':
            db.execute('''
            SELECT
             DISTINCT
             --rm.relation_id,rm.type,rm.ref,rm.role,rm.member_order,
             --wn.node_id,wn.node_order,
             n.lon,n.lat
            FROM relation_members AS rm
            LEFT JOIN way_nodes AS wn ON rm.ref=wn.way_id
            LEFT JOIN nodes AS n ON wn.node_id=n.node_id
            WHERE rm.relation_id=? AND rm.type='way'
            ORDER BY rm.member_order,wn.node_order
            ''', (type_id,))
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
    #
    # Debug: Unbekannte Wege als rote Linien anzeigen
    #
    # TODO
    print('</svg>')

#
# Grenze Friedhof St. Georgen
# Ways 914496150 und 1040222686 sind Teil von Relation 13923337
#
# Gebäude mit Innenhöfen
# Beispiel Staudinger Gesamtschule:
# Relation: 4176098
#   -> 5 Mitglieder:
#      Weg 311811960 als inner
#      Weg 311811961 als inner
#      Weg 311811963 als inner
#      Weg 311811962 als inner
#      Weg 24756034 als outer

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
    draw_map(lon, lat, zoomlevel, bbox_x, bbox_y)
