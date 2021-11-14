# Colors to perform DFS
WHITE = "White"
GRAY = "Gray"
BLACK = "Black"


# This class stores all the information related to a vertex
class Vertex:
    def __init__(self, v=None):
        self.v = v
        self.color = WHITE
        self.time = 0
        self.parent = None
        self.distance = None
        self.adjacent = {}


# This graph defines the graph and add information to the vertices
class Graph:
    def __init__(self, V={}):
        self.V = V

    def add_vertex(self, u, v, weight):
        if u in self.V:
            self.V[u].adjacent[v] = weight
        else:
            vertex = Vertex(u)
            vertex.adjacent[v] = weight
            self.V[u] = vertex
        if v not in self.V:
            self.V[v] = Vertex(v)
