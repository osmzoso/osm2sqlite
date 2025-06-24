# Routing

## route.py

```
Calculates shortest route.

Usage:
./tools/route.py DATABASE LON_START LAT_START LON_DEST LAT_DEST PERMIT CSVFILE

PERMIT: 1 (foot), 2 (bike_gravel), 4 (bike_road) or 8 (car)
```

Table **graph** (see option **graph**) and R\*Tree **rtree_way** (see option **rtree**)  
are required for the calculation of shortest paths.

As an example, the command  
`./route.py freiburg.db 7.853 47.995 7.862 47.995 1 route.csv`  
calculates the shortest route for pedestrians and saves a list of
coordinates in the file *route.csv*.

The command  
`./tools/html_leaflet_csv.py route.csv route.html`  
creates an HTML file with an interactive map of the route.  
![routing_path.jpg](routing_path.jpg)  

The command  
`./tools/convert_csv2gpx.py route.csv route.gpx`  
converts the coordinate list in the CSV file into a GPX file.

