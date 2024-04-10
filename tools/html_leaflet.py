#!/usr/bin/env python
"""
Simple Python Leaflet.js Wrapper
"""


class Leaflet:
    """
    A class used to produce HTML file with Leaflet.js
    """
    def __init__(self, html_filename):
        """Initialize the class attributes:
        Color and size properties (init value):
          color        : hexcolor or 'none'       ('#0000ff')
          opacity      : opacity from 0 to 1      (0.5)
          weight       : line thickness in px     (4)
          dasharray    : examples: '5 5', '2 8 4' ('none')
          fillcolor    : hexcolor or 'none'       ('#ff7800')
          fillopacity  : opacity from 0 to 1      (0.5)
        """
        self.file = open(html_filename, 'w', encoding='utf-8')
        self.bbox = {'min_lon': 180, 'min_lat': 90, 'max_lon': -180, 'max_lat': -90}
        self.p = {
          'color': '#0000ff',
          'opacity': 0.5,
          'weight': 4,
          'dasharray': 'none',
          'fillcolor': '#ff7800',
          'fillopacity': 0.5
        }

    def __del__(self):
        """destructor, close the file"""
        self.file.close()

    def adjust_boundingbox(self, lon, lat):
        """Adjusts boundingbox."""
        self.bbox['min_lon'] = min(self.bbox['min_lon'], lon)
        self.bbox['min_lat'] = min(self.bbox['min_lat'], lat)
        self.bbox['max_lon'] = max(self.bbox['max_lon'], lon)
        self.bbox['max_lat'] = max(self.bbox['max_lat'], lat)

    def lonlat2str(self, lonlat):
        """Converts a list [(lon1,lat1),(lon2,lat2),...] into
        a string with JavaScript array code."""
        latlon_str = ''
        for lon, lat in lonlat:
            if latlon_str != '':
                latlon_str += ',\n'
            latlon_str += '[' + str(lat) + ',' + str(lon) + ']'
            self.adjust_boundingbox(lon, lat)
        return latlon_str

    def set_property(self, properties):
        """Changes the properties as they are specified in the dictionary properties."""
        for k, v in properties.items():
            self.p[k] = v

    def write_html_footer(self):
        """Write HTML footer and close the file"""
        self.file.write('\n</body>\n</html>')
        self.file.close()

    def write_html_header(self, title):
        """Write HTML header with link to Leaflet 1.5.1 and a simple CSS."""
        # Leaflet 1.5.1
        # https://leafletjs.com/reference-1.5.1.html
        # Documentation: https://web.archive.org/web/20201202155513/https://leafletjs.com/reference-1.5.1.html
        # https://leafletjs.com/examples/quick-start/
        self.file.write(f'''<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>
''')
        self.file.write('''
<style>
body {
 font-family: Verdana, Arial;
 font-size: 1.0em;
 color: #bbbbbb;
 background: #333333;
}
table {
 border: 2px solid #bbbbbb;
 border-collapse: collapse;
}
th {
 border: 1px solid #cccccc;
 background: #555555;
}
td {
 border: 1px solid #aaaaaa;
}
a {
 color: #68B0FD;
}
</style>
</head>
<body>
''')

    def write_html_code(self, html_code):
        """Write HTML code in the file"""
        self.file.write(html_code)

    def write_script_start(self):
        """Write tag <script> and JavaScript code to init Leaflet.js."""
        self.file.write('''
<script>
// define boundingbox
var map_boundingbox = [ [ 52.5, 13.3 ], [ 52.8, 13.5 ] ];
resize_boundingbox();

// init map with given boundingbox
var mymap = L.map('mapid').fitBounds( map_boundingbox, {padding: [0,0], maxZoom: 19} );

// init tile server
var tile_server = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';  // OpenStreetMap's Standard tile layer
//var tile_server = 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png';  // Wikimedia Maps
L.tileLayer( tile_server, {
   maxZoom: 19,
   attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(mymap);

// show scale
L.control.scale( { position: 'bottomleft', maxWidth: 200, metric:true, imperial:false } ).addTo(mymap);
''')

    def add_marker(self, lon, lat, popuptext='', openpopup=False):
        """Write Leaflet.js code to display a marker."""
        self.file.write(f'L.marker([{lat}, {lon}])')
        if popuptext != '':
            self.file.write(f".bindPopup('{popuptext}')")
        self.file.write('.addTo(mymap)')
        if openpopup:
            self.file.write('.openPopup()')
        self.file.write(';\n')
        self.adjust_boundingbox(lon, lat)

    def add_polyline(self, lonlat):
        """Write Leaflet.js code to display a polyline."""
        lat_lon_str = self.lonlat2str(lonlat)
        self.file.write(f'L.polyline( [ {lat_lon_str} ]')
        self.file.write(f", {{ color:'{self.p['color']}', opacity:{self.p['opacity']}, weight:{self.p['weight']}, dashArray:'{self.p['dasharray']}', stroke:true }} )")
        self.file.write('.addTo(mymap);\n')

    def add_line(self, lon1, lat1, lon2, lat2):
        """Write Leaflet.js code to display a simple line."""
        self.add_polyline([(lon1, lat1), (lon2, lat2)])   # wrapper for a simple line

    def add_polygon(self, lonlat, popuptext=''):
        """Write Leaflet.js code to display a polygon."""
        lat_lon_str = self.lonlat2str(lonlat)
        self.file.write(f'L.polygon( [ {lat_lon_str} ]')
        self.file.write(f", {{ color:'{self.p['color']}', opacity:{self.p['opacity']}, weight:{self.p['weight']}, dashArray:'{self.p['dasharray']}', stroke:true }} )")
        self.file.write(".addTo(mymap)")
        if popuptext != '':
            self.file.write(f".bindPopup('{popuptext}')")
        self.file.write(';\n')

    def add_circle(self, lon, lat, radius, popuptext=''):
        """Write Leaflet.js code to display a circle."""
        self.file.write(f'L.circle([{lat}, {lon}], {radius}')
        self.file.write(f", {{ color:'{self.p['color']}', opacity:{self.p['opacity']}, weight:{self.p['weight']}, dashArray:'{self.p['dasharray']}', fillColor:'{self.p['fillcolor']}', fillOpacity:{self.p['fillopacity']} }} )")
        self.file.write(".addTo(mymap)")
        if popuptext != '':
            self.file.write(f".bindPopup('{popuptext}')")
        self.file.write(';\n')
        self.adjust_boundingbox(lon, lat)

    def add_circlemarker(self, lon, lat):
        """Write Leaflet.js code to display a circlemarker."""
        self.file.write(f'L.circleMarker([{lat}, {lon}]')
        self.file.write(f", {{ color:'{self.p['color']}', opacity:{self.p['opacity']}, weight:{self.p['weight']}, dashArray:'{self.p['dasharray']}', fillColor:'{self.p['fillcolor']}', fillOpacity:{self.p['fillopacity']} }} )")
        self.file.write(".addTo(mymap);\n")
        self.adjust_boundingbox(lon, lat)

    def add_rectangle(self, lon1, lat1, lon2, lat2, popuptext=''):
        """Write Leaflet.js code to display a rectangle."""
        self.file.write(f'L.rectangle( [ [ {lat1}, {lon1} ], [ {lat2}, {lon2} ] ]')
        self.file.write(f", {{ color:'{self.p['color']}', opacity:{self.p['opacity']}, weight:{self.p['weight']}, dashArray:'{self.p['dasharray']}', fillColor:'{self.p['fillcolor']}', fillOpacity:{self.p['fillopacity']} }} )")
        self.file.write(".addTo(mymap)")
        if popuptext != '':
            self.file.write(f".bindPopup('{popuptext}')")
        self.file.write(';\n')
        self.adjust_boundingbox(lon1, lat1)
        self.adjust_boundingbox(lon2, lat2)

    def write_script_end(self):
        """Write JavaScript code to finish Leaflet.js code and tag </script>."""
        self.file.write(f'''
//
function resize_boundingbox() {{
    map_boundingbox = [ [ {self.bbox['min_lat']}, {self.bbox['min_lon']} ], [ {self.bbox['max_lat']}, {self.bbox['max_lon']} ] ];
}}

// show popup with coordinates at mouse click
var popup = L.popup();
function onMapClick(e) {{
    // copy coordinates in new object
    var geo = e.latlng;
    var lat = geo.lat;
    var lon = geo.lng;
    // round to 7 decimal places
    lat = lat.toFixed(7);
    lon = lon.toFixed(7);
    // output coordinates and zoomlevel on console
    console.log( 'mouse clicked at ' +
     ' lon: ' + lon + ' lat: ' + lat +
     ' zoomlevel: ' + mymap.getZoom() +
     ' Leaflet version: ' + L.version
      );
    //
    var popuptext = '<pre>Länge  : '+lon+'&deg;<br>Breite : '+lat+'&deg;<br>';
    popup.setLatLng(e.latlng).setContent(popuptext).openOn(mymap);
}}
mymap.on('click', onMapClick);

</script>
''')


if __name__ == "__main__":
    print("This is a module, use 'import html_leaflet'")
    help(Leaflet)
