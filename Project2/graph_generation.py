import random

INF = float('inf')

def generate_edges(V, E, seed=42):
    rng = random.Random(seed)

    max_edges = V * (V - 1) // 2

    if V < 1 or not V - 1 <= E <= max_edges:
        raise ValueError("Invalid V or E")

    edges = []
    used = set()

    # Step 1: Ensure all vertices are connected
    for v in range(1, V):
        u = rng.randrange(v)
        weight = rng.randint(1, 20)

        edges.append((u, v, weight))
        used.add((u, v))

    # Step 2: Add remaining random edges
    while len(edges) < E:
        u, v = rng.sample(range(V), 2)

        if u > v:
            u, v = v, u

        if (u, v) not in used:
            weight = rng.randint(1, 20)

            edges.append((u, v, weight))
            used.add((u, v))

    return edges


def to_adjacency_matrix(V, edges):
    graph = [[INF] * V for _ in range(V)]

    for i in range(V):
        graph[i][i] = 0

    for u, v, weight in edges:
        graph[u][v] = weight
        graph[v][u] = weight

    return graph


def to_adjacency_list(V, edges):
    graph = [[] for _ in range(V)]

    for u, v, weight in edges:
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    return graph


if __name__ == "__main__":
    V = 5
    E = 7

    edges = generate_edges(V, E)

    matrix = to_adjacency_matrix(V, edges)
    adj_list = to_adjacency_list(V, edges)

    print("Adjacency Matrix:")
    for row in matrix:
        print(row)

    print("\nAdjacency List:")
    for i, neighbours in enumerate(adj_list):
        print(i, neighbours)


# INF = float('inf')

# # input graph (test correctness of algorithm)
# graph = [ 
#     [0,   4,   2, INF, INF, INF, INF],
#     [4,   0,   1,   5,  10, INF, INF],
#     [2,   1,   0, INF,   3, INF, INF],
#     [INF, 5, INF,   0,   2,   6, INF],
#     [INF,10,   3,   2,   0,   4,   7],
#     [INF,INF,INF,   6,   4,   0,   1],
#     [INF,INF,INF, INF,   7,   1,   0]
# ]