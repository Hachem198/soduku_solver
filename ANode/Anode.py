import heapq
import copy
import time
import matplotlib.pyplot as plt

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

class AStarNode:
    def __init__(self, grid, g):
        self.grid = tuple(tuple(row) for row in grid)
        self.g = g
        self.h = total_conflicts(grid)
        self.f = self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

def plot_conflicts(conflict_history, output_file='a_star_conflicts.png'):
    plt.figure(figsize=(10, 5))
    plt.plot(conflict_history, marker='o', linestyle='-', color='blue', label='Conflicts (h)')
    plt.title('Conflict Reduction Over Iterations (A*)')
    plt.xlabel('Iteration')
    plt.ylabel('Heuristic Score (Conflicts + Empty Penalty)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()

def a_star_solve(initial_grid):
    start_time = time.time()
    iterations = 0
    conflict_history = []

    initial_node = AStarNode(initial_grid, 0)
    heap = []
    heapq.heappush(heap, initial_node)
    visited = set()

    while heap:
        current_node = heapq.heappop(heap)
        current_grid = [list(row) for row in current_node.grid]
        iterations += 1
        conflict_history.append(current_node.h)

        if current_node.h == 0 and find_empty_cell(current_grid) is None:
            end_time = time.time()
            print("\n--- Analysis ---")
            print(f"Iterations       : {iterations}")
            print(f"Execution time   : {end_time - start_time:.4f} seconds")
            print(f"Final score (f)  : {current_node.f}")
            print(f"Conflicts at end : {current_node.h}")
            plot_conflicts(conflict_history)
            return current_grid

        if current_node.grid in visited:
            continue
        visited.add(current_node.grid)

        empty_cell = find_empty_cell(current_grid)
        if not empty_cell:
            continue

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_grid, row, col, num):
                new_grid = copy.deepcopy(current_grid)
                new_grid[row][col] = num
                new_node = AStarNode(new_grid, current_node.g + 1)
                heapq.heappush(heap, new_node)

    end_time = time.time()
    print("\n--- Analysis ---")
    print(f"Iterations       : {iterations}")
    print(f"Execution time   : {end_time - start_time:.4f} seconds")
    plot_conflicts(conflict_history)
    print("No solution found.")
    return None

# Example usage
initial_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solved_grid = a_star_solve(initial_grid)

if solved_grid:
    print("\nSolution grid:")
    print_grid(solved_grid)
else:
    print("\nNo solution found.")
