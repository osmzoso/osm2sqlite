# 1. osm2sqlite

A simple command line tool for reading
[OpenStreetMap XML data](https://wiki.openstreetmap.org/wiki/OSM_XML)
into a SQLite database.

Read simple XML file **country.osm** into database **test.db**:  
`osm2sqlite test.db read country.osm`  

OSM data can be obtained from a provider such as [Geofabrik](https://download.geofabrik.de).

## Read .osm.bz2 file

The OSM XML data is provided as bzip2 compressed data.

To avoid unpacking the bzip2 file, the tool can read from stdin.

Examples for reading .osm.bz2 files:  
`7z e -so ../germany.osm.bz2 | osm2sqlite germany.db read -`  
`bzip2 -c -d ../germany.osm.bz2 | osm2sqlite germany.db read -`  

> The .osm.bz2 format is [deprecated](https://download.geofabrik.de/bz2.html).  
> In future, only .osm.pbf files will be provided from Geofabrik.

## Read .osm.pbf file

The tool **osmium** can convert .osm.pbf files to .osm.

Example for reading an .osm.pbf file into a SQLite database:  
`osmium cat country.osm.pbf -f osm -o - | osm2sqlite country.db read -`  

Install osmium on Fedora Linux:  
`sudo dnf install osmium-tool`  

[Compiled osmium.exe for Windows (without warranty)](https://github.com/pango3001/Osmium_1_14)  

Convert .osm.pbf to osm, output to stdout:  
`osmium cat myfile.osm.pbf --output-format=osm --output=- | less -S`  
`osmium cat myfile.osm.pbf -f osm -o - | less -S`  

Convert .osm.pbf to .osm.bz2: `osmium cat myfile.osm.pbf -o myfile.osm.bz2`  

Convert .osm.pbf to .osm: `osmium cat myfile.osm.pbf -o myfile.osm`  

<https://osmcode.org/osmium-tool/>


# 2. Tables

The following tables and indexes are created in the database:

#### Table "nodes"
column       | type                | description
-------------|---------------------|-------------------------------------
node_id      | INTEGER PRIMARY KEY | node ID
lon          | REAL                | longitude
lat          | REAL                | latitude

#### Table "node_tags"
column       | type                | description
-------------|---------------------|-------------------------------------
node_id      | INTEGER             | node ID
key          | TEXT                | tag key
value        | TEXT                | tag value
- INDEX node_tags__node_id ON node_tags (node_id)
- INDEX node_tags__key     ON node_tags (key)

#### Table "way_nodes"
column       | type                | description
-------------|---------------------|-------------------------------------
way_id       | INTEGER             | way ID
node_id      | INTEGER             | node ID
node_order   | INTEGER             | node order
- INDEX way_nodes__way_id  ON way_nodes (way_id, node_order)
- INDEX way_nodes__node_id ON way_nodes (node_id)

#### Table "way_tags"
column       | type                | description
-------------|---------------------|-------------------------------------
way_id       | INTEGER             | way ID
key          | TEXT                | tag key
value        | TEXT                | tag value
- INDEX way_tags__way_id   ON way_tags (way_id)
- INDEX way_tags__key      ON way_tags (key)

#### Table "relation_members"
column       | type                | description
-------------|---------------------|-------------------------------------
relation_id  | INTEGER             | relation ID
ref          | TEXT                | reference ('node','way','relation')
ref_id       | INTEGER             | node, way or relation ID
role         | TEXT                | describes a particular feature
member_order | INTEGER             | member order
- INDEX relation_members__relation_id ON relation_members (relation_id, member_order)
- INDEX relation_members__ref_id      ON relation_members (ref_id)

#### Table "relation_tags"
column       | type                | description
-------------|---------------------|-------------------------------------
relation_id  | INTEGER             | relation ID
key          | TEXT                | tag key
value        | TEXT                | tag value
- INDEX relation_tags__relation_id    ON relation_tags (relation_id)
- INDEX relation_tags__key            ON relation_tags (key)

The database can be easily queried with the [SQLite CLI tool](https://www.sqlite.org/cli.html).


# 3. Options

There are several options for creating additional data in the database.

## Option "rtree"

This option creates additional [R*Tree](https://www.sqlite.org/rtree.html)
indexes **rtree_node** and **rtree_way** for finding ways quickly.  

Internally, the index **rtree_way** is created as follows:  
``` sql
CREATE VIRTUAL TABLE rtree_way USING rtree(way_id, min_lat, max_lat, min_lon, max_lon);

INSERT INTO rtree_way (way_id, min_lat, max_lat, min_lon, max_lon)
SELECT way_nodes.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)
FROM way_nodes
LEFT JOIN nodes ON way_nodes.node_id=nodes.node_id
GROUP BY way_nodes.way_id;
```

#### Example queries

``` sql
/*
** Find all elements of the index (ways) that are contained within the boundingbox:
**    min_lon (x1):  7.851, min_lat (y1): 47.995
**    max_lon (x2):  7.854, max_lat (y2): 47.996
*/
SELECT way_id
FROM rtree_way
WHERE min_lon>= 7.851 AND max_lon<= 7.854
 AND  min_lat>=47.995 AND max_lat<=47.996;
/*
** Find all elements of the index (ways) that overlap the boundingbox:
*/
SELECT way_id
FROM rtree_way
WHERE max_lon>= 7.851 AND min_lon<= 7.854
 AND  max_lat>=47.995 AND min_lat<=47.996;
/*
** Limits of an element of the index:
*/
SELECT min_lon,max_lon,min_lat,max_lat
FROM rtree_way
WHERE way_id=4872512;
```


## Option "addr"

This option creates two tables with address data.  

#### Table "addr_street"
column       | type                | description
-------------|---------------------|-------------------------------------
street_id    | INTEGER PRIMARY KEY | street ID
postcode     | TEXT                | postcode
city         | TEXT                | city
street       | TEXT                | street
min_lon      | REAL                | boundingbox min. longitude
min_lat      | REAL                | boundingbox min. latitude
max_lon      | REAL                | boundingbox max. longitude
max_lat      | REAL                | boundingbox max. latitude
- INDEX addr_street_1 ON addr_street (postcode,city,street)

#### Table "addr_housenumber"
column       | type                | description
-------------|---------------------|-------------------------------------
housenumber_id | INTEGER PRIMARY KEY | housenumber ID
street_id      | INTEGER             | street ID
housenumber    | TEXT                | housenumber
lon            | REAL                | longitude
lat            | REAL                | latitude
way_id         | INTEGER             | way ID
node_id        | INTEGER             | node ID
- INDEX addr_housenumber_1 ON addr_housenumber (street_id)

The view **addr_view** join the two tables.


## Option "graph"

This option creates an additional table **graph** with the complete graph
of all highways.  
This data is required for routing purposes, for example.  

#### Table "graph"
column          | type                | description
----------------|---------------------|-------------------------------------
edge_id         | INTEGER PRIMARY KEY | edge ID
start_node_id   | INTEGER             | edge start node ID
end_node_id     | INTEGER             | edge end node ID
dist            | INTEGER             | distance in meters
way_id          | INTEGER             | way ID
permit          | INTEGER             | bit field access

Visualization of the table 'graph':  
![table_graph.jpg](table_graph.jpg)

The bit field **permit** determines who may use this edge:  
Bit 0 : 2^0  1  foot  
Bit 1 : 2^1  2  bike_gravel  
Bit 2 : 2^2  4  bike_road  
Bit 3 : 2^3  8  car  
Bit 4 : 2^4 16  bike_oneway  
Bit 5 : 2^5 32  car_oneway  

> This field is currently not yet filled, but there is a script that
> fills this field, see **./tools/fill_graph_permit.py**.

Queries on how to determine a smaller subgraph from this table
can be found in **./queries/graph_subgraph.sql**.



# Appendix


## Test

For testing, the databases of the C and Python version are compared.

    ./test/run_test.sh

It has been found that the mantissa rarely differs by 1 bit.  
However, this should not be a problem for calculations.  

```
+-------------+-------+-----------------------------+---------------------+
|   node_id   |  db   |    format('%!.50f',lon)     |    binary64_lon     |
+-------------+-------+-----------------------------+---------------------+
| 25724717    | db_c  | 8.8370532999999991119466358 | x'4021ac924009048b' |
| 25724717    | db_py | 8.8370533000000008883034752 | x'4021ac924009048c' |
| 25885946    | db_c  | 8.8214282999999991119466358 | x'4021a4924009048b' |
| 25885946    | db_py | 8.8214283000000008883034752 | x'4021a4924009048c' |
| 26652345    | db_c  | 8.8780443000000008879624147 | x'4021c18f05c1e0e1' |
| 26652345    | db_py | 8.8780442999999991116055753 | x'4021c18f05c1e0e0' |
| 31117904    | db_c  | 8.8619116000000008881443136 | x'4021b94c7a2c1609' |
| 31117904    | db_py | 8.8619115999999991117874742 | x'4021b94c7a2c1608' |
+-------------+-------+-----------------------------+---------------------+

+-------------+-------+-----------------------------+---------------------+
|   node_id   |  db   |    format('%!.50f',lat)     |    binary64_lat     |
+-------------+-------+-----------------------------+---------------------+
| 21316798    | db_c  | 53.076708000000003551122063 | x'404a89d19157abb9' |
| 21316798    | db_py | 53.076707999999996447429428 | x'404a89d19157abb8' |
| 21523098    | db_c  | 53.105010299999996447282979 | x'404a8d70fa3e1f1f' |
| 21523098    | db_py | 53.105010300000003555312422 | x'404a8d70fa3e1f20' |
| 25869795    | db_c  | 53.16163010000000355148586  | x'404a94b04b8cc64d' |
| 25869795    | db_py | 53.161630099999996447793226 | x'404a94b04b8cc64c' |
| 25869846    | db_c  | 53.025771400000003552577254 | x'404a834c7a2c1609' |
| 25869846    | db_py | 53.02577139999999644888462  | x'404a834c7a2c1608' |
+-------------+-------+-----------------------------+---------------------+
```


## Tools

Directory **./tools** contains some tools.

`0_create_my_db.sh` Demo Workflow  
`check_addr_street_name.py` checks if the addr:street name is identical with the street name.  
`convert_csv2gpx.py` Convert CSV to GPX  
`convert_gpx2csv.py` Convert GPX to CSV  
`map.py` Draw a simple map  
`fill_graph_permit.py` Fill field 'permit' in table 'graph'   
`html_leaflet_addr.py` Creates an HTML file with a map of all addresses in a specific area  
`html_leaflet_csv.py` Creates an HTML file with a map from a CSV file containing waypoints (lon,lat)  
`html_leaflet_demo.py` Shows the usage of html_leaflet.py  
`html_leaflet_gpx.py` Creates an HTML file with a map of all paths from the specified GPX files  
`html_leaflet_graph.py` Creates an HTML file with a map to display the data in the "graph" table  
`html_leaflet.py` Python modul for creating HTML files with
[Leaflet.js](https://leafletjs.com/reference.html).  
`info.py` Show OSM data on stdout  
`route.py` Find shortest way  


## Size of the tables in the database

Output from `sqlite3_analyzer freiburg-regbez-latest.db`:

```
/** Disk-Space Utilization Report For freiburg-regbez-latest.db

Page size in bytes................................ 65536     
Pages in the whole file (measured)................ 34355     
Pages in the whole file (calculated).............. 34355     
Pages that store data............................. 34354       99.997% 
Pages on the freelist (per header)................ 0            0.0% 
Pages on the freelist (calculated)................ 1            0.003% 
Pages of auto-vacuum overhead..................... 0            0.0% 
Number of tables in the database.................. 19        
Number of indices................................. 14        
Number of defined indices......................... 14        
Number of implied indices......................... 0         
Size of the file in bytes......................... 2251489280
Bytes of user payload stored...................... 975149184   43.3% 

*** Page counts for all tables with their indices *****************************

WAY_NODES......................................... 14755       42.9% 
WAY_TAGS.......................................... 6731        19.6% 
NODES............................................. 5832        17.0% 
NODE_TAGS......................................... 2307         6.7% 
RTREE_WAY_NODE.................................... 1178         3.4% 
RELATION_MEMBERS.................................. 1036         3.0% 
GRAPH............................................. 595          1.7% 
RTREE_WAY_ROWID................................... 479          1.4% 
ADDR_HOUSENUMBER.................................. 461          1.3% 
RTREE_NODE_NODE................................... 410          1.2% 
RELATION_TAGS..................................... 308          0.90% 
RTREE_NODE_ROWID.................................. 163          0.47% 
ADDR_STREET....................................... 77           0.22% 
RTREE_WAY_PARENT.................................. 14           0.041% 
RTREE_NODE_PARENT................................. 5            0.015% 
MAP_DEF........................................... 2            0.006% 
SQLITE_SCHEMA..................................... 1            0.003% 

*** Page counts for all tables and indices separately *************************

WAY_NODES......................................... 6060        17.6% 
NODES............................................. 5832        17.0% 
WAY_NODES__WAY_ID................................. 4426        12.9% 
WAY_NODES__NODE_ID................................ 4269        12.4% 
WAY_TAGS.......................................... 3404         9.9% 
WAY_TAGS__KEY..................................... 1948         5.7% 
WAY_TAGS__WAY_ID.................................. 1379         4.0% 
RTREE_WAY_NODE.................................... 1178         3.4% 
NODE_TAGS......................................... 1170         3.4% 
NODE_TAGS__KEY.................................... 641          1.9% 
RELATION_MEMBERS.................................. 497          1.4% 
NODE_TAGS__NODE_ID................................ 496          1.4% 
RTREE_WAY_ROWID................................... 479          1.4% 
GRAPH............................................. 411          1.2% 
RTREE_NODE_NODE................................... 410          1.2% 
ADDR_HOUSENUMBER.................................. 358          1.0% 
RELATION_MEMBERS__RELATION_ID..................... 288          0.84% 
RELATION_MEMBERS__REF_ID.......................... 251          0.73% 
GRAPH__WAY_ID..................................... 184          0.54% 
RELATION_TAGS..................................... 171          0.50% 
RTREE_NODE_ROWID.................................. 163          0.47% 
ADDR_HOUSENUMBER__STREET_ID....................... 103          0.30% 
RELATION_TAGS__KEY................................ 79           0.23% 
RELATION_TAGS__RELATION_ID........................ 58           0.17% 
ADDR_STREET....................................... 50           0.15% 
ADDR_STREET__POSTCODE_CITY_STREET................. 27           0.079% 
RTREE_WAY_PARENT.................................. 14           0.041% 
RTREE_NODE_PARENT................................. 5            0.015% 
MAP_DEF........................................... 1            0.003% 
MAP_DEF__KEY_VALUE................................ 1            0.003% 
SQLITE_SCHEMA..................................... 1            0.003% 
```

## GPX XML structure

```
0: gpx [creator, version, {http://www.w3.org/2001/XMLSchema-instance}schemaLocation]
    1: metadata [-]
        2: link [href]
            3: text [-]
        2: time [-]
        2: bounds [maxlat, maxlon, minlat, minlon]
    1: wpt [lat, lon]
        2: ele [-]
        2: name [-]
        2: cmt [-]
        2: desc [-]
        2: sym [-]
        2: extensions [-]
            3: gpxx:WaypointExtension [-]
                4: gpxx:DisplayMode [-]
        2: time [-]
    1: trk [-]
        2: name [-]
        2: extensions [-]
            3: gpxx:TrackExtension [-]
                4: gpxx:DisplayColor [-]
        2: trkseg [-]
            3: trkpt [lat, lon]
                4: ele [-]
                4: time [-]
```

<https://en.wikipedia.org/wiki/GPS_Exchange_Format>  
<https://www.j-berkemeier.de/ShowGPX.html>  
