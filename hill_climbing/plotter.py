import matplotlib.pyplot as plt

def plot_conflicts(conflict_history, output_file='hill_climbing_conflicts.png'):

    plt.figure(figsize=(10, 5))
    plt.plot(conflict_history, marker='o', linestyle='-', color='blue', label='Conflicts')
    plt.title('Conflict Reduction Over Iterations (Hill Climbing)')
    plt.xlabel('Iteration')
    plt.ylabel('Number of Conflicts')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()


