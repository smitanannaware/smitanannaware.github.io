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
    if v.d > w(u, v)
        v.d = w(u, v)
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


# update the distance of the neighbour with min edge value from cloud and the neighbour vertex to heap
def relax(graph: Graph, vertex, adj, queue):
    dist = int(graph.V[vertex].adjacent[adj])
    if graph.V[adj].distance > dist:
        graph.V[adj].distance = dist
        graph.V[adj].parent = graph.V[vertex]
        heapq.heappush(queue, (dist, graph.V[adj].v))


# Find the minimum spanning tree from given source vertex
def prims(graph: Graph, source):
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

    # Calculate tree cost and minimum spanning tree path
    cloud.reverse()
    tree_path = ""
    tree_cost = 0
    print("Tree edges: ")
    for vertex in cloud:
        node = graph.V[vertex]
        tree_cost += node.distance
        if node.parent:
            print(node.parent.v, node.v, node.parent.adjacent[node.v])

    print("Tree Cost is : ", tree_cost)
