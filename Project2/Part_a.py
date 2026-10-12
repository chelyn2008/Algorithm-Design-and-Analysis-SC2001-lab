def dijkstra(graph, source):
    V = len(graph)
    dist = [INF] * V # creating array for priority queue
    visited = [False] * V # to mark whether visited 

    dist[source] = 0 # setting starting vertex distance to be 0

    for _ in range(V): # going through each vertex
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
