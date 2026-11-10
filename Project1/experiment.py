"""Part (c): run with python experiment.py."""
import csv
import math
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save plots as files without opening a GUI window.
import matplotlib.pyplot as plt

from generate_data import N_VALUES, load_dataset
from hybrid_sort import HybridMergeSort


RESULTS = Path(__file__).resolve().parent / "results" / "part_c"
S_VALUES = [1, 2, 4, 8, 16, 32, 64, 128]


def save_results(filename, headings, rows):
    with (RESULTS / filename).open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headings)
        writer.writerows(rows)


def part_c_i():
    # Keep S fixed and change the input size n.
    S = 16
    comparison_counts = []
    rows = []

    for n in N_VALUES:
        A = load_dataset(n)
        comparisons = HybridMergeSort(A, 0, n - 1, S)
        assert A == sorted(A)  # Check the result is sorted.
        comparison_counts.append(comparisons)
        rows.append([n, S, comparisons])
        print(f"c(i): n={n}, S={S}, comparisons={comparisons}", flush=True)
        del A

    save_results("c_i_results.csv", ["n", "S", "comparisons"], rows)

    # Scale n log2(n) so we can compare its growth with our measurements.
    theory = []
    scale = comparison_counts[-1] / (N_VALUES[-1] * math.log2(N_VALUES[-1]))
    for n in N_VALUES:
        theory.append(scale * n * math.log2(n))

    plt.figure()
    plt.loglog(N_VALUES, comparison_counts, "o-", label="Measured comparisons")
    plt.loglog(N_VALUES, theory, "--", label="Scaled n log2(n)")
    plt.xlabel("Input size n")
    plt.ylabel("Key comparisons")
    plt.title("c(i): Fixed S = 16")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "c_i_fixed_s.png")
    plt.close()


def part_c_ii():
    # Keep n fixed and change the threshold S.
    n = 100000
    original = load_dataset(n)
    expected = sorted(original)
    comparison_counts = []
    rows = []

    for S in S_VALUES:
        A = original.copy()  # Each threshold gets the same unsorted input.
        comparisons = HybridMergeSort(A, 0, n - 1, S)
        assert A == expected
        comparison_counts.append(comparisons)
        rows.append([n, S, comparisons])
        print(f"c(ii): n={n}, S={S}, comparisons={comparisons}", flush=True)

    save_results("c_ii_results.csv", ["n", "S", "comparisons"], rows)
    plt.figure()
    plt.plot(S_VALUES, comparison_counts, "o-")
    plt.xlabel("Threshold S")
    plt.ylabel("Key comparisons")
    plt.title("c(ii): Fixed n = 100,000")
    plt.tight_layout()
    plt.savefig(RESULTS / "c_ii_fixed_n.png")
    plt.close()


def part_c_iii():
    # Compare thresholds at two sizes to find the fastest tested S.
    # These larger inputs avoid near-zero CPU readings on Windows.
    n_values = [100000, 1000000]
    repeats = 3
    rows = []
    trial_rows = []
    best_rows = []
    plt.figure()

    for n in n_values:
        original = load_dataset(n)
        expected = sorted(original)
        average_times = []
        best_S = S_VALUES[0]
        best_time = float("inf")

        for S in S_VALUES:
            total_time = 0
            for trial in range(1, repeats + 1):
                A = original.copy()
                start = time.process_time()
                comparisons = HybridMergeSort(A, 0, n - 1, S)
                cpu_time = time.process_time() - start
                total_time += cpu_time
                assert A == expected  # Checking is outside the timer.
                trial_rows.append([n, S, trial, comparisons, cpu_time])

            average_time = total_time / repeats
            average_times.append(average_time)
            rows.append([n, S, comparisons, average_time])
            if average_time < best_time:
                best_time = average_time
                best_S = S
            print(f"c(iii): n={n}, S={S}, average CPU={average_time:.4f}s", flush=True)

        best_rows.append([n, best_S, best_time])
        print(f"Best tested S for n={n}: {best_S}", flush=True)
        plt.plot(S_VALUES, average_times, "o-", label=f"n = {n:,}")

    save_results("c_iii_results.csv", ["n", "S", "comparisons", "average_cpu_seconds"], rows)
    save_results("c_iii_trials.csv", ["n", "S", "trial", "comparisons", "cpu_seconds"], trial_rows)
    save_results("best_thresholds.csv", ["n", "best_S", "average_cpu_seconds"], best_rows)
    plt.xlabel("Threshold S")
    plt.ylabel("Average CPU seconds (log scale)")
    plt.yscale("log")
    plt.title("c(iii): Find the fastest threshold")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "c_iii_threshold_times.png")
    plt.close()
    print(f"Use S={best_rows[-1][1]} from the largest tuning size for part (d).")


if __name__ == "__main__":
    RESULTS.mkdir(parents=True, exist_ok=True)
    part_c_i()
    part_c_ii()
    part_c_iii()
