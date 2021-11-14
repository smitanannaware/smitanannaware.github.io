import heapq
import math
from graph import Graph, Vertex

'''
Pseudocode:
INITIALIZE-SINGLE-SOURCE(G, s)
    for each vertex v from G.V                    --- O(n)
        v.d = infinity
        v.parent = NIL
    s.d = 0

RELAX(u,v,w)                                      --- O(log n)
    if v.d > u.d + w(u, v)
        v.d = u.d + w(u, v)
        v.parent = u

DIJKSTRA(G, w, s)
    INITIALIZE-SINGLE-SOURCE(G, s)
    S = NULL
    priority Q = G.V                              --- O(n log n)
    while Q not empty
        u = EXTRACT_MIN(Q)                        --- O(log n)
        S.add(u)
        for each vertex v in G.Adj[u]             --- O(m)
            RELAX(u,v,w)

'''


# Initializing all the vertex details
def init_single_source(graph, source=None):
    for vertex in graph.V:
        graph.V[vertex].distance = float('inf')
    if source:
        graph.V[source].distance = 0


# Find the distance of the neighbour and the neighbour vertex to heap
def relax(graph: Graph, vertex, adj, queue):
    dist = graph.V[vertex].distance + int(graph.V[vertex].adjacent[adj])
    if graph.V[adj].distance > dist:
        graph.V[adj].distance = dist
        graph.V[adj].parent = graph.V[vertex]
        heapq.heappush(queue, (dist, graph.V[adj].v))


# Print the tree path from leaf node
def print_path(v: Vertex):
    if v.parent is None:
        return v.v
    else:
        return print_path(v.parent) + '->' + v.v


# Find the shortest path from given source vertex
def dijkstra(graph: Graph, source):
    init_single_source(graph=graph, source=source)
    cloud = []

    queue = [(graph.V[source].distance, graph.V[source].v)]

    while len(queue) > 0:
        # Get the minimum distance vertex from heap
        dist, vertex = heapq.heappop(queue)
        if vertex not in cloud:
            # Add the vertex with minimum distance to cloud
            cloud.append(vertex)
            # Process the neighbours
            for adj in graph.V[vertex].adjacent:
                if adj not in cloud:
                    relax(graph, vertex, adj, queue)

    # Calculate tree cost and shortest tree path
    cloud.reverse()
    tree_path = ""
    tree_cost = 0
    print("Tree path: ")
    for vertex in cloud:
        node = graph.V[vertex]
        tree_cost += node.distance
        if vertex not in tree_path:
            tree_path = tree_path + "," + print_path(node)
            print(print_path(graph.V[vertex]))

    print("Tree Cost is : ", tree_cost)
