from collections import defaultdict
from heapq import heappop, heappush
import os
from time import sleep
import math

# copied from https://github.com/simonbrahan/aoc2021/blob/master/15/dijkstra.py
# many thanks!!

def get_neighbours(cell, grid):
    x, y = cell
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    out = []
    for add_x, add_y in directions:
        neighbour_x = x + add_x
        neighbour_y = y + add_y

        if 0 <= neighbour_y < len(grid) and 0 <= neighbour_x < len(grid[neighbour_y]):
            out.append((neighbour_x, neighbour_y))

    return out


def get_risk(grid, DEBUG):
    destination = (len(grid) - 1, len(grid[0]) - 1)
    cumulative_cell_risks = defaultdict(lambda: math.inf)
    cumulative_cell_risks[(0, 0)] = 0
    cell_visit_queue = []
    heappush(cell_visit_queue, (0, (0, 0)))

    unvisited_cells = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            unvisited_cells.add((x, y))

    while destination in unvisited_cells:
        current_risk, current = heappop(cell_visit_queue)

        # heap is tricky to keep clean, so sometimes a visited cell will be added more than once.
        # No bother; just ignore it.
        if current not in unvisited_cells:
            continue

        neighbours = get_neighbours(current, grid)

        for neighbour in neighbours:
            if neighbour not in unvisited_cells:
                continue

            neighbour_risk = min(
                cumulative_cell_risks[neighbour],
                cumulative_cell_risks[current] + grid[neighbour[1]][neighbour[0]]
            )

            cumulative_cell_risks[neighbour] = neighbour_risk
            heappush(cell_visit_queue, (neighbour_risk, neighbour))

        unvisited_cells.remove(current)
        if DEBUG:
            print_grid(grid,unvisited_cells)
            sleep(0.000000025)

    return cumulative_cell_risks[destination]

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def print_grid(grid,unvisited_cells):
    s = ''
    print("\033[2F" * len(grid), end=None)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            a = str(cell)
            if (x,y) not in unvisited_cells:
                a = color.CYAN + a + color.END
            s += a
        s += "\n"
    print(s)