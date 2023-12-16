# 4. Map Drawing

See **./src_py/map.py**

For map drawing R*Tree index **"rtree_way"** and a table **map_def** with
map definitions (colors etc.) is required in the database.  

Example to generate a map with zoomlevel 16 and size 900 x 600px:  
```
sqlite3 ../freiburg.db < map_def.sql
./map.py ../freiburg.db 7.800 47.979 16 900 600 > map_zoom16.svg
```

## Map projection

See **./src_py/proj.py**

In order to draw a map, the coordinates of a spherical surface must
be mapped onto a plane surface.  
The Mercator projection is often used for this.  
To convert WGS84 coordinates, the simplified Web Mercator projection is usually used.

WGS84 (lon, lat) vs. Web Mercator (x, y):  

```
                                 ^
               lat:  85.05112888 | y:  20037508.34
                                 |
x: -20037508.34                  |                 x: 20037508.34
---------------------------------0------------------------------->
lon: -180°                       |                 lon: +180°
                                 |
               lat: -85.05112888 | y: -20037508.34
```

WGS84 (EPSG:4326), used in OpenStreetMap  
(see https://en.wikipedia.org/wiki/World_Geodetic_System#WGS_84)
    
Web Mercator (EPSG:3857)  
(see https://en.wikipedia.org/wiki/Web_Mercator_projection)

In principle, the Mercator projection cannot be used to display
coordinates near the poles.  
Polar areas with abs(latitude) bigger then 85.05112888 (85°3'4.064") are clipped off.

The conversion of Web Mercator coordinates into pixel coordinates is relatively simple.

Several pixel sizes of a square world map have been defined for this purpose:  
```
zoomlevel   size_world_map_in_pixel     meter_per_pixel
    0              256 x 256               156543.03      
    1              512 x 512                78271.52      
    2             1024 x 1024               39135.76      
    3             2048 x 2048               19567.88      
    4             4096 x 4096               9783.94       
    5             8192 x 8192               4891.97       
    6            16384 x 16384              2445.98       
    7            32768 x 32768              1222.99       
    8            65536 x 65536               611.50       
    9           131072 x 131072              305.75       
   10           262144 x 262144              152.87       
   11           524288 x 524288              76.44        
   12          1048576 x 1048576             38.22        
   13          2097152 x 2097152             19.11        
   14          4194304 x 4194304              9.55        
   15          8388608 x 8388608              4.78        
   16         16777216 x 16777216             2.39        
   17         33554432 x 33554432             1.19        
   18         67108864 x 67108864             0.60        
   19        134217728 x 134217728            0.30        
```

# Drawing the map

The map will be drawn in layers. Layer 1 is drawn first:

Layer 1: grassland, farmland  
Layer 2: forest, orchard, wineyard, parks   
Layer 3: sports field, playground  
Layer 4: water  
Layer 5: building, Swimming-Pools  
Layer 6: For two-colour roads lower part  
Layer 7: For two-colour roads upper part  
Layer 8: Superordinate roads (Bundesstr. Autobahn)  
Layer 9: Bridges, Trees, POI  
Layer 10: Powerline  
Layer 99: Unknown Ways (red)  

TODO  Don't print points outside the boundingbox  

