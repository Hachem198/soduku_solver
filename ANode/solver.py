import heapq
import copy
import time
import asyncio
from .utils import is_valid, find_empty_cell, total_conflicts
from .ploter import plot_conflicts

class AStarNode:
    def __init__(self, grid, g):
        self.grid = tuple(tuple(row) for row in grid)
        self.g = g
        self.h = total_conflicts(grid)
        self.f = self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

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






async def a_star_solve_stream(initial_grid):
    start_time = time.time()
    iterations = 0

    initial_node = AStarNode(initial_grid, 0)
    heap = []
    heapq.heappush(heap, initial_node)
    visited = set()

    while heap:
        current_node = heapq.heappop(heap)
        current_grid = [list(row) for row in current_node.grid]
        iterations += 1

        yield {
            "grid": copy.deepcopy(current_grid),
            "conflicts": current_node.h,
            "iteration": iterations,
            "algorithm": "A*",
            "time": time.time() - start_time,
        }

        await asyncio.sleep(0.05)  # Visualization pacing

        if current_node.h == 0 and find_empty_cell(current_grid) is None:
            return  # Found solution

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

    return  # No solution found