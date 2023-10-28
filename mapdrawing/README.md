# Map Drawing

The Python script *draw_map_interactive.py* read data directly from the database
and draw a very simple map in a window.

The library tkinter is used for drawing.
Therefore no street names can be displayed.

The script is only a test to investigate how fast the data can be accessed.


## Map projection (Web Mercator EPSG:3857)

See `map_proj.py`

```
Help on module map_proj:

NAME
    map_proj - Contains functions for converting coordinates

DESCRIPTION
    1. Systems
    WGS84 (lon, lat)    - used in OpenStreetMap
    Web Mercator (x, y) - Spherical projection
    Pixel coordinates   - Bitmap coordinates
    
    
    2. Restrictions Web Mercator
    
    Polar areas with abs(latitude) bigger then 85.05112878 are clipped off.
    
    
    3. Compare WGS84 - Web Mercator
    
                                               ^       right upper corner:
                                               |       lon: +180°0'0" (E), lat: 85°3'4.064" (N)
                                               |       x: 20037508.34, y: 20037508.34
                                               |
    -------------------------------------------0------------------------------------------>
                                               |
    left down corner:                          |
    lon: -180°0'0" (W), lat: -85°3'4.064" (S)  |
    x: -20037508.34,  y: -20037508.34          |

FUNCTIONS
    degree_decimal_to_minutes(degrees_decimal)
        Return degrees, minutes, seconds of degrees decimal
    
    degree_minutes_to_decimal(degrees, minutes, seconds)
        Convert degrees minutes seconds to decimal degrees
    
    pixel_to_webmercator(x_px, y_px, pixel_world_map)
        Transform pixel coordinates to  Web Mercator
        Returns x, y
    
    pixel_to_wgs84(x_px, y_px, pixel_world_map)
        Transform pixel coordinates to WGS84
        Returns lon, lat
    
    webmercator_to_pixel(x, y, pixel_world_map)
        Transform Web Mercator to pixel coordinates
        Returns x_px, y_px
    
    webmercator_to_wgs84(x, y)
        Transform Web Mercator (EPSG:3857) to WGS84 (EPSG:4326)
        Returns lon, lat (decimal degrees)
    
    wgs84_to_pixel(lon, lat, pixel_world_map)
        Transform WGS84 to pixel coordinates
        Returns x_px, y_px
    
    wgs84_to_webmercator(lon, lat)
        Transform WGS84 (EPSG:4326) to Web Mercator (EPSG:3857)
        Returns x, y (meters)
    
    zoom_sizes(zoomlevel)
        Calculates sizes for given zoom level
        TODO
        meters_pixel : Resolution (meters/pixel) measured at Equator"

FILE
    /osm2sqlite/mapdrawing/map_proj.py

```


## Future goals..

- output SVG
- define the colors in a table

The map will be drawn in layers. Layer 1 is drawn first.

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

