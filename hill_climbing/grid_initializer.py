import copy
import random

def fill_grid_initial(initial_grid):

    grid = copy.deepcopy(initial_grid)
    for row in range(9):
        existing = set(grid[row])
        missing = list(set(range(1, 10)) - existing)
        random.shuffle(missing)
        idx = 0
        for col in range(9):
            if grid[row][col] == 0:
                grid[row][col] = missing[idx]
                idx += 1
    return grid
