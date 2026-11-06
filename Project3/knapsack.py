"""Unbounded knapsack using bottom-up dynamic programming."""


def max_profit(capacity, weights, profits):
    """Return the best profit at each capacity and one choice of objects."""
    if capacity < 0 or len(weights) != len(profits):
        raise ValueError("Invalid capacity or mismatched weights and profits")
    if any(w <= 0 for w in weights) or any(p <= 0 for p in profits):
        raise ValueError("Weights and profits must be positive")

    best = [0] * (capacity + 1)
    choice = [None] * (capacity + 1)

    for c in range(1, capacity + 1):
        for i, weight in enumerate(weights):
            if weight <= c:
                candidate = profits[i] + best[c - weight]
                if candidate > best[c]:
                    best[c] = candidate
                    choice[c] = i

    objects = []
    remaining = capacity
    while choice[remaining] is not None:
        i = choice[remaining]
        objects.append(i)
        remaining -= weights[i]

    return best, objects


def show_result(capacity, weights, profits):
    best, objects = max_profit(capacity, weights, profits)
    print(f"Capacity: {capacity}")
    print(f"Weights: {weights}; profits: {profits}")
    print("c:   ", *range(capacity + 1))
    print("P(c):", *best)
    print(f"Maximum profit P({capacity}): {best[capacity]}")
    print(f"Objects chosen (0-based, repeats allowed): {objects}")
    print()


if __name__ == "__main__":
    show_result(16, [4, 5, 8], [7, 6, 9])
    show_result(12, [5, 6, 7], [7, 6, 9])
