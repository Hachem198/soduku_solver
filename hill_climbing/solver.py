import random
from .conflicts import calculate_column_conflicts, calculate_subgrid_conflicts, total_conflicts
from .grid_initializer import fill_grid_initial
import copy
import asyncio
import time

def hill_climbing_solve(initial_grid, max_iterations=1000):

    
    grid = fill_grid_initial(initial_grid)
    current_conflicts = total_conflicts(grid)
    iterations = 0
    conflict_history = [current_conflicts]

    while current_conflicts > 0 and iterations < max_iterations:
        best_delta = 0
        best_swap = None

        for row in range(9):
            non_fixed = [col for col in range(9) if initial_grid[row][col] == 0]
            for i in range(len(non_fixed)):
                for j in range(i + 1, len(non_fixed)):
                    col_a, col_b = non_fixed[i], non_fixed[j]

                    old = (calculate_column_conflicts(grid, col_a) +
                           calculate_column_conflicts(grid, col_b) +
                           calculate_subgrid_conflicts(grid, row // 3, col_a // 3) +
                           calculate_subgrid_conflicts(grid, row // 3, col_b // 3))

                    grid[row][col_a], grid[row][col_b] = grid[row][col_b], grid[row][col_a]

                    new = (calculate_column_conflicts(grid, col_a) +
                           calculate_column_conflicts(grid, col_b) +
                           calculate_subgrid_conflicts(grid, row // 3, col_a // 3) +
                           calculate_subgrid_conflicts(grid, row // 3, col_b // 3))

                    grid[row][col_a], grid[row][col_b] = grid[row][col_b], grid[row][col_a]  # Swap back

                    delta = new - old

                    if delta < best_delta:
                        best_delta = delta
                        best_swap = (row, col_a, col_b)

        if best_delta < 0:
            row, col_a, col_b = best_swap
            grid[row][col_a], grid[row][col_b] = grid[row][col_b], grid[row][col_a]
            current_conflicts += best_delta
        else:
            # Random restart escape
            rows = [r for r in range(9) if sum(1 for c in range(9) if initial_grid[r][c] == 0) >= 2]
            if not rows:
                break
            row = random.choice(rows)
            non_fixed = [c for c in range(9) if initial_grid[row][c] == 0]
            if len(non_fixed) >= 2:
                col_a, col_b = random.sample(non_fixed, 2)
                grid[row][col_a], grid[row][col_b] = grid[row][col_b], grid[row][col_a]
                current_conflicts = total_conflicts(grid)

        conflict_history.append(current_conflicts)
        iterations += 1

    return grid, iterations, conflict_history

async def hill_climbing_solve_stream(initial_grid, max_iterations=1000):
    start_time = time.time()
    grid = fill_grid_initial(initial_grid)
    current_conflicts = total_conflicts(grid)
    iterations = 0

    yield {
        "grid": copy.deepcopy(grid),
        "conflicts": current_conflicts,
        "iteration": iterations
    }

    while current_conflicts > 0 and iterations < max_iterations:
        best_delta = 0
        best_swap = None

        for row in range(9):
            non_fixed = [col for col in range(9) if initial_grid[row][col] == 0]
            for i in range(len(non_fixed)):
                for j in range(i + 1, len(non_fixed)):
                    col_a, col_b = non_fixed[i], non_fixed[j]

                    old = (calculate_column_conflicts(grid, col_a) +
                           calculate_column_conflicts(grid, col_b) +
                           calculate_subgrid_conflicts(grid, row // 3, col_a // 3) +
                           calculate_subgrid_conflicts(grid, row // 3, col_b // 3))

                    grid[row][col_a], grid[row][col_b] = grid[row][col_b], grid[row][col_a]

                    new = (calculate_column_conflicts(grid, col_a) +
                           calculate_column_conflicts(grid, col_b) +
                           calculate_subgrid_conflicts(grid, row // 3, col_a // 3) +
                           calculate_subgrid_conflicts(grid, row // 3, col_b // 3))

                    grid[row][col_a], grid[row][col_b] = grid[row][col_b], grid[row][col_a]  # Swap back

                    delta = new - old

                    if delta < best_delta:
                        best_delta = delta
                        best_swap = (row, col_a, col_b)

        if best_delta < 0:
            row, col_a, col_b = best_swap
            grid[row][col_a], grid[row][col_b] = grid[row][col_b], grid[row][col_a]
            current_conflicts += best_delta
        else:
            rows = [r for r in range(9) if sum(1 for c in range(9) if initial_grid[r][c] == 0) >= 2]
            if not rows:
                break
            row = random.choice(rows)
            non_fixed = [c for c in range(9) if initial_grid[row][c] == 0]
            if len(non_fixed) >= 2:
                col_a, col_b = random.sample(non_fixed, 2)
                grid[row][col_a], grid[row][col_b] = grid[row][col_b], grid[row][col_a]
                current_conflicts = total_conflicts(grid)

        iterations += 1
        yield {
            "grid": copy.deepcopy(grid),
            "conflicts": current_conflicts,
            "iteration": iterations,
            "algorithm": "hill_climbing",
            "time": time.time() - start_time
        }

        await asyncio.sleep(0.05)  # Add a small delay for UI visualization