from graph_generation import (
    generate_edges,
    to_adjacency_list
)
INF = float('inf')

# Minimizing heap used as the priority queue.
# Each heap entry is a (distance, vertex) pair. pos[v] remembers where vertex v
# sits inside the heap so that decrease_key can find it in O(1).
class MinHeap:
    def __init__(self, V):
        self.heap = []        # array holding the binary heap
        self.pos = [-1] * V   # pos[v] = index of v in heap, -1 if not in heap

    def is_empty(self):
        return len(self.heap) == 0

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos[self.heap[i][1]] = i
        self.pos[self.heap[j][1]] = j

    # move entry at index i up until its parent is smaller - O(log V)
    def sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i][0] < self.heap[parent][0]:
                self.swap(i, parent)
                i = parent
            else:
                break

    # move entry at index i down until both children are larger - O(log V)
    def sift_down(self, i):
        n = len(self.heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == i:
                break

            self.swap(i, smallest)
            i = smallest

    def insert(self, v, d):
        self.heap.append((d, v))
        self.pos[v] = len(self.heap) - 1
        self.sift_up(self.pos[v])

    # remove and return the vertex with the smallest distance - O(log V)
    def extract_min(self):
        d, u = self.heap[0]
        last = self.heap.pop()
        self.pos[u] = -1

        if self.heap: # put the last entry at the root and fix the heap
            self.heap[0] = last
            self.pos[last[1]] = 0
            self.sift_down(0)

        return u, d

    # lower the distance of vertex v that is already in the heap - O(log V)
    def decrease_key(self, v, d):
        i = self.pos[v]
        self.heap[i] = (d, v)
        self.sift_up(i)

    def contains(self, v):
        return self.pos[v] != -1


# Dijkstra using an array of adjacency lists and a minimizing heap
def dijkstra_heap(graph, source):
    V = len(graph)
    dist = [INF] * V
    visited = [False] * V # to mark whether visited

    dist[source] = 0 # setting starting vertex distance to be 0

    # put every vertex into the priority queue - O(V log V)
    pq = MinHeap(V)
    for v in range(V):
        pq.insert(v, dist[v])

    while not pq.is_empty(): # runs V times
        u, d = pq.extract_min() # O(log V) instead of O(V) array scan

        if d == INF: # remaining vertices are unreachable
            break

        visited[u] = True

        # Scan only the neighbours of u (adjacency list), not a whole matrix row.
        # Over the whole run every edge is looked at twice -> O(E) relaxations.
        for v, weight in graph[u]:
            if not visited[v]:
                new_dist = dist[u] + weight

                if new_dist < dist[v]:
                    dist[v] = new_dist
                    pq.decrease_key(v, new_dist) # O(log V)

    return dist

if __name__ == "__main__":
    V = 100
    E = 200

    edges = generate_edges(V, E)
    graph = to_adjacency_list(V, edges)

    result = dijkstra_heap(graph, 0)
    print(result)
