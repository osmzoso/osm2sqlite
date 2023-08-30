#!/usr/bin/env python
#
# Routing
#
import sys
import sqlite3
import math
import queue

if len(sys.argv) != 6:
    print(f'''
    Calculate shortest way.
    Usage:
    {sys.argv[0]} DATABASE LON_START LAT_START LON_DEST LAT_DEST
    ''')
    sys.exit(1)

database = sys.argv[1]

# Coordinates start and destination
lon_start = float(sys.argv[2])
lat_start = float(sys.argv[3])
lon_dest = float(sys.argv[4])
lat_dest = float(sys.argv[5])

# database connection
db_connect = sqlite3.connect(database)
db = db_connect.cursor()   # new database cursor


class Graph:
    """
    A class used to represent a graph

    - The numbers of the nodes must be between 1 and N
    - There can be multiple edges between two nodes.
      Therefore, each edge must have a unique number.
    - For the priority queue the heap queue algorithm from the Python standard library is used.
    """
    def __init__(self, number_of_nodes):
        """Initialize the class attributes:
          adjacency_list  : contains the data of the graph (dict with sets)
          number_of_nodes : number of nodes in the graph (int)
          number_of_edges : number of edges in the graph (int)
        Attributes for the Dijkstra algorithm:
          infinite        : largest positive integer supported by the platform
          sum_distance    : sum distance for each node (list)
          previous_node   : shortest way tree nodes (list)
          previous_edge   : shortest way tree edges (list)
        """
        # fill adjacency list, insert empty set for each node
        self.adjacency_list = {node: set() for node in range(1, number_of_nodes+1)}
        self.number_of_nodes = number_of_nodes
        self.number_of_edges = 0
        # attributes used by the Dijkstra algorithm
        self.infinite = sys.maxsize
        self.sum_distance = []
        self.previous_node = []
        self.previous_edge = []

    def add_edge(self, node_start, node_end, edge_id=-1, weight=1, directed=False):
        """Add an edge to the graph"""
        self.number_of_edges = self.number_of_edges + 1
        self.adjacency_list[node_start].add((node_end, edge_id, weight))
        if not directed:
            self.adjacency_list[node_end].add((node_start, edge_id, weight))

    def print_graph(self):
        """Print a formatted list of the graph"""
        for key in self.adjacency_list.keys():
            self.print_node_edges(key)

    def print_node_edges(self, node):
        """Print the edges of node formatted"""
        print(f'node {node} : edges to')
        for (node, edge_id, weight) in self.adjacency_list[node]:
            print(f' -> node:{node:15d}  edge_id:{edge_id:15d}  weight:{weight:15d} ')

    def dijkstra(self, node_start, node_end=-1):
        """Dijkstra Algorithm
        Calculates a shortest way tree for node_start
        Aborts prematurely when node_end is reached"""
        # initialize start values
        self.sum_distance = [self.infinite] * (self.number_of_nodes + 1)
        self.previous_node = [0] * (self.number_of_nodes + 1)
        self.previous_edge = [0] * (self.number_of_nodes + 1)
        self.priority_queue = queue.PriorityQueue()  # nodes to be examined
        # add start node to the list of nodes to be examined
        self.sum_distance[node_start] = 0
        self.priority_queue.put((0, node_start))
        while not self.priority_queue.empty():
            # search for the node with the shortest current distance in the list of nodes to be examined
            # and remove this node from the list
            current_distance, current_min_node = self.priority_queue.get()
            # if the just removed node is equal to the end node then the algorithm can be aborted prematurely
            if current_min_node == node_end:
                break
            # check all neighbours of the removed node
            for (reached_node, edge_id, edge_weight) in self.adjacency_list[current_min_node]:
                # if the node reached has not yet been examined then add it to the list
                if self.sum_distance[reached_node] == self.infinite:
                    self.priority_queue.put((self.sum_distance[current_min_node]+edge_weight, reached_node))
                # if the distance to the node with this edge is shorter then save the shorter distance and this edge.
                if self.sum_distance[current_min_node] + edge_weight < self.sum_distance[reached_node]:
                    self.sum_distance[reached_node] = self.sum_distance[current_min_node] + edge_weight
                    self.previous_node[reached_node] = current_min_node
                    self.previous_edge[reached_node] = edge_id

    def shortest_way(self, node_start, node_end):
        """Calculate shortest way between node_start and node_end
        Returns node_sequence (list), edge_sequence (list), sum_distance (int)"""
        self.dijkstra(node_start, node_end)
        node_sequence, edge_sequence = self.get_sequences(node_end)
        return node_sequence, edge_sequence, self.sum_distance[node_end]

    def get_sequences(self, node_end):
        """Determine the order of the nodes and edges from the shortest way tree"""
        node_sequence = []
        part_node = node_end
        while self.previous_node[part_node] != 0:
            node_sequence.append(part_node)
            part_node = self.previous_node[part_node]
        node_sequence.append(part_node)
        node_sequence.reverse()
        #
        edge_sequence = []
        for node in node_sequence:
            edge_sequence.append(self.previous_edge[node])
        edge_sequence.pop(0)  # remove first element
        return node_sequence, edge_sequence


def create_subgraph_tables(lon1, lat1, lon2, lat2):
    """Creates temp. tables that contain a subgraph
    described by a boundingbox.
    """
    db.execute('DROP TABLE IF EXISTS subgraph')
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
    ''', (lon1, lon2, lat1, lat2))
    db.execute('DROP TABLE IF EXISTS subgraph_nodes')
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
    #
    db.execute('SELECT max(no) FROM subgraph_nodes')
    (number_of_nodes,) = db.fetchone()
    return number_of_nodes


def boundingbox_subgraph(lon1, lat1, lon2, lat2, enlarge=1.2):
    """Calculate a boundingbox for the subgraph that is big enough to get a shortest way.
    In addition, a factor for enlargement must be specified.
    """
    if lon2 < lon1:
        lon1, lon2 = lon2, lon1
    if lat2 < lat1:
        lat1, lat2 = lat2, lat1
    mp_lon = (lon1 + lon2) / 2
    mp_lat = (lat1 + lat2) / 2
    diff_mp_lon = mp_lon - lon1
    diff_mp_lat = mp_lat - lat1
    if diff_mp_lat > diff_mp_lon:
        diff = diff_mp_lat * enlarge
    else:
        diff = diff_mp_lon * enlarge
    lon1 = mp_lon - diff
    lat1 = mp_lat - diff
    lon2 = mp_lon + diff
    lat2 = mp_lat + diff
    return lon1, lat1, lon2, lat2


def part_way_coordinates(way_id, node_start, node_end):
    """Returns a list with the coordinates of a part way"""
    #
    db.execute("SELECT node_order FROM way_nodes WHERE way_id=? AND node_id=?", (way_id, node_start))
    (node_start_order,) = db.fetchone()
    db.execute("SELECT node_order FROM way_nodes WHERE way_id=? AND node_id=?", (way_id, node_end))
    (node_end_order,) = db.fetchone()
    #
    query = '''
    SELECT wn.way_id,wn.node_id,wn.node_order,n.lon,n.lat
    FROM way_nodes AS wn
    LEFT JOIN nodes AS n ON wn.node_id=n.node_id
    WHERE wn.way_id=? AND wn.node_order>=? AND wn.node_order<=?
    ORDER BY wn.node_order '''
    if node_start_order > node_end_order:
        node_start_order, node_end_order = node_end_order, node_start_order
        query = query + 'DESC'
    coordinates = []
    db.execute(query, (way_id, node_start_order, node_end_order))
    for (way_id, node_id, node_order, lon, lat) in db.fetchall():
        coordinates.append((lon, lat))
    return coordinates


#
print('## start : ', lon_start, lat_start)
print('## dest  : ', lon_dest,  lat_dest)
#
# 1. Fill graph
#
lon1, lat1, lon2, lat2 = boundingbox_subgraph(lon_start, lat_start, lon_dest, lat_dest, 1.3)
print('## subgraph boundingbox', lon1, lat1, lon2, lat2)
number_of_nodes = create_subgraph_tables(lon1, lat1, lon2, lat2)
#
graph = Graph(number_of_nodes)
#
db.execute('''
SELECT s.edge_id,sns.no,sne.no,s.dist,s.way_id
FROM subgraph AS s
LEFT JOIN subgraph_nodes AS sns ON s.edge_start=sns.node_id
LEFT JOIN subgraph_nodes AS sne ON s.edge_end=sne.node_id
''')
for (edge_id, node_start, node_end, dist, way_id) in db.fetchall():
    graph.add_edge(node_start, node_end, edge_id, dist)
print('## graph number_of_nodes : ', graph.number_of_nodes)
print('## graph number_of_edges : ', graph.number_of_edges)
#
# 2. Find the nodes in the graph that are closest to the coordinates of the start point and end point
#
dist_node_start = sys.maxsize
graph_node_start = -1
dist_node_end = sys.maxsize
graph_node_end = -1
db.execute('SELECT no,lon,lat FROM subgraph_nodes')
for (no, lon, lat) in db.fetchall():
    dist = math.sqrt((lon_start-lon)**2 + (lat_start-lat)**2)
    if dist < dist_node_start:
        graph_node_start = no
        dist_node_start = dist
    dist = math.sqrt((lon_dest-lon)**2 + (lat_dest-lat)**2)
    if dist < dist_node_end:
        graph_node_end = no
        dist_node_end = dist
#
# 3. Routing
#
node_sequence, edge_sequence, distance = graph.shortest_way(graph_node_start, graph_node_end)
#
# 4. Output the coordinates of the path
#
print('## distance : ', distance, 'm')
# a) simple method, only start and end coordinates of the edge
# for graph_node in node_sequence:
#    db.execute('SELECT node_id,lon,lat FROM subgraph_nodes WHERE no=?', (graph_node,))
#    (node_id, lon, lat) = db.fetchone()
#    print(lon, lat)
# b) more sophisticated, all coordinates of the edge
path_coordinates = []
# get first Node
db.execute('SELECT node_id,lon,lat FROM subgraph_nodes WHERE no=?', (node_sequence[0],))
(first_node_id, lon, lat) = db.fetchone()
path_coordinates.append((lon, lat))
#
for edge_id in edge_sequence:
    db.execute('SELECT edge_start,edge_end,way_id FROM graph WHERE edge_id=?', (edge_id,))
    (edge_start, edge_end, way_id) = db.fetchone()
    if first_node_id == edge_start:
        coordinates = part_way_coordinates(way_id, edge_start, edge_end)
        first_node_id = edge_end
    else:
        coordinates = part_way_coordinates(way_id, edge_end, edge_start)
        first_node_id = edge_start
    coordinates.pop(0)  # remove the first coordinates
    path_coordinates.extend(coordinates)
for lon, lat in path_coordinates:
    print(lon, lat)
