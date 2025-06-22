# Drawing a map

For map drawing R\*Tree indexes (see option **rtree**) and table **map_def** with
map definitions (colors etc.) are required in the database.  

Creation of the **map_def** table: `sqlite3 ../freiburg.db < ./tools/map_def.sql`  

## map.py

Example to generate a map with zoomlevel 16 and size 900 x 600px:  
`./tools/map.py ../freiburg.db 7.800 47.979 16 900 600 map_zoom16.svg`  

Converting SVG to PNG with **inkscape**:  
`inkscape map_zoom16.svg -o map_zoom16.png`

## Map projection

In OSM, the coordinates are in [WGS84](https://en.wikipedia.org/wiki/World_Geodetic_System#WGS_84)
format to describe points on a spherical surface.  
This format is also described under the name [EPSG:4326](https://epsg.io/4326).  

In order to draw a map, the coordinates of a spherical surface must
be mapped onto a plane surface.  
The [Mercator projection](https://en.wikipedia.org/wiki/Mercator_projection) is usually used for this.  

In principle, the Mercator projection cannot be used to display
coordinates near the poles.  

Most often the simplified [Web Mercator projection](https://en.wikipedia.org/wiki/Web_Mercator_projection) is used.        
This format is also described under the name [EPSG:3857](https://epsg.io/3857).  
Polar areas with abs(latitude) bigger then 85.05112878 (85°3'4.0636") are clipped off.

Comparison of WGS84 (lon, lat) with Web Mercator (x, y):  
```
                                 ^
               lat:  85.05112878 | y:  20037508.343
                                 |
x: -20037508.343                 |                 x: 20037508.343
---------------------------------0--------------------------------->
lon: -180°                       |                 lon: +180°
                                 |
               lat: -85.05112878 | y: -20037508.343
```

As you can see, the WGS84 coordinates are transformed into a square world map.

The conversion of Web Mercator coordinates into pixel coordinates is relatively simple.

## Zoomlevel

Defined pixel sizes (zoomlevel) of a square world map:  
```
zoomlevel       pixel_world_map          meters_pixel
    0              256 x 256               156543.03
    1              512 x 512                78271.52
    2             1024 x 1024               39135.76
    3             2048 x 2048               19567.88
    4             4096 x 4096                9783.94
    5             8192 x 8192                4891.97
    6            16384 x 16384               2445.98
    7            32768 x 32768               1222.99
    8            65536 x 65536                611.50
    9           131072 x 131072               305.75
   10           262144 x 262144               152.87
   11           524288 x 524288                76.44
   12          1048576 x 1048576               38.22
   13          2097152 x 2097152               19.11
   14          4194304 x 4194304                9.55
   15          8388608 x 8388608                4.78
   16         16777216 x 16777216               2.39
   17         33554432 x 33554432               1.19
   18         67108864 x 67108864               0.60
   19        134217728 x 134217728              0.30
   20        268435456 x 268435456              0.15
```

## Drawing the map

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

## Multipolygon

To represent larger areas, several ways can be connected to one area
using a relation.  
If the area is open inside, this can be specified using inner ways.  
Inner ways are almost always just single ways.  

<https://wiki.openstreetmap.org/wiki/DE:Relation:multipolygon>  
<https://wiki.openstreetmap.org/wiki/Multipolygon_Examples>  
<https://wiki.openstreetmap.org/wiki/Relation:multipolygon/Algorithm>  
<https://postgis.net/docs/ST_MakePolygon.html>  

## POI

Examples:
```
tourism=gallery
shop=hairdresser
amenity=cafe
```

Display point of interest only in larger zoom level:  
Zoomlevel 17: show as a small dot  
Zommlevel 18,19: show as a symbol  

