from solver import hill_climbing_solve
from utils import print_grid
from plotter import plot_conflicts
import time

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

start_time = time.time()
solved_grid, iterations, conflict_history = hill_climbing_solve(initial_grid)
execution_time = time.time() - start_time

print(f"Solved in {iterations} iterations")
print(f"Final conflicts: {conflict_history[-1]}")
print(f"Execution time: {execution_time:.4f} seconds")
print("Solution grid:")
print_grid(solved_grid)

plot_conflicts(conflict_history)
