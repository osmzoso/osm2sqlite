# Tools

Contains scripts to convert csv to gpx and vice versa.

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

