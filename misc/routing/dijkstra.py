#
#
#
import sys


#
# Dijkstra
#
nodes = []  #
graph = {}  # Contains the graph as an adjacency list
d = []      # sum distance
v = []      # Shortest way tree (array contains previous node)
b = []      # unvisited_nodes
def print_d_v():
    global b, d, v
    print()
    print('B:', b)
    print('D:', d)
    print('V:', v)

def dijkstra(start_node):
    global graph, d, v, b
    infinite = sys.maxsize
    # initialize start values
    d = [infinite] * (len(nodes) + 1)
    d[start_node] = 0
    v = [0] * (len(nodes) + 1)
    # mark start node as unvisited
    b.append(start_node)
    while len(b) > 0:
        # Debug
        print_d_v()
        # wähle i aus b[] mit d[i] minimal und entferne i aus b[]
        current_min_node = 0
        for node in b:
            if d[node] < d[current_min_node]:
                current_min_node = node
        b.remove(current_min_node)
        # alle Nachbarn j von i untersuchen
        for reached_node,edge_dist in graph[current_min_node].items():
            # mark if the node reached has not yet been examined
            if d[reached_node] == infinite:
                b.append(reached_node)
            # Verkürze
            if d[current_min_node] + edge_dist < d[reached_node]:
                d[reached_node] = d[current_min_node] + edge_dist
                v[reached_node] = current_min_node

#
# Fill the dict graph{} with a simple demo graph
#
#        +-+     7     +-+
#        |2|-----------|3|
#        +-+           +-+
#        / \           / \
#       /   \         /   \
#     4/     \2     1/     \12
#     /       \     /       \
#    /         \   /         \
#  +-+    5     +-+          +-+
#  |1|----------|7|          |4|
#  +-+          +-+          +-+
#    \         /   \         /
#     \       /     \       /
#    10\     /4     8\     /4
#       \   /         \   /
#        \ /           \ /
#        +-+           +-+
#        |6|-----------|5|
#        +-+     3     +-+
#
# All edges are undirected
#
def demo_graph():
    global nodes, graph
    #
    # Adjacency list of the graph
    #
    nodes = [1,2,3,4,5,6,7]
    for node in nodes:
        graph[node] = {}
    graph[1][2] = 4
    graph[1][7] = 5
    graph[1][6] = 10
    graph[2][1] = 4
    graph[2][7] = 2
    graph[2][3] = 7
    graph[3][2] = 7
    graph[3][7] = 1
    graph[3][4] = 12
    graph[4][3] = 12
    graph[4][5] = 4
    graph[5][4] = 4
    graph[5][7] = 8
    graph[5][6] = 3
    graph[6][5] = 3
    graph[6][7] = 4
    graph[6][1] = 10
    graph[7][1] = 5
    graph[7][2] = 2
    graph[7][3] = 1
    graph[7][5] = 8
    graph[7][6] = 4
    print(graph)

#
# Helper Print all edges of a node
#
def print_node_edges(node_nr):
    print('\nAll edges of node', node_nr)
    print(graph[node_nr])
    for dest_node,dist in graph[node_nr].items():
        print('dest_node:', dest_node, 'dist:', dist)





#
# Test the algorithm
#
demo_graph()
print_node_edges(1)
print_node_edges(7)
dijkstra(1)
print_d_v()

