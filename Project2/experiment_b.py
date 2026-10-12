import time
import math
import statistics
import matplotlib.pyplot as plt
from pathlib import Path

from graph_generation import generate_edges, to_adjacency_list, to_adjacency_matrix
from Part_a import dijkstra
from Part_b import dijkstra_heap

RESULTS_DIR = Path(__file__).resolve().parent / "graphs"
RESULTS_DIR.mkdir(exist_ok=True)

# Check Part B gives the same distances as Part A before timing anything
def check_correctness():
    for seed in range(10):
        V = 200
        E = 1000
        edges = generate_edges(V, E, seed=seed)

        expected = dijkstra(to_adjacency_matrix(V, edges), 0)
        actual = dijkstra_heap(to_adjacency_list(V, edges), 0)

        assert expected == actual, f"Mismatch on seed {seed}"

    print("Correctness check passed: Part B matches Part A on 10 random graphs\n")


# Measure Dijkstra's execution time
def measure_runtime(graph, repeats=10):
    times = []

    for _ in range(repeats):
        start = time.perf_counter()

        dijkstra_heap(graph, 0)

        end = time.perf_counter()

        times.append(end - start)

    return statistics.median(times)


# Theoretical bound for the heap version: (V + E) log V
def theoretical(V, E):
    return (V + E) * math.log2(V)


# Experiment 1: Vary number of vertices (same sizes as Part A)
def experiment_vertices():
    vertex_sizes = [100, 200, 400, 800, 1600]
    results = []

    for V in vertex_sizes:
        E = 2 * V
        graph_times = []

        # Test 5 different random graphs
        for seed in range(5):
            edges = generate_edges(V, E, seed=seed)
            graph = to_adjacency_list(V, edges)

            runtime = measure_runtime(graph)
            graph_times.append(runtime)

        median_time = statistics.median(graph_times)
        results.append((V, E, median_time))

        print(f"V={V}, E={E}, Time={median_time:.6f}s, "
              f"Time/((V+E)logV)={median_time / theoretical(V, E):.3e}")

    return results


# Experiment 2: Vary number of edges (same sizes as Part A)
def experiment_edges():
    V = 500
    edge_sizes = [500, 2000, 10000, 50000]
    results = []

    for E in edge_sizes:
        graph_times = []

        for seed in range(5):
            edges = generate_edges(V, E, seed=seed)
            graph = to_adjacency_list(V, edges)

            runtime = measure_runtime(graph)
            graph_times.append(runtime)

        median_time = statistics.median(graph_times)
        results.append((V, E, median_time))

        print(f"E={E}, V={V}, Time={median_time:.6f}s, "
              f"Time/((V+E)logV)={median_time / theoretical(V, E):.3e}")

    return results


# Plot results
def plot_results(vertex_results, edge_results):

    # Experiment 1
    V_values = [r[0] for r in vertex_results]
    V_times = [r[2] for r in vertex_results]

    plt.figure()
    plt.plot(V_values, V_times, marker='o')
    plt.xlabel("Number of Vertices (V)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Dijkstra (Adj List + Min Heap): Varying V (E = 2V)")
    plt.grid(True)
    plt.savefig(RESULTS_DIR / "part_b_varying_V.png", dpi=300)

    # Experiment 2
    E_values = [r[1] for r in edge_results]
    E_times = [r[2] for r in edge_results]

    plt.figure()
    plt.plot(E_values, E_times, marker='o')
    plt.xlabel("Number of Edges (E)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Dijkstra (Adj List + Min Heap): Varying E (V = 500)")
    plt.grid(True)
    plt.savefig(RESULTS_DIR / "part_b_varying_E.png", dpi=300)

    # Empirical vs theoretical: if O((V+E) log V) holds, the points form a straight line
    all_results = vertex_results + edge_results
    x = [theoretical(V, E) for V, E, _ in all_results]
    y = [t for _, _, t in all_results]

    plt.figure()
    plt.scatter(x, y)
    plt.xlabel("(V + E) log2 V")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Dijkstra (Adj List + Min Heap): Time vs (V+E) log V")
    plt.grid(True)
    plt.savefig(RESULTS_DIR / "part_b_vs_theory.png", dpi=300)

if __name__ == "__main__":
    check_correctness()

    print("Experiment 1: Varying V")
    vertex_results = experiment_vertices()

    print("\nExperiment 2: Varying E")
    edge_results = experiment_edges()

    plot_results(vertex_results, edge_results)
