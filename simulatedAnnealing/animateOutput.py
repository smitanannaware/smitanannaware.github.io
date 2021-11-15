# __author:Smita Nannaware
# data:11/12/2021

import time
from copy import deepcopy

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.table import Table

N = 8
curr_state = None
path_indexes = None
Q = 'Q'
d = '-'
fig, ax = plt.subplots()
ax.set_axis_off()
width, height = 1.0 / N, 1.0 / N
tb = None


def checkerboard_table(data, bkg_colors=['grey', 'white']):
    global tb
    tb = Table(ax, bbox=[0, 0, 1, 1])
    # Add cells
    for (i, j), val in np.ndenumerate(data):
        # Index either the first or second item of bkg_colors based on
        # a checker board pattern
        idx = [j % 2, (j + 1) % 2][i % 2]
        color = bkg_colors[idx]

        tb.add_cell(i, j, width, height, text=val,
                    loc='center', facecolor=color)

    ax.add_table(tb)


def animate(i):
    global curr_state, path_indexes
    if len(path_indexes) > 0:
        move = path_indexes.pop(0)
        tb.get_celld()[move[0]].get_text().set_text(d)
        tb.get_celld()[move[1]].get_text().set_text(Q)
        ax.plot()


def play_animation(current_pos, path, num):
    global curr_state, path_indexes, N
    N = num
    curr_state = current_pos
    path_indexes = deepcopy(path)
    checkerboard_table(current_pos)
    frames = len(path)
    ani = matplotlib.animation.FuncAnimation(fig, animate,
                                             frames=frames, interval=.05)
    plt.show()
