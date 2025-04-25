from collections import Counter

def calculate_column_conflicts(grid, col):

    column = [grid[row][col] for row in range(9)]
    counts = Counter(column)
    return sum(v - 1 for v in counts.values() if v > 1)

def calculate_subgrid_conflicts(grid, subgrid_row, subgrid_col):
 
    start_row, start_col = 3 * subgrid_row, 3 * subgrid_col
    subgrid = [grid[i][j] for i in range(start_row, start_row + 3)
                             for j in range(start_col, start_col + 3)]
    counts = Counter(subgrid)
    return sum(v - 1 for v in counts.values() if v > 1)

def total_conflicts(grid):

    conflicts = 0
    for col in range(9):
        conflicts += calculate_column_conflicts(grid, col)
    for subgrid_row in range(3):
        for subgrid_col in range(3):
            conflicts += calculate_subgrid_conflicts(grid, subgrid_row, subgrid_col)
    return conflicts
