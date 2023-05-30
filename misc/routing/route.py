#!/usr/bin/env python
#
# Routing
#
import sys, sqlite3, math

if len(sys.argv)!=6:
    print('''
    Route shortest way.
    Usage:
    route.py DATABASE LON_START LAT_START LON_DEST LAT_DEST
    ''')
    sys.exit(1)

database = sys.argv[1]

# Koordinaten Start und Ziel
lon_start  = float(sys.argv[2])
lat_start  = float(sys.argv[3])
lon_dest   = float(sys.argv[4])
lat_dest   = float(sys.argv[5])

# database connection
db_connect = sqlite3.connect(database)
db = db_connect.cursor()   # new database cursor

#
# Graph as an adjacency list for graphs with more than one edge between two nodes
#
# Restrictions:
# The numbers of the nodes must be between 1 and N.
#
# https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/representing-graphs-in-code/
#
class Graph:
    def __init__(self, number_of_nodes):
        # insert empty set for each node
        self.adjacency_list = {node: set() for node in range(1, number_of_nodes+1)}
        self.number_of_nodes = number_of_nodes
        self.number_of_edges = 0
        #
        self.d = []      # sum distance
        self.v = []      # Shortest way tree (array contains previous node)
        self.b = []      # unvisited_nodes

    def add_edge(self, node_start, node_end, edge_id=-1, weight=1, directed=False):
        self.number_of_edges = self.number_of_edges + 1
        self.adjacency_list[node_start].add((node_end, edge_id, weight))
        if not directed:
            self.adjacency_list[node_end].add((node_start, edge_id, weight))

    def print_graph(self):
        #print("adjacency_list :\n", self.adjacency_list)   # print raw dict
        for key in self.adjacency_list.keys():
            self.print_node_edges(key)

    def print_node_edges(self, node):
        print(f'node {node} : edges to')
        for (node, edge_id, weight) in self.adjacency_list[node]:
            print(f' -> node:{node:15d}  edge_id:{edge_id:15d}  weight:{weight:15d} ')

    def print_d_v(self):
        print()
        print('B:', self.b)
        print('D:', self.d)
        print('V:', self.v)

    def dijkstra(self, node_start, node_end, debug=False):
        self.infinite = sys.maxsize     # largest positive integer supported by the platform
        # initialize start values
        self.d = [self.infinite] * (self.number_of_nodes + 1)
        self.d[node_start] = 0
        self.v = [0] * (self.number_of_nodes + 1)
        self.b = []
        # mark start node as unvisited
        self.b.append(node_start)
        while len(self.b) > 0:
            if debug:
                self.print_d_v()
            # wähle i aus b[] mit d[i] minimal und entferne i aus b[]
            current_min_node = 0
            for node in self.b:
                if self.d[node] < self.d[current_min_node]:
                    current_min_node = node
            self.b.remove(current_min_node)
            # wenn Zielknoten erreicht dann vorzeitig abbrechen
            if current_min_node == node_end:
                break
            # alle Nachbarn j von i untersuchen
            for (reached_node, edge_id, edge_weight) in self.adjacency_list[current_min_node]:
                # mark if the node reached has not yet been examined
                if self.d[reached_node] == self.infinite:
                    self.b.append(reached_node)
                # Verkürze
                if self.d[current_min_node] + edge_weight < self.d[reached_node]:
                    self.d[reached_node] = self.d[current_min_node] + edge_weight
                    self.v[reached_node] = current_min_node
        if debug:
            self.print_d_v()
        # Knotenreihenfolge ermitteln
        part_node = node_end
        node_sequence = []
        while self.v[part_node] != 0:
            node_sequence.append(part_node)
            part_node = self.v[part_node]
        node_sequence.append(part_node)
        node_sequence.reverse()
        #
        return node_sequence, self.d[node_end]


#
# 1. Teilgraph erstellen
#
graph_min_lon = lon_start
graph_min_lat = lat_start
graph_max_lon = lon_dest
graph_max_lat = lat_dest
if lon_start > lon_dest:
    graph_min_lon = lon_dest
    graph_max_lon = lon_start
if lat_start > lat_dest:
    graph_min_lat = lat_dest
    graph_max_lat = lat_start
#
graph_min_lon = graph_min_lon - 0.05
graph_min_lat = graph_min_lat - 0.05
graph_max_lon = graph_max_lon + 0.05
graph_max_lat = graph_max_lat + 0.05
#
print('# graph boundingbox', graph_min_lon, graph_min_lat, graph_max_lon, graph_max_lat)
#db.execute('DROP TABLE IF EXISTS subgraph')
db.execute('''
CREATE TEMP TABLE subgraph AS
SELECT edge_id,edge_start,edge_end,dist,way_id
FROM graph
WHERE way_id IN (
 SELECT way_id
 FROM rtree_way
 WHERE max_lon>=? AND min_lon<=?
  AND  max_lat>=? AND min_lat<=?
)
''',
(graph_min_lon, graph_max_lon, graph_min_lat, graph_max_lat))
#db.execute('DROP TABLE IF EXISTS subgraph_nodes')
db.execute('''
CREATE TEMP TABLE subgraph_nodes (
 no      INTEGER PRIMARY KEY,
 node_id INTEGER,
 lon     REAL,
 lat     REAL
)
''')
db.execute('''
INSERT INTO subgraph_nodes (node_id, lon, lat)
SELECT s.node_id,n.lon,n.lat FROM
(
 SELECT edge_start AS node_id FROM subgraph
 UNION
 SELECT edge_end AS node_id FROM subgraph
) AS s
LEFT JOIN nodes AS n ON s.node_id=n.node_id
''')
db.execute('CREATE INDEX subgraph_nodes__node_id ON subgraph_nodes(node_id)')
#
db.execute('SELECT max(no) FROM subgraph_nodes')
(number_of_nodes,) = db.fetchone()
graph = Graph(number_of_nodes)
#
db.execute('''
SELECT s.edge_id,sns.no,sne.no,s.dist,s.way_id
FROM subgraph AS s
LEFT JOIN subgraph_nodes AS sns ON s.edge_start=sns.node_id
LEFT JOIN subgraph_nodes AS sne ON s.edge_end=sne.node_id
''')
for (edge_id,node_start,node_end,dist,way_id) in db.fetchall():
    graph.add_edge(node_start, node_end, edge_id, dist)
print('# graph number_of_nodes', graph.number_of_nodes)
print('# graph number_of_edges', graph.number_of_edges)
#
# 2. Knoten im Graph ermitteln die am nächsten zu den Koordinaten von Startpunkt und Endpunkt liegen
#
dist_node_start = sys.maxsize
graph_node_start = -1
dist_node_end = sys.maxsize
graph_node_end   = -1
db.execute('SELECT no,lon,lat FROM subgraph_nodes')
for (no,lon,lat) in db.fetchall():
    dist = math.sqrt( (lon_start-lon)**2 + (lat_start-lat)**2 )
    if dist < dist_node_start:
        graph_node_start = no
        dist_node_start = dist
    dist = math.sqrt( (lon_dest-lon)**2 + (lat_dest-lat)**2 )
    if dist < dist_node_end:
        graph_node_end = no
        dist_node_end = dist
#
# 3. Routing
#
node_sequence, distance = graph.dijkstra(graph_node_start, graph_node_end)
#
# 4. Ergebnis ausgeben
#
print('#')
print('# start : ', lon_start, lat_start, '-> graph node', graph_node_start)
print('# dest  : ', lon_dest,  lat_dest,  '-> graph node', graph_node_end)
print('#')
print('# distance : ', distance, 'm')
print('#')
for graph_node in node_sequence:
    db.execute('''
    SELECT node_id,lon,lat
    FROM subgraph_nodes
    WHERE no=?
    ''', (graph_node,))
    (node_id, lon, lat) = db.fetchone()
    print(lon, lat)

