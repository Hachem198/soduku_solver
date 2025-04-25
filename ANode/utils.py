def print_grid(grid):
    for row in grid:
        print(' '.join(map(str, row)))

def is_valid(grid, row, col, num):
    if num in grid[row]:
        return False
    for r in range(9):
        if grid[r][col] == num:
            return False
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def total_conflicts(grid):
    conflicts = 0
    empty_cells = 0
    for row in grid:
        counts = {}
        for num in row:
            if num == 0:
                empty_cells += 1
            else:
                counts[num] = counts.get(num, 0) + 1
        conflicts += sum(v - 1 for v in counts.values() if v > 1)

    for col in range(9):
        counts = {}
        for row in range(9):
            num = grid[row][col]
            if num == 0:
                continue
            counts[num] = counts.get(num, 0) + 1
        conflicts += sum(v - 1 for v in counts.values() if v > 1)

    for subgrid_row in range(3):
        for subgrid_col in range(3):
            counts = {}
            for i in range(3):
                for j in range(3):
                    num = grid[subgrid_row*3 + i][subgrid_col*3 + j]
                    if num == 0:
                        continue
                    counts[num] = counts.get(num, 0) + 1
            conflicts += sum(v - 1 for v in counts.values() if v > 1)

    return conflicts + empty_cells * 10
