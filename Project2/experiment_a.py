import time
import statistics
import matplotlib.pyplot as plt
from pathlib import Path
import csv

from graph_generation import generate_edges, to_adjacency_matrix
from Part_a import dijkstra

RESULTS_DIR = Path(__file__).resolve().parent / "graphs"
RESULTS_DIR.mkdir(exist_ok=True)

# Measure Dijkstra's execution time
def measure_runtime(graph, repeats=10):
    times = []

    for _ in range(repeats):
        start = time.perf_counter()

        dijkstra(graph, 0)

        end = time.perf_counter()

        times.append(end - start)

    return statistics.median(times)


# Experiment 1: Vary number of vertices
def experiment_vertices():
    vertex_sizes = [100, 200, 400, 800, 1600]
    results = []

    for V in vertex_sizes:
        E = 2 * V
        graph_times = []

        # Test 5 different random graphs
        for seed in range(5):
            edges = generate_edges(V, E, seed=seed)
            graph = to_adjacency_matrix(V, edges)

            runtime = measure_runtime(graph)
            graph_times.append(runtime)

        median_time = statistics.median(graph_times)
        results.append((V, median_time))

        print(f"V={V}, E={E}, Time={median_time:.6f}s")

    return results


# Experiment 2: Vary number of edges
def experiment_edges():
    V = 500
    edge_sizes = [500, 2000, 10000, 50000]
    results = []

    for E in edge_sizes:
        graph_times = []

        for seed in range(5):
            edges = generate_edges(V, E, seed=seed)
            graph = to_adjacency_matrix(V, edges)

            runtime = measure_runtime(graph)
            graph_times.append(runtime)

        median_time = statistics.median(graph_times)
        results.append((E, median_time))

        print(f"E={E}, V={V}, Time={median_time:.6f}s")

    return results


# Plot results
def plot_results(vertex_results, edge_results):

    # Experiment 1
    V_values = [r[0] for r in vertex_results]
    V_times = [r[1] for r in vertex_results]

    plt.figure()
    plt.plot(V_values, V_times, marker='o')
    plt.xlabel("Number of Vertices (V)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Dijkstra (Matrix + Array): Varying V")
    plt.grid(True)
    plt.savefig(RESULTS_DIR / "part_a_varying_V.png", dpi=300)
    

    # Experiment 2
    E_values = [r[0] for r in edge_results]
    E_times = [r[1] for r in edge_results]

    plt.figure()
    plt.plot(E_values, E_times, marker='o')
    plt.xlabel("Number of Edges (E)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Dijkstra (Matrix + Array): Varying E")
    plt.grid(True)
    plt.savefig(RESULTS_DIR / "part_a_varying_E.png", dpi=300)

def save_results(filename, results, headers):
    filepath = RESULTS_DIR / filename

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(results)

    print(f"Saved results to {filepath}")

if __name__ == "__main__":
    print("Experiment 1: Varying V")
    vertex_results = experiment_vertices()

    print("\nExperiment 2: Varying E")
    edge_results = experiment_edges()

    vertex_results = experiment_vertices()
    edge_results = experiment_edges()

    # Save numerical results
    save_results(
        "part_a_vertices.csv",
        vertex_results,
        ["Vertices (V)", "Median Runtime (s)"]
    )

    save_results(
        "part_a_edges.csv",
        edge_results,
        ["Edges (E)", "Median Runtime (s)"]
    )


    plot_results(vertex_results, edge_results)
