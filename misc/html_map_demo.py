#!/usr/bin/env python
#
# Demo Leaflet.js Wrapper
#
import html_leaflet

m1 = html_leaflet.Leaflet()
m1.print_html_header('Demo Map')
#
print('<h1>Test Leaflet.js Python Wrapper</h1>')
print('''
<p>
<div id="mapid" style="width: 100%; height: 700px;"></div>
</p>
''')
m1.print_script_start()
# add Marker
m1.add_marker(13.3757533, 52.5185551, 'Berlin Reichstag', True)
# add circle 1 (with default colors)
m1.add_circle(13.3634942, 52.5143171, 300, 'This is a circle with default colors')
# add circle 2 (set every property manually)
m1.set_color('#bb1122')
m1.set_opacity(0.6)
m1.set_fillcolor('#ffffff')
m1.set_fillopacity(0.6)
m1.add_circle(13.384, 52.517, 200, 'This is a white circle')
# add circle 3 (set all 6 properties at once)
m1.set_properties('#992255', 1.0, 4, '4 7', '#ff0000', 0.3)
m1.add_circle(13.3657672, 52.5183113, 200, 'This is a dotted circle')
# add line
m1.set_properties('#ff0000', 0.6, 6, '', '#00ffff', 0.7)
m1.add_line(13.369, 52.513, 13.376, 52.514)
# add polyline
# all coordinates in a list with sets [(lon1, lat1), (lon2, lat2), (lon3, lat3), ...]
lonlat = [(13.368, 52.519), (13.372, 52.514), (13.382, 52.519), (13.378, 52.522)]
m1.add_polyline(lonlat)
# add polygon
lonlat = [(13.367, 52.511), (13.373, 52.513), (13.376, 52.511)]
m1.set_weight(20)
m1.add_polygon(lonlat, 'This is a polygon')
# add rectangle
m1.set_properties('#005588', 1.0, 3, 'none', '#005588', 0.3)
m1.add_rectangle(13.3788740, 52.5152569, 13.3856956, 52.5104557, 'This is a rectangle')
# add circlemarker
m1.set_properties('#ffaa00', 1.0, 10, '5 5', 'none', 1.0)
m1.add_circlemarker(13.3868086, 52.5203199)
# finally add a red dotted rectangle with the coordinates of the boundingbox
m1.set_properties('#ff0000', 1.0, 2, '5 5', 'none', 1.0)
m1.add_rectangle(m1.bbox_min_lon, m1.bbox_min_lat, m1.bbox_max_lon, m1.bbox_max_lat, '')
# finish the javascript code
m1.print_script_end()
print('''
</body>
</html>
''')
