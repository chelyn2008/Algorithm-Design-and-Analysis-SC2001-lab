from graph_generation import (
    generate_edges,
    to_adjacency_matrix
)
INF = float('inf')

# Your Dijkstra function goes here
def dijkstra(graph, source):
    V = len(graph)
    dist = [INF] * V # creating array for priority queue
    visited = [False] * V # to mark whether visited 

    dist[source] = 0 # setting starting vertex distance to be 0

    for _ in range(V): # going through each vertex
        min_dist = INF
        u = -1 # selected vertex 

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
            # there is a direct edge that exists between the 2 vertices
            if not visited[v] and graph[u][v] != INF: 
                new_dist = dist[u] + graph[u][v]

                if new_dist < dist[v]:
                    dist[v] = new_dist

    return dist

if __name__ == "__main__":
    V = 100
    E = 200

    edges = generate_edges(V, E)
    graph = to_adjacency_matrix(V, edges)

    result = dijkstra(graph, 0)
    print(result)