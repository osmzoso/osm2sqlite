# Appendix


## Table size

Output from `sqlite3_analyzer freiburg-regbez-latest.db`:

```
/** Disk-Space Utilization Report For freiburg-regbez-latest.db

Page size in bytes................................ 65536     
...

*** Page counts for all tables and indices separately *************************

WAY_NODES......................................... 5940        17.8% 
NODES............................................. 5727        17.1% 
WAY_NODES__WAY_ID................................. 4339        13.0% 
WAY_NODES__NODE_ID................................ 4181        12.5% 
WAY_TAGS.......................................... 3313         9.9% 
WAY_TAGS__KEY..................................... 1894         5.7% 
WAY_TAGS__WAY_ID.................................. 1340         4.0% 
RTREE_WAY_NODE.................................... 1156         3.5% 
NODE_TAGS......................................... 1103         3.3% 
NODE_TAGS__KEY.................................... 604          1.8% 
RELATION_MEMBERS.................................. 480          1.4% 
RTREE_WAY_ROWID................................... 472          1.4% 
NODE_TAGS__NODE_ID................................ 469          1.4% 
GRAPH............................................. 374          1.1% 
ADDR_HOUSENUMBER.................................. 356          1.1% 
RELATION_MEMBERS__TYPE............................ 320          0.96% 
RTREE_HIGHWAY_NODE................................ 287          0.86% 
RELATION_MEMBERS__RELATION_ID..................... 279          0.84% 
GRAPH__WAY_ID..................................... 180          0.54% 
RELATION_TAGS..................................... 152          0.46% 
RTREE_HIGHWAY_ROWID............................... 111          0.33% 
ADDR_HOUSENUMBER__STREET_ID....................... 102          0.31% 
RELATION_TAGS__KEY................................ 70           0.21% 
RELATION_TAGS__RELATION_ID........................ 51           0.15% 
ADDR_STREET....................................... 50           0.15% 
ADDR_STREET__POSTCODE_CITY_STREET................. 27           0.081% 
RTREE_WAY_PARENT.................................. 14           0.042% 
RTREE_HIGHWAY_PARENT.............................. 4            0.012% 
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

