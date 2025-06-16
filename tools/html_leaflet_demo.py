#!/usr/bin/env python
"""
Demo Leaflet.js Wrapper
"""
import html_leaflet

HTML_FILENAME = 'demo.html'

m = html_leaflet.Leaflet(HTML_FILENAME)
m.write_html_header('Demo Map')
m.write_html_code('''
<h1>Test Leaflet.js Python Wrapper</h1>
<p><div id="mapid" style="width: 100%; height: 700px;"></div></p>
''')
m.write_script_start()
# add Marker
m.add_marker(13.3757533, 52.5185551, 'Berlin Reichstag', True)
# add circle 1 (with default colors)
m.add_circle(13.3634942, 52.5143171, 300, 'This is a circle with default colors')
# add circle 2 (set every property manually)
m.set_property({'color': '#bb1122'})
m.set_property({'opacity': 0.6})
m.set_property({'fillcolor': '#ffffff'})
m.set_property({'fillopacity': 0.6})
m.add_circle(13.384, 52.517, 200, 'This is a white circle')
# add circle 3 (set all 6 properties at once)
m.set_property(
  {'color': '#992255', 'opacity': 1.0, 'weight': 4, 'dasharray': '4 7',
   'fillcolor': '#ff0000', 'fillopacity': 0.3}
)
m.add_circle(13.3657672, 52.5183113, 200, 'This is a dotted circle')
# add line
m.set_property(
  {'color': '#ff0000', 'opacity': 0.6, 'weight': 6, 'dasharray': '',
   'fillcolor': '#00ffff', 'fillopacity': 0.7}
)
m.add_line(13.369, 52.513, 13.376, 52.514)
# add polyline
# all coordinates in a list with sets [(lon1, lat1), (lon2, lat2), (lon3, lat3), ...]
lonlat = [(13.368, 52.519), (13.372, 52.514), (13.382, 52.519), (13.378, 52.522)]
m.add_polyline(lonlat)
# add polygon
lonlat = [(13.367, 52.511), (13.373, 52.513), (13.376, 52.511)]
m.set_property({'weight': 20})
m.add_polygon(lonlat, 'This is a polygon')
# add rectangle
m.set_property(
  {'color': '#005588', 'opacity': 1.0, 'weight': 3, 'dasharray': 'none',
   'fillcolor': '#005588', 'fillopacity': 0.3}
)
m.add_rectangle(13.3788740, 52.5152569, 13.3856956, 52.5104557, 'This is a rectangle')
# add circlemarker
m.set_property(
  {'color': '#ffaa00', 'opacity': 1.0, 'weight': 10, 'dasharray': '5 5',
   'fillcolor': 'none', 'fillopacity': 1.0}
)
m.add_circlemarker(13.3868086, 52.5203199)
# finally add a red dotted rectangle with the coordinates of the boundingbox
m.set_property(
  {'color': '#ff0000', 'opacity': 1.0, 'weight': 2, 'dasharray': '5 5',
   'fillcolor': 'none', 'fillopacity': 1.0}
)
m.add_rectangle(m.bbox['min_lon'], m.bbox['min_lat'], m.bbox['max_lon'], m.bbox['max_lat'], '')
# finish the javascript code
m.write_script_end()
m.write_html_footer()
del m

print(f'Example file "{HTML_FILENAME}" created')
