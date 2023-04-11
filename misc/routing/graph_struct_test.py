#
# Graph as an adjacency list for graphs with more than one edge between two nodes
#
# dict with lists
# graph = {
#  node_nr : [ [dest_node, edge_nr, dist], [dest_node, edge_nr, dist], ... ],
#  node_nr : [ [dest_node, edge_nr, dist], [dest_node, edge_nr, dist], ... ],
#  ...
# }

nodes = []
graph = {}

#
# Fill the dict graph{} with a simple test graph
# All edges are undirected
# edge_nr(dist)
#
#        +-+    2(7)   +-+
#        |2|-----------|3|
#        +-+           +-+
#        / \           / \
#       /   \         /   \
#  1(4)/     \7(2)   /     \3(12)
#     /       \     /8(1)   \
#    /         \   /         \
#  +-+   9(5)   +-+          +-+
#  |1|----------|7|          |4|
#  +-+          +-+          +-+
#    \         /   \         /
#     \       /     \11(8)  /
# 6(10)\     /10(4)  \     /4(4)
#       \   /         \   /
#        \ /           \ /
#        +-+           +-+
#        |6|-----------|5|
#        +-+   5(3)    +-+
#
def init_test_graph():
    global nodes, graph
    nodes = [1,2,3,4,5,6,7]
    graph[1] = [ [2,1,4], [7,9,5], [6,6,10] ]
    graph[2] = [ [1,1,4], [7,7,2], [3,2,7] ]
    graph[3] = [ [2,2,7], [7,8,1], [4,3,12] ]
    graph[4] = [ [3,3,12], [5,4,4] ]
    graph[5] = [ [4,4,4], [7,11,8], [6,5,3] ]
    graph[6] = [ [1,6,10], [7,10,4], [5,5,3] ]
    graph[7] = [ [1,9,5], [2,7,2], [3,8,1], [5,11,8], [6,10,4] ]
    print(graph)

def print_edges(node_nr):
    global graph
    print(f'Edges node {node_nr}:')
    for edge in graph[node_nr]:
        #print('dest_node:', edge[0],
        #      'edge_nr:  ', edge[1],
        #      'dist:     ', edge[2])
        print(f'dest_node:{edge[0]:4d}  edge_nr:{edge[1]:4d}  dist:{edge[2]:4d} ')
    print('-----------------')

#
#
#
init_test_graph()
for node in nodes:
    print_edges(node)

