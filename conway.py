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
# * Convert from a fixed array for the board size to only populating the live coordinates
# * GUI setup
# * GUI output
# * Load and save patterns from a file
#
# Note: This is only if I'm interested ;-)

import copy
import curses
import time


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
# Display data
#

def display_board(screen, board):
    screen.clear()
    for row_idx, row in enumerate(board):
        for cell_idx, cell in enumerate(row):
            if cell:
                screen.addstr(row_idx, cell_idx, ' ', curses.A_REVERSE)
    screen.refresh()


#
# Populate data structures
#

def populate_data(board_size, initial_dataset):
    max_x, max_y = board_size

    board = []
    for dummy in range(0, max_y):
        row = []
        for dummy in range(0, max_x):
            row.append(False)
        board.append(row)

    for x, y in initial_dataset:
        board[y][x] = True

    return board


#
# Checks on the board
#

def check_will_die(cell, board):
    x, y = cell
    neighbors = 0
    for x_idx in range(x - 1, x + 2):
        if (x_idx < 0) or (x_idx > len(board[0]) - 1):
            continue

        for y_idx in range(y - 1, y + 2):
            if (y_idx < 0) or (y_idx > len(board) - 1):
                continue

            if board[y_idx][x_idx] and (x_idx, y_idx) != cell:
                neighbors += 1

    if (neighbors < 2) or (neighbors > 3):
        return True

    return False


def check_new_life(center, board, checked_cells):
    x, y = center
    fertile_areas = set()

    for x_idx in range(x - 1, x + 2):
        if (x_idx < 0) or (x_idx > len(board[0]) - 1):
            continue

        for y_idx in range(y - 1, y + 2):
            if (y_idx < 0) or (y_idx > len(board) - 1):
                continue

            if (x_idx, y_idx) not in checked_cells and not board[y_idx][x_idx]:
                fertile_areas.add((x_idx, y_idx))

    babies = set()
    barren = set()
    for x, y in fertile_areas:
        neighbors = 0
        for x_idx in range(x - 1, x + 2):
            if (x_idx < 0) or (x_idx > len(board[0]) - 1):
                continue

            for y_idx in range(y - 1, y + 2):
                if (y_idx < 0) or (y_idx > len(board) - 1):
                    continue

                if board[y_idx][x_idx] and (x_idx, y_idx) != (x, y):
                    neighbors += 1

        if neighbors == 3:
            babies.add((x, y))
        else:
            barren.add((x, y))

    return babies, barren



def main(stdscr):

    curses.curs_set(0)
    stdscr.nodelay(True)

    max_y, max_x = stdscr.getmaxyx()
    board = populate_data((max_x, max_y), GOSPER)

    #
    # cycle data
    #
    while True:
        display_board(stdscr, board)
        time.sleep(0.1)
        checked_cells = set()
        next_board = copy.deepcopy(board)

        for row_idx, row in enumerate(board):
            for cell_idx, cell in enumerate(row):
                if cell:
                    if check_will_die((cell_idx, row_idx), board):
                        next_board[row_idx][cell_idx] = False
                    checked_cells.add((cell_idx, row_idx))

                    babies, barren = check_new_life((cell_idx, row_idx), board, checked_cells)
                    checked_cells.update(babies)
                    checked_cells.update(barren)

                    for x, y in babies:
                        next_board[y][x] = True
        board = next_board

        keypress = stdscr.getch()
        # TODO: If "S" or "s" is pressed, then save
        if keypress != -1:
            # Currently any key press means exit
            break


if __name__ == '__main__':
    curses.wrapper(main)
