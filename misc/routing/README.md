# Routing

## Calculation of a simple graph for routing purposes

First, routable data must be created from the OSM data.

The testscript `calc_graph.py` creates a simple table with the graph data.

### Table 'graph'

column       | type                | description
-------------|---------------------|-------------------------------------
edge_id      | INTEGER PRIMARY KEY | edge ID
edge_start   | INTEGER             | edge start node ID
edge_end     | INTEGER             | edge end node ID
dist         | INTEGER             | distance in meters
way_id       | INTEGER             | way ID


Visualization of the table 'graph':  

![Table 'graph'](./table_graph.jpg)

