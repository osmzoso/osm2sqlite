#!/usr/bin/perl
#
# Erstellt eine Karte der Adressen aus der Datenbank 'osm_addr'.
# Die Datei wird im HTML-Format in $path$filename erstellt.
#
# Benutzung:
# $0 MIN_LON MIN_LAT MAX_LON MAX_LAT
#
use strict;
use utf8;
use DBI;
use POSIX;
use Encode qw(encode decode);

#
my $input_database = $ARGV[0];
my $output_htmlfile = './karte_osm_adressen.html';

# Datenbank verbinden
my $db = DBI->connect( "DBI:SQLite:$input_database" );

# Parameter auswerten
my $min_lon = $ARGV[1];
my $min_lat = $ARGV[2];
my $max_lon = $ARGV[3];
my $max_lat = $ARGV[4];

#
open(OUTFILE, '>'.$output_htmlfile);
zeige_osm_adressen( $min_lon, $min_lat, $max_lon, $max_lat );
close(OUTFILE);
print "Datei $output_htmlfile wurde erstellt.\n";

# Verbinden zur Datenbank trennen
$db->disconnect;


#---------------------------------------------------------------------------------------------------------------------
# Zeigt alle vorhandenen OSM-Adressen im Umkreis
#---------------------------------------------------------------------------------------------------------------------
sub zeige_osm_adressen {
my ( $min_lon, $min_lat, $max_lon, $max_lat ) = @_;   # Parameter

# Prüfen ob Parameter korrekt
if( $min_lon !~ /^[-+]?[0-9]*\.?[0-9]+$/ ) { die("Fehler: min_lon nicht numerisch\n"); }
if( $min_lat !~ /^[-+]?[0-9]*\.?[0-9]+$/ ) { die("Fehler: min_lat nicht numerisch\n"); }
if( $max_lon !~ /^[-+]?[0-9]*\.?[0-9]+$/ ) { die("Fehler: max_lon nicht numerisch\n"); }
if( $max_lat !~ /^[-+]?[0-9]*\.?[0-9]+$/ ) { die("Fehler: max_lat nicht numerisch\n"); }

# SQL-Abfrage erstellen
my $query = "
SELECT way_id,node_id,postcode,city,street,housenumber,lon,lat
FROM addr_view
WHERE lon>=$min_lon AND lat>=$min_lat AND lon<=$max_lon AND lat<=$max_lat
ORDER BY postcode,street,abs(housenumber)
";

# HTML Kopf
print OUTFILE "<script>\n";
print OUTFILE "// Boundingbox der anzuzeigenden Karte\n";
print OUTFILE "var CP_map_boundingbox = [ [ $min_lat, $min_lon ], [ $max_lat, $max_lon ] ];\n";
print OUTFILE "</script>\n";
print_html_header();

# Ausgabe der Leaflet-Marker
my $sth = $db->prepare($query);
$sth->execute();
while( my ( $way_id, $node_id, $plz, $ort, $strasse, $hausnummer, $laenge, $breite ) = $sth->fetchrow_array ) {

   # Javascript Marker setzen
   my $popup_text = '<pre>';
   $popup_text .= 'addr:postcode    : '.$plz.'<br>';
   $popup_text .= 'addr:city        : '.$ort.'<br>';
   $popup_text .= 'addr:street      : '.$strasse.'<br>';
   $popup_text .= 'addr:housenumber : '.$hausnummer.'<br>';
   $popup_text .= '</pre>';
   print OUTFILE "L.marker([$breite, $laenge]).bindPopup('$popup_text').addTo(mymap);\n";
}
$sth->finish();

# Rechteck Boundingbox
print OUTFILE "L.rectangle( [ [ $min_lat, $min_lon ], [ $max_lat, $max_lon ] ], { color:'#000068', fill:false, dashArray:'5 5', weight:3 } ).addTo(mymap);\n";

#
print OUTFILE "</script>\n";

# Ausgabe der Adressen-Liste
print OUTFILE "<table>\n";
print OUTFILE "<tr><th>way_id</th><th>node_id</th><th>addr:postcode</th><th>addr:city</th><th>addr:street</th><th>addr:housenumber</th><th>lon</th><th>lat</th></tr>\n";
my $sth = $db->prepare($query);
$sth->execute();
while( my ( $way_id, $node_id, $plz, $ort, $strasse, $hausnummer, $laenge, $breite ) = $sth->fetchrow_array ) {

   # Ausgabe formatiert auf stdout
   #print sprintf( "%-15s", $way_id ),' ';
   #print sprintf( "%-15s", $node_id ),' ';
   #print sprintf( "%10.7f", $laenge ),' ';
   #print sprintf( "%10.7f", $breite ),' ';
   #print sprintf( "%-5s", $plz ),' ';
   #print "$ort, $strasse $hausnummer\n";

   # Ausgabe als HTML-Tabelle
   print OUTFILE "<tr>";
   print OUTFILE "<td>$way_id</td>";
   print OUTFILE "<td>$node_id</td>";
   print OUTFILE "<td>$plz</td>";
   print OUTFILE "<td>$ort</td>";
   print OUTFILE "<td>$strasse</td>";
   print OUTFILE "<td>$hausnummer</td>";
   print OUTFILE "<td>$laenge</td>";
   print OUTFILE "<td>$breite</td>";
   print OUTFILE "</tr>\n";
}
$sth->finish();
print OUTFILE "</table>\n";

# HTML Ende
print OUTFILE "</body>\n";
print OUTFILE "</html>\n";

}

#---------------------------------------------------------------------------------------------------------------------
# HTML Kopf mit Javascript
#---------------------------------------------------------------------------------------------------------------------
sub print_html_header {

print OUTFILE <<HTML_CODE

<!DOCTYPE html>
<html>
<head>
<title>Karte OSM Adressen</title>
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
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />
<link rel="stylesheet" href="https://unpkg.com/leaflet\@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
<script src="https://unpkg.com/leaflet\@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>
</head>
<body>

<h2>Karte OpenStreetMap Adressen ($min_lon $min_lat) ($max_lon $max_lat)</h2>

<p>
<div id="mapid" style="width: 1200px; height: 800px;"></div>
</p>

<script>

// Karte mit angegebener Boundingbox initialisieren
var mymap = L.map('mapid').fitBounds( CP_map_boundingbox, {padding: [0,0], maxZoom: 19} );

// Tile-Server initialisieren
var CP_tile_server = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';  // OpenStreetMap's Standard tile layer
//var CP_tile_server = 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png';  // Wikimedia Maps
L.tileLayer( CP_tile_server, {
   maxZoom: 19,
   attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(mymap);

HTML_CODE

}
