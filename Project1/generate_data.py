"""Part (b): save random datasets for use in parts (c) and (d)."""
import random
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "datasets"
N_VALUES = [1000, 10000, 100000, 1000000, 10000000]
X = 1000  # Random integers are in [1, X], inclusive.
BASE_SEED = 2001


def generate_dataset(n, x, seed):
    """Write n random integers, one per line, without holding them all in memory."""
    if n < 1 or x < 1:
        raise ValueError("n and x must be positive")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"input_{n}.txt"
    rng = random.Random(seed)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for _ in range(n):
            file.write(f"{rng.randint(1, x)}\n")
    return path


def load_dataset(n):
    """Load a saved dataset into a list for a sorting experiment."""
    path = DATA_DIR / f"input_{n}.txt"
    with path.open(encoding="utf-8") as file:
        values = [int(line) for line in file]
    if len(values) != n:
        raise ValueError(f"Expected {n} integers in {path}, found {len(values)}")
    return values


def main():
    for n in N_VALUES:
        seed = BASE_SEED + n
        path = generate_dataset(n, X, seed)
        print(f"Saved {n:,} integers in [1, {X}] to {path.name} (seed={seed})", flush=True)


if __name__ == "__main__":
    main()
