# Map Drawing

The Python script *draw_map_interactive.py* read data directly from the database
and draw a very simple map in a window.

The library tkinter is used for drawing.
Therefore no street names can be displayed.

The script is only a test to investigate how fast the data can be accessed.

TODOs:

- map projection (Web Mercator EPSG:3857)
- define the colors in a table
- output SVG


# Notes

The map is drawn in layers. Layer 1 is drawn first.

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


# EPSG 3857

<https://gis.stackexchange.com/questions/120636/math-formula-for-transforming-from-epsg4326-to-epsg3857>

<https://matplotlib.org/basemap/users/merc.html>

