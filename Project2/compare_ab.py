import time
import statistics
import matplotlib.pyplot as plt
from pathlib import Path

from graph_generation import generate_edges, to_adjacency_matrix, to_adjacency_list
from Part_a import dijkstra
from Part_b import dijkstra_heap

RESULTS_DIR = Path(__file__).resolve().parent / "graphs"
RESULTS_DIR.mkdir(exist_ok=True)

# Median runtime of one Dijkstra function on one graph
def measure_runtime(func, graph, repeats=3):
    times = []

    for _ in range(repeats):
        start = time.perf_counter()
        func(graph, 0)
        end = time.perf_counter()
        times.append(end - start)

    return statistics.median(times)


# Time both versions on the same random graphs (median over 3 seeds)
def compare(V, E):
    a_times = []
    b_times = []

    for seed in range(3):
        edges = generate_edges(V, E, seed=seed)
        a_times.append(measure_runtime(dijkstra, to_adjacency_matrix(V, edges)))
        b_times.append(measure_runtime(dijkstra_heap, to_adjacency_list(V, edges)))

    return statistics.median(a_times), statistics.median(b_times)


# Sparse graphs: E = 2V, growing V
def compare_sparse():
    results = []

    for V in [100, 200, 400, 800, 1600]:
        a, b = compare(V, 2 * V)
        results.append((V, a, b))
        print(f"V={V}, E={2 * V}: Part A={a:.6f}s, Part B={b:.6f}s")

    return results


# Fixed V, growing density up to a complete graph
def compare_density():
    V = 500
    max_edges = V * (V - 1) // 2
    results = []

    for E in [500, 2000, 10000, 50000, 100000, max_edges]:
        a, b = compare(V, E)
        results.append((E, a, b))
        print(f"V={V}, E={E}: Part A={a:.6f}s, Part B={b:.6f}s")

    return results


def plot(results, xlabel, title, filename):
    x = [r[0] for r in results]

    plt.figure()
    plt.plot(x, [r[1] for r in results], marker='o', label="(a) Matrix + Array")
    plt.plot(x, [r[2] for r in results], marker='s', label="(b) Adj List + Min Heap")
    plt.xlabel(xlabel)
    plt.ylabel("Execution Time (seconds)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(RESULTS_DIR / filename, dpi=300)

if __name__ == "__main__":
    print("Sparse graphs (E = 2V)")
    sparse = compare_sparse()

    print("\nVarying density (V = 500)")
    density = compare_density()

    plot(sparse, "Number of Vertices (V)", "Part A vs Part B: Sparse Graphs (E = 2V)",
         "compare_sparse.png")
    plot(density, "Number of Edges (E)", "Part A vs Part B: Varying E (V = 500)",
         "compare_density.png")
