#!/usr/bin/python3 -tt
# Author: Toshio Kuratomi
# Copyright: (C) 2019, Toshio Kuratomi
# License: GPLv3+

"""
This is Conway's Game of Life.

It's just a toy.

But writing code is fun.

And therefore I did.
"""

# Improvements to make:
# * GUI setup
# * GUI output
# * Load and save patterns from a file
#
# Note: This is only if I'm interested ;-)

import curses
import functools
import time
import tracemalloc


#
# Load coordinates
#

# (0, 0)  in upper left hand corner
GOSPER = ((1, 5),
          (1, 6),
          (2, 5),
          (2, 6),
          (11, 5),
          (11, 6),
          (11, 7),
          (12, 4),
          (12, 8),
          (13, 3),
          (13, 9),
          (14, 3),
          (14, 9),
          (15, 6),
          (16, 4),
          (16, 8),
          (17, 5),
          (17, 6),
          (17, 7),
          (18, 6),
          (21, 3),
          (21, 4),
          (21, 5),
          (22, 3),
          (22, 4),
          (22, 5),
          (23, 2),
          (23, 6),
          (25, 1),
          (25, 2),
          (25, 6),
          (25, 7),
          (35, 3),
          (35, 4),
          (36, 3),
          (36, 4),
         )


#
# Initialize data structures
#

def initialize_data(board_size, initial_dataset):
    max_x, max_y = board_size

    board = set()
    for x, y in initial_dataset:
        if x > max_x:
            raise ValueError(f'dataset contains points ({x}, {y}) greater than the screen\'s'
                             f' x-axis ({max_x}, {max_y})')
        if y > max_y:
            raise ValueError(f'dataset contains points ({x}, {y}) greater than the screen\'s'
                             f' y-axis ({max_x}, {max_y})')

        board.add((x, y))

    return board


#
# Display data
#

def display_board(screen, board):
    screen.clear()
    for x, y in board:
        screen.addstr(y, x, ' ', curses.A_REVERSE)
    screen.refresh()


#
# Checks on the board
#

@functools.lru_cache()
def find_neighbors(cell, max_x, max_y):
    x, y = cell
    neighbors = set()

    for x_idx in range(x - 1, x + 2):
        if (x_idx < 0) or (x_idx > max_x - 1):
            continue

        for y_idx in range(y - 1, y + 2):
            if (y_idx < 0) or (y_idx > max_y - 1):
                continue

            if (x_idx, y_idx) != cell:
                neighbors.add((x_idx, y_idx))

    return neighbors


def check_will_live(cell, board, max_x, max_y):
    neighbors = find_neighbors(cell, max_x, max_y)

    if len([n for n in neighbors if n in board]) in (2, 3):
        return True

    return False


def check_new_life(center, board, checked_cells, max_x, max_y):
    x, y = center
    fertile_areas = set()

    for neighbor in find_neighbors(center, max_x, max_y):
        if neighbor not in checked_cells and neighbor not in board:
            fertile_areas.add(neighbor)

    babies = set()
    barren = set()
    for cell in fertile_areas:
        neighbors = find_neighbors(cell, max_x, max_y)

        if len([n for n in neighbors if n in board]) == 3:
            babies.add(cell)
        else:
            barren.add(cell)

    return babies, barren


def main(stdscr):

    curses.curs_set(0)
    stdscr.nodelay(True)

    max_y, max_x = stdscr.getmaxyx()
    board = initialize_data((max_x, max_y), GOSPER)

    #
    # cycle data
    #
    while True:
        display_board(stdscr, board)
        time.sleep(0.1)
        checked_cells = set()
        next_board = set()

        for cell in board:
            if check_will_live(cell, board, max_x, max_y):
                next_board.add(cell)
            checked_cells.add(cell)

            babies, barren = check_new_life(cell, board, checked_cells, max_x, max_y)
            checked_cells.update(babies)
            checked_cells.update(barren)

            next_board.update(babies)

        board = next_board

        keypress = stdscr.getch()
        # TODO: If "S" or "s" is pressed, then save
        if keypress != -1:
            # Currently any key press means exit
            break


if __name__ == '__main__':
    tracemalloc.start()
    initial_snap = tracemalloc.take_snapshot()

    curses.wrapper(main)

    end_snap = tracemalloc.take_snapshot()
    top_stats = end_snap.compare_to(initial_snap, 'lineno')

    for stat in top_stats[:20]:
        print(stat)
