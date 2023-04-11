#
# Simple Python Leaflet.js Wrapper
#
# https://leafletjs.com/examples/quick-start/
#
# https://leafletjs.com/reference-1.5.1.html
#

class Leaflet:
    def __init__(self):
        self.bbox_min_lon =  180;
        self.bbox_min_lat =   90;
        self.bbox_max_lon = -180;
        self.bbox_max_lat =  -90;
        self.color        = '#0000ff';
        self.opacity      = 0.5;
        self.weight       = 4;
        self.dasharray    = 'none';      # '5 5' or 'none'
        self.fillcolor    = '#ff7800';   # hexcolor or 'none'
        self.fillopacity  = 0.5;
    #
    #
    #
    def adjust_boundingbox(self, lon, lat):
        if self.bbox_min_lon > lon:
            self.bbox_min_lon = lon
        if self.bbox_min_lat > lat:
            self.bbox_min_lat = lat
        if self.bbox_max_lon < lon:
            self.bbox_max_lon = lon
        if self.bbox_max_lat < lat:
            self.bbox_max_lat = lat
    def lonlat2str(self, lonlat):
        lat_lon_str = ''
        for i in range(0, len(lonlat), 2):
            if i>0:
                lat_lon_str += ','
            lat_lon_str += '[' + str(lonlat[i+1]) + ',' + str(lonlat[i]) + ']'
            self.adjust_boundingbox(lonlat[i], lonlat[i+1])
        return lat_lon_str
    #
    #
    #
    def set_color(self, new_color):
        self.color = new_color
        return True
    def set_opacity(self, new_opacity):
        self.opacity = new_opacity
        return True
    def set_weight(self, new_weight):
        self.weight = new_weight
        return True
    def set_dasharray(self, new_dasharray):
        self.dasharray = new_dasharray
        return True
    def set_fillcolor(self, new_fillcolor):
        self.fillcolor = new_fillcolor
        return True
    def set_fillopacity(self, new_fillopacity):
        self.fillopacity = new_fillopacity
        return True
    def set_properties(self, color, opacity, weight, dasharray, fillcolor, fillopacity):
        self.set_color(color)
        self.set_opacity(opacity)
        self.set_weight(weight)
        self.set_dasharray(dasharray)
        self.set_fillcolor(fillcolor)
        self.set_fillopacity(fillopacity)
        return True
    #
    #
    #
    def print_html_header(self, title):
        print(f'''
<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>
''')
        print('''
<style>
body {
 font-family: Verdana, Arial;
 font-size: 1.0em;
}
table {
 border: 2px solid #bbbbbb;
 border-collapse: collapse;
}
th {
 border: 1px solid #cccccc;
 font-size: 0.8em;
}
td {
 border: 1px solid #aaaaaa;
 font-size: 0.8em;
}
</style>
</head>
<body>
''')
    #
    #
    #
    def print_script_start(self):
        print('''
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
''')
    #
    #
    #
    def add_marker(self, lon, lat, popuptext, openpopup):
        print(f'L.marker([{lat}, {lon}])', end='')
        if popuptext != '':
            print(f".bindPopup('{popuptext}')", end='')
        print('.addTo(mymap)', end='')
        if openpopup:
            print(f'.openPopup()', end='')
        print(';')
        self.adjust_boundingbox(lon, lat)
    def add_polyline(self, lonlat):
        lat_lon_str = self.lonlat2str( lonlat )
        print(f'L.polyline( [ {lat_lon_str} ]', end='')
        print(f", {{ color:'{self.color}', opacity:{self.opacity}, weight:{self.weight}, dashArray:'{self.dasharray}', stroke:true }} )", end='')
        print(".addTo(mymap);")
    def add_line(self, lon1, lat1, lon2, lat2):
        self.add_polyline( [lon1, lat1, lon2, lat2] )   # wrapper for a simple line
    def add_polygon(self, lonlat, popuptext):
        lat_lon_str = self.lonlat2str( lonlat )
        print(f'L.polygon( [ {lat_lon_str} ]', end='')
        print(f", {{ color:'{self.color}', opacity:{self.opacity}, weight:{self.weight}, dashArray:'{self.dasharray}', stroke:true }} )", end='')
        print(".addTo(mymap)", end='')
        if popuptext != '':
            print(f".bindPopup('{popuptext}')", end='')
        print(';')
    def add_circle(self, lon, lat, radius, popuptext):
        print(f'L.circle([{lat}, {lon}], {radius}', end='')
        print(f", {{ color:'{self.color}', opacity:{self.opacity}, weight:{self.weight}, dashArray:'{self.dasharray}', fillColor:'{self.fillcolor}', fillOpacity:{self.fillopacity} }} )", end='')
        print(".addTo(mymap)", end='')
        if popuptext != '':
            print(f".bindPopup('{popuptext}')", end='')
        print(';')
        self.adjust_boundingbox(lon, lat)
    def add_circlemarker(self, lon, lat):
        print(f'L.circleMarker([{lat}, {lon}]', end='')
        print(f", {{ color:'{self.color}', opacity:{self.opacity}, weight:{self.weight}, dashArray:'{self.dasharray}', fillColor:'{self.fillcolor}', fillOpacity:{self.fillopacity} }} )", end='')
        print(".addTo(mymap);")
        self.adjust_boundingbox(lon, lat)
    def add_rectangle(self, lon1, lat1, lon2, lat2, popuptext):
        print(f'L.rectangle( [ [ {lat1}, {lon1} ], [ {lat2}, {lon2} ] ]', end='')
        print(f", {{ color:'{self.color}', opacity:{self.opacity}, weight:{self.weight}, dashArray:'{self.dasharray}', fillColor:'{self.fillcolor}', fillOpacity:{self.fillopacity} }} )", end='')
        print(".addTo(mymap)", end='')
        if popuptext != '':
            print(f".bindPopup('{popuptext}')", end='')
        print(';')
        self.adjust_boundingbox(lon1, lat1)
        self.adjust_boundingbox(lon2, lat2)
    #
    #
    #
    def print_script_end(self):
        print(f'''
//
function resize_boundingbox() {{
    map_boundingbox = [ [ {self.bbox_min_lat}, {self.bbox_min_lon} ], [ {self.bbox_max_lat}, {self.bbox_max_lon} ] ];
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
     ' lon: ' + lon +' lat: ' + lat +
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

