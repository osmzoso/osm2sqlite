# Tools

Directory **./tools** contains some tools.

`0_create_my_db.sh` Demo Workflow  
`check_addr_street_name.py` checks if the addr:street name is identical with the street name.  
`check_multipolygon.py` checks if multipolygon is closed  
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

