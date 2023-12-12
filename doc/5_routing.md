# 5. Routing

The table **graph** is required for the calculation of shortest paths.

Visualization of the table 'graph':  
![table_graph.jpg](table_graph.jpg)

The command
```
./src_py/route.py DATABASE LON_START LAT_START LON_DEST LAT_DEST
```
calculates the shortest path and outputs the result
as a csv list (lon,lat,ele) on stdout.

Visualization of a routing path:  
![routing_path.jpg](routing_path.jpg)

