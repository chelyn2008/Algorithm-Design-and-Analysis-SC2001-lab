# INF = float('inf')

# # input graph
# graph = [ 
#     [0,   4,   2, INF, INF, INF, INF],
#     [4,   0,   1,   5,  10, INF, INF],
#     [2,   1,   0, INF,   3, INF, INF],
#     [INF, 5, INF,   0,   2,   6, INF],
#     [INF,10,   3,   2,   0,   4,   7],
#     [INF,INF,INF,   6,   4,   0,   1],
#     [INF,INF,INF, INF,   7,   1,   0]
# ]

import random

INF = float('inf')

def generate_graph(V, E, seed=42):
    rng = random.Random(seed)

    max_edges = V * (V - 1) // 2

    if not V - 1 <= E <= max_edges:
        raise ValueError("Invalid edge count")

    graph = [[INF] * V for _ in range(V)]

    for i in range(V):
        graph[i][i] = 0

    edges = set()

    # Ensure the graph is connected
    for i in range(1, V):
        j = rng.randrange(i)
        graph[i][j] = graph[j][i] = rng.randint(1, 20)
        edges.add((j, i))

    # Add random edges until E is reached
    while len(edges) < E:
        u, v = rng.sample(range(V), 2)
        a, b = sorted((u, v))

        if (a, b) not in edges:
            edges.add((a, b))
            graph[a][b] = graph[b][a] = rng.randint(1, 20)

    return graph


def dijkstra(graph, source):
    V = len(graph)
    dist = [INF] * V
    visited = [False] * V

    dist[source] = 0

    for _ in range(V):
        min_dist = INF
        u = -1

        # Array-based minimum selection
        for v in range(V):
            if not visited[v] and dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        if u == -1:
            break

        visited[u] = True

        # Scan adjacency matrix row
        for v in range(V):
            if not visited[v] and graph[u][v] != INF:
                new_dist = dist[u] + graph[u][v]

                if new_dist < dist[v]:
                    dist[v] = new_dist

    return dist

result = dijkstra(graph, 0)

for i, distance in enumerate(result):
    print(f"{chr(65+i)}: {distance}")
