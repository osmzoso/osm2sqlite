# Print a simple map

The python script *print_map.py* read data directly from the database
and print a very simple map in a window.

The library tkinter is used for drawing.

The script is only a test to investigate how fast the data can be accessed.

The map is drawn in layers. Layer 1 is drawn first.

Layer 1: grassland, farmland  
Layer 2: forest, orchard, wineyard, parks  
Layer 3: sports field, playground  
Layer 4: water  
Layer 5: building, Swimming-Pools  
Layer 6: Bei zweifarbigen Strassen unterer Teil  
Layer 7: Bei zweifarbigen Strassen oberer Teil  
Layer 8: Hochwertige Strassen (Bundesstr. Autobahn)  
Layer 9: Brücken, Bäume, POI  
Layer 10: Stromleitungen  
Layer 11: Unbekannte Ways (rot)  


## TODO

- map projection (Web Mercator EPSG:3857)
- define the colors in a table

