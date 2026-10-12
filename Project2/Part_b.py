from graph_generation import (
    generate_edges,
    to_adjacency_list
)

# Teammate's Dijkstra function goes here

if __name__ == "__main__":
    V = 100
    E = 200

    edges = generate_edges(V, E)
    graph = to_adjacency_list(V, edges)

    result = dijkstra_heap(graph, 0)
    print(result)