"""Part (d): original Merge Sort vs Hybrid Merge Sort on 10 million integers.
"""
import csv
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save plots as files without opening a GUI window.
import matplotlib.pyplot as plt

from generate_data import load_dataset
from hybrid_sort import HybridMergeSort
from merge_sort import MergeSort


BASE = Path(__file__).resolve().parent / "results"
RESULTS = BASE / "part_d"
BEST_S_FILE = BASE / "part_c" / "best_thresholds.csv"
N = 10000000
REPEATS = 3


def read_best_S():
    """Take the best S found in part (c) for the largest tuning size."""
    with BEST_S_FILE.open() as file:
        rows = list(csv.DictReader(file))
    largest = max(rows, key=lambda row: int(row["n"]))
    return int(largest["best_S"])


def run(name, sort_fn, original, expected):
    """Run one algorithm REPEATS times; return (comparisons, times, average)."""
    times = []
    comparisons = None
    for trial in range(1, REPEATS + 1):
        A = original.copy()  # Same unsorted input every time.
        start = time.process_time()
        comparisons = sort_fn(A)
        cpu_time = time.process_time() - start
        assert A == expected  # Checking is outside the timer.
        times.append(cpu_time)
        print(f"{name}: trial {trial}, comparisons={comparisons}, CPU={cpu_time:.2f}s", flush=True)
        del A
    return comparisons, times, sum(times) / len(times)


def main(n=N, S=None):
    if S is None:
        S = int(sys.argv[1]) if len(sys.argv) > 1 else read_best_S()
    print(f"n={n:,}, S={S}", flush=True)

    original = load_dataset(n)
    expected = sorted(original)

    merge = run("MergeSort", lambda A: MergeSort(A, 0, n), original, expected)
    hybrid = run(f"Hybrid(S={S})", lambda A: HybridMergeSort(A, 0, n - 1, S), original, expected)

    RESULTS.mkdir(parents=True, exist_ok=True)
    with (RESULTS / "d_results.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["algorithm", "n", "S", "comparisons", "trial_1_cpu", "trial_2_cpu", "trial_3_cpu", "average_cpu_seconds"])
        writer.writerow(["MergeSort", n, "", merge[0], *merge[1], merge[2]])
        writer.writerow(["HybridMergeSort", n, S, hybrid[0], *hybrid[1], hybrid[2]])

    labels = ["Merge Sort", f"Hybrid (S={S})"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
    ax1.bar(labels, [merge[0], hybrid[0]], color=["tab:blue", "tab:orange"])
    ax1.set_ylabel("Key comparisons")
    ax1.set_title(f"Comparisons (n = {n:,})")
    ax2.bar(labels, [merge[2], hybrid[2]], color=["tab:blue", "tab:orange"])
    ax2.set_ylabel("Average CPU seconds")
    ax2.set_title(f"CPU time (n = {n:,})")
    fig.tight_layout()
    fig.savefig(RESULTS / "d_comparison.png")
    plt.close(fig)

    print(f"\nComparisons: MergeSort={merge[0]:,}  Hybrid={hybrid[0]:,}")
    print(f"Avg CPU:     MergeSort={merge[2]:.2f}s  Hybrid={hybrid[2]:.2f}s")


if __name__ == "__main__":
    main()
