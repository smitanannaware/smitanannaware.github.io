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
success = 0
success_time_taken = []
failure_time_taken = []


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
        board[randint(0, N - 1)][i] = 'Q'
    return board


def get_queens_on_board_diagonally(board):
    # place queen randomly
    for i in range(0, N):
        board[i][i] = Q
    return board


def print_board(board=[]):
    for row in board:
        print(' '.join(row), end='\n')


def perform_simulated_annealing(current_pos, current_heuristic, cooling_sch, case):
    global success

    temperature = 1500000000
    is_success = False
    path_index = []
    start_time = time.time()
    if current_heuristic == 0:
        print("Solved already")
    else:
        while temperature > 1e-200:
            if case == 2:
                print("Temperature : ", temperature)
            # print("current State heuristic :", current_heuristic)
            h_table = []
            children, child_heuristic = get_random_successor(current_pos, path_index, case)

            if child_heuristic > current_heuristic:
                diff = child_heuristic - current_heuristic
                pdf = float(float(math.e) ** float(float(-diff) / float(temperature)))
                if case == 2:
                    print("Probability : ", pdf)
                if pdf > random.uniform(0, 1):
                    current_pos = children
                    current_heuristic = child_heuristic
                elif case == 2:
                    path_index.pop()
            else:
                current_pos = children
                current_heuristic = child_heuristic
                if child_heuristic == 0:
                    print("Solution state:")
                    print_board(current_pos)
                    print("Success")
                    is_success = True
                    break
            temperature = temperature * cooling_sch
        if is_success:
            print("Found solution!!")
            success += 1
            success_time_taken.append(time.time() - start_time)
        else:
            print("Solution not found!!")
            failure_time_taken.append(time.time() - start_time)
        if case == 2:
            print("Time taken : ", time.time() - start_time)
    return path_index


def get_random_successor(current_pos, path_index, case):
    i, j = 0, 0
    for r in range(10):
        i = randint(0, N - 1)
        j = randint(0, N - 1)
        if current_pos[i][j] != Q:
            break

    x, y = get_position(current_pos, Q, j)
    children = deepcopy(current_pos)
    children[i][j], children[x][y] = children[x][y], children[i][j]
    child_heuristic = calculate_heuristic(children)
    if case == 2:
        path_index.append([(x, y), (i, j)])
    return children, child_heuristic


def main():
    global N
    print("N Queens problem by Simulated Annealing")
    N = int(input("Please enter the number of queens : \n"))
    place_diagonally = input("Do you want to place queens diagonally? If No, queens will be placed randomly. "
                             "Enter Y or N : \n")
    case = int(input("Select from the options below : \n"
                     "1. Run performance analysis based on cooling schedule\n"
                     "2. Visualize the simulated annealing\n"))

    if case == 2:
        board = get_board()
        if place_diagonally == 'Y':
            init_pos = get_queens_on_board_diagonally(board)
        else:
            init_pos = get_queens_on_board(board)
        current_pos = deepcopy(init_pos)
        print_board(current_pos)

        current_heuristic = calculate_heuristic(current_pos)
        path = perform_simulated_annealing(current_pos, current_heuristic, 0.60, case)
        play_animation(init_pos, path, N)
    elif case == 1:
        cooling_sch = float(input("Please enter the cooling schedule value between 0 to 1 : \n"))
        if 0 <= cooling_sch <= 1:
            run = int(input("Enter the number of executions\n"))
            for i in range(0, run):
                print("Run number : ", i)
                board = get_board()
                if place_diagonally == 'Y':
                    current_pos = get_queens_on_board_diagonally(board)
                else:
                    current_pos = get_queens_on_board(board)
                print_board(current_pos)
                current_heuristic = calculate_heuristic(current_pos)
                path = perform_simulated_annealing(current_pos, current_heuristic, cooling_sch, case)

            print("Total Run = {run}\n"
                  "\nAverage time taken for success = {avg1}"
                  "\nAverage time taken for failure = {avg2}"
                  .format(run=run,
                          avg1=(sum(success_time_taken) / len(success_time_taken))
                          if len(success_time_taken) > 0 else 0,
                          avg2=(sum(failure_time_taken) /
                                len(failure_time_taken)) if
                          len(failure_time_taken) > 0 else 0))
            success_rate = (success / run) * 100
            print("Success Rate = {sr} %".format(sr=success_rate))
            print("Failure Rate = {fr} %".format(fr=((run - success) / run) * 100))
            k = input("Please enter a key to exit")
        else:
            print("Please enter valid input!!")
    else:
        print("Please enter valid input!!")


main()
