# Appendix


## Table size

Output from `sqlite3_analyzer freiburg-regbez-latest.db`:

```
/** Disk-Space Utilization Report For freiburg-regbez-latest.db

Page size in bytes................................ 65536     
...

*** Page counts for all tables and indices separately *************************

WAY_NODES......................................... 6024        17.7% 
NODES............................................. 5798        17.1% 
WAY_NODES__WAY_ID................................. 4400        12.9% 
WAY_NODES__NODE_ID................................ 4243        12.5% 
WAY_TAGS.......................................... 3367         9.9% 
WAY_TAGS__KEY..................................... 1926         5.7% 
WAY_TAGS__WAY_ID.................................. 1363         4.0% 
RTREE_WAY_NODE.................................... 1171         3.4% 
NODE_TAGS......................................... 1135         3.3% 
NODE_TAGS__KEY.................................... 622          1.8% 
RELATION_MEMBERS.................................. 487          1.4% 
NODE_TAGS__NODE_ID................................ 483          1.4% 
RTREE_WAY_ROWID................................... 475          1.4% 
RTREE_NODE_NODE................................... 402          1.2% 
GRAPH............................................. 379          1.1% 
ADDR_HOUSENUMBER.................................. 357          1.1% 
RELATION_MEMBERS__RELATION_ID..................... 283          0.83% 
RELATION_MEMBERS__REF_ID.......................... 246          0.72% 
GRAPH__WAY_ID..................................... 182          0.54% 
RTREE_NODE_ROWID.................................. 161          0.47% 
RELATION_TAGS..................................... 157          0.46% 
ADDR_HOUSENUMBER__STREET_ID....................... 102          0.30% 
RELATION_TAGS__KEY................................ 73           0.21% 
RELATION_TAGS__RELATION_ID........................ 53           0.16% 
ADDR_STREET....................................... 50           0.15% 
ADDR_STREET__POSTCODE_CITY_STREET................. 27           0.079% 
RTREE_WAY_PARENT.................................. 13           0.038% 
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

## Links

<https://de.wikipedia.org/wiki/GPS_Exchange_Format>  
<https://www.gpsbabel.org/htmldoc-development/The_Formats.html>  
<https://www.gpsbabel.org/htmldoc-development/fmt_gpx.html>  
<https://www.topografix.com/gpx.asp>  
<https://www.j-berkemeier.de/ShowGPX.html>  

Problem Namespaces...

<https://gis.stackexchange.com/questions/228966/how-to-properly-get-coordinates-from-gpx-file-in-python>  
<https://stackoverflow.com/questions/14853243/parsing-xml-with-namespace-in-python-via-elementtree>  
<https://docs.python.org/3/library/xml.etree.elementtree.html#parsing-xml-with-namespaces>  
<https://mygeodata.cloud/converter/>  

