# __author:Smita Nannaware
# data:11/12/2021

from decimal import *
import math
import random
import time
from copy import deepcopy
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from animateOutput import play_animation

d = '-'
Q = 'Q'
N = 8


def get_output(array, row, column, f=None):
    try:
        for i in range(row):
            print("\n", file=f)
            for j in range(column):
                print(array[i][j], end=" ", file=f)
        print("\n", file=f)
    except Exception as e:
        print("Error occurred while getting output ", str(e))


def calculate_no_of_attacks(boardPos, i, j):
    num_of_attacks = 0
    k = 1
    j += k
    while j < N:
        if boardPos[i][j] == Q:
            num_of_attacks += 1
        if i + k < N and boardPos[i + k][j] == Q:
            num_of_attacks += 1
        if i - k > -1 and boardPos[i - k][j] == Q:
            num_of_attacks += 1
        k += 1
        j += 1
    return num_of_attacks


def get_position(array, value, column):
    y = -1
    x = -1
    for i in range(N):
        # find the index of value in array
        if array[i][column] == Q:
            x = i
            y = column
            break
    return x, y


def calculate_heuristic(boardPos):
    heuristic_val = 0
    for j in range(N):
        for i in range(N):
            if boardPos[i][j] == Q:
                heuristic_val += (calculate_no_of_attacks(boardPos, i, j))
    return heuristic_val


def gen_children(boardPos):
    h_table = [[0] * N for i in range(N)]
    for j in range(N):
        x, y = get_position(boardPos, Q, j)
        for i in range(N):
            if x == i and y == j:
                h_table[i][j] = float('inf')
            else:
                children = deepcopy(boardPos)
                children[i][j], children[x][y] = children[x][y], children[i][j]
                h_table[i][j] = calculate_heuristic(children)
    return h_table


def get_board():
    # create an board without queens
    board = []
    for i in range(0, N):
        board.append(['-'] * N)
    return board


def get_queens_on_board(board):
    # place queen randomly
    for i in range(0, N):
        board[i][i] = Q
    return board


def print_board(board=[]):
    for row in board:
        print(' '.join(row), end='\n')


def perform_simulated_annealing(current_pos, current_heuristic):
    temperature = 1500000000
    cooling_sch = 0.60
    trials = 150000

    success = False
    path_index = []
    start_time = time.time()
    if current_heuristic == 0:
        print("Solved already")
    else:
        while temperature:
            print("Temperature : ", temperature)
            # print("current State heuristic :", current_heuristic)
            h_table = gen_children(current_pos)
            children, child_heuristic = get_random_successor(current_pos, h_table, path_index)

            if child_heuristic > current_heuristic:
                diff = child_heuristic - current_heuristic
                pdf = float(float(math.e) ** float(float(-diff) / float(temperature)))
                print("Probability : ", pdf)
                if pdf > random.uniform(0, 1):
                    current_pos = children
                    current_heuristic = child_heuristic
                else:
                    path_index.pop()
            else:
                current_pos = children
                current_heuristic = child_heuristic
                if child_heuristic == 0:
                    print_board(current_pos)
                    print("Success")
                    success = True
                    break
            temperature = temperature * cooling_sch
        if success:
            print("Found solution!!")
        else:
            print("Solution not found!!")
        print("Time taken : ", time.time() - start_time)

    return path_index


def get_random_successor(current_pos, h_table, path_index):
    i, j = 0, 0
    for r in range(10):
        i = randint(0, N - 1)
        j = randint(0, N - 1)
        if h_table[i][j] != float('inf'):
            break

    child_heuristic = h_table[i][j]
    x, y = get_position(current_pos, Q, j)
    children = deepcopy(current_pos)
    children[i][j], children[x][y] = children[x][y], children[i][j]
    path_index.append([(x, y), (i, j)])
    return children, child_heuristic


def main():
    global N
    N = int(input("Please enter the number of queens : "))
    board = get_board()
    init_pos = get_queens_on_board(board)
    current_pos = deepcopy(init_pos)
    print_board(current_pos)

    current_heuristic = calculate_heuristic(current_pos)
    path = perform_simulated_annealing(current_pos, current_heuristic)
    play_animation(init_pos, path, N)


main()
