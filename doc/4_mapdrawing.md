# 4. Map Drawing

See **./src_py/map.py**.

For map drawing R*Tree index **"rtree_way"** and  
a table **map_def** is required in the database.  
This table contains definitions for some zoomlevels.  

```
Creates a simple map in SVG format on stdout.
Usage:
./src_py/map.py DATABASE LON LAT ZOOMLEVEL SIZE_X SIZE_Y
```

Example to generate a map with zoomlevel 16 and size 900 x 600px:  
```
sqlite3 ../freiburg.db < map_def.sql
./map.py ../freiburg.db 7.800 47.979 16 900 600 > map_zoom16.svg
```

TODOs:  
1. The map will be drawn in layers. Layer 1 is drawn first:  
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
Layer 11: Unknown Ways (red)  
2. Don't print points outside the boundingbox  


## Map projection Web Mercator (EPSG:3857)

See `proj.py`

```
Help on module map_proj:

NAME
    map_proj - Contains functions for converting coordinates

DESCRIPTION
    1. Coordinate reference systems
    
    WGS84 (lon, lat)    - used in OpenStreetMap
    (see https://en.wikipedia.org/wiki/World_Geodetic_System#WGS_84)
    
    Web Mercator (x, y) - Spherical projection
    (see https://en.wikipedia.org/wiki/Web_Mercator_projection)
    
    Pixel coordinates   - Bitmap coordinates
    
    
    2. Restrictions Web Mercator
    
    Polar areas with abs(latitude) bigger then 85.05112878 (85°3'4.064") are clipped off.
    
    
    3. WGS84 vs. Web Mercator
    
                                     ^
                   lat:  85.05112878 | y:  20037508.34
                                     |
    x: -20037508.34                  |                 x: 20037508.34
    ---------------------------------0------------------------------->
    lon: -180°                       |                 lon: +180°
                                     |
                   lat: -85.05112878 | y: -20037508.34

FUNCTIONS
    degree_decimal_to_minutes(degrees_decimal)
        Return degrees, minutes, seconds of degrees decimal
    
    degree_minutes_to_decimal(degrees, minutes, seconds)
        Return decimal degrees of degrees minutes seconds
    
    pixel_boundingbox(lon, lat, pixel_world_map, size_x_px, size_y_px)
        Calculate pixel boundingbox
        size_x_px, size_y_px: map size in pixel
        Return min_x_px, min_y_px, max_x_px, max_y_px
    
    pixel_to_webmercator(x_px, y_px, pixel_world_map)
        Transform pixel coordinates to  Web Mercator
        Returns x, y
    
    pixel_to_wgs84(x_px, y_px, pixel_world_map)
        Transform pixel coordinates to WGS84
        Returns lon, lat
    
    size_world_map(zoomlevel)
        Calculates the size of the world map for a zoom level
        Return pixel_world_map, meters_pixel
        (resolution (meters/pixel) measured at Equator)"
    
    webmercator_to_pixel(x, y, pixel_world_map)
        Transform Web Mercator to pixel coordinates
        Returns x_px, y_px
    
    webmercator_to_wgs84(x, y)
        Return WGS84 (EPSG:4326) of Web Mercator (EPSG:3857)
    
    wgs84_to_pixel(lon, lat, pixel_world_map)
        Transform WGS84 to pixel coordinates
        Returns x_px, y_px
    
    wgs84_to_webmercator(lon, lat)
        Return Web Mercator (EPSG:3857) of WGS84 (EPSG:4326)

FILE
    /osm2sqlite/mapdrawing/map_proj.py
```

