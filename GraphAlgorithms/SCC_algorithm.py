# Strongly Connected components
from copy import deepcopy

from graph import *

order_of_visit = []


# Explore the vertex neighbors. Once explored all edges fully mark it as visited
def DFS_VISIT(graph, vertex):
    vertex.color = GRAY
    for adjV in vertex.adjacent:
        if graph.V[adjV].color == WHITE:
            graph.V[adjV].parent = vertex
            DFS_VISIT(graph, graph.V[adjV])
    vertex.color = BLACK
    order_of_visit.append(vertex.v)
    # return vertex.v


# Initialize the vertices and perform DFS_VISIT for all vertices if they not explored
def DFS(graph, reverse):
    for vertex in graph.V:
        graph.V[vertex].color = WHITE
        graph.V[vertex].parent = None

    if reverse:
        global order_of_visit
        order = deepcopy(order_of_visit)
        order.reverse()
        order_of_visit = []
        for vertex in order:
            if graph.V[vertex].color == WHITE:
                DFS_VISIT(graph, graph.V[vertex])
                # Print strongly connected components
                scc = ""
                for i in order_of_visit:
                    scc = scc + i + " "
                print(scc)
                order_of_visit = []

    else:
        for vertex in graph.V:
            if graph.V[vertex].color == WHITE:
                DFS_VISIT(graph, graph.V[vertex])


# Create transposed graph by reversing the edges of the graph
def transpose_graph(graph):
    graph_t = Graph({})
    for vertex in graph.V:
        vertex_obj = graph.V[vertex]
        for adj in vertex_obj.adjacent:
            graph_t.add_vertex(adj, vertex_obj.v, vertex_obj.adjacent[adj])
    return graph_t


# Find strongly connected components
def find_SCC(graph):
    DFS(graph, False)
    graph_t = transpose_graph(graph)
    print("Strongly connected components are: ")
    DFS(graph_t, True)
