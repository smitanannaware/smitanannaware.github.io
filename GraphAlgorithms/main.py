import os
import random
import sys

import SCC_algorithm
import dijkstra_algorithm
import prims_algorithm
from graph import Graph


# Build the graph based on given edges
def build_graph(is_directed, edges):
    graph = Graph()
    for edge in edges:
        edge_detail = edge.split(' ')
        graph.add_vertex(edge_detail[0], edge_detail[1], edge_detail[-1])
        if not is_directed:
            graph.add_vertex(edge_detail[1], edge_detail[0], edge_detail[-1])
    return graph


def get_correct_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# This method takes the appropriate input from user and runs the selected algorithm
def main():
    edges = []
    source = ""

    problem_type = int(input("Please enter the problem : \n" +
                             "1. Single Source Shortest Path \n" +
                             "2. Minimum Spanning Tree \n" +
                             "3. Finding Strongly Connected Components \n"))

    file_name = input("Please enter the input file name (e.g. input.txt) :\n")
    try:
        is_directed = False
        with open(file_name) as f:
            lines = f.readlines()
            if lines[0].rstrip('\n').split(' ')[-1] == 'D':
                is_directed = True
            for line_index in range(1, len(lines)):
                if line_index == len(lines) - 1 and len(lines[-1]) == 1:
                    source = lines[-1]
                else:
                    edges.append(lines[line_index].rstrip('\n'))

        graph = build_graph(is_directed, edges)
        for v in graph.V:
            print(v, " connected to ", graph.V[v].adjacent)

        if not source:
            vertices = graph.V.keys()
            source = random.choice(list(graph.V.keys()))

        if problem_type == 1:
            print("Source vertex : ", source)
            dijkstra_algorithm.dijkstra(graph=graph, source=source)
        elif problem_type == 2:
            print("Source vertex : ", source)
            prims_algorithm.prims(graph=graph, source=source)
        elif problem_type == 3:
            SCC_algorithm.find_SCC(graph)
        else:
            print("Incorrect input. Try again!!")
    except FileNotFoundError:
        print("Oops! That was incorrect file name. Try again!!")

    k = input("Press a key to exit")

main()
