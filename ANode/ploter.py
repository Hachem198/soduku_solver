import matplotlib.pyplot as plt

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
