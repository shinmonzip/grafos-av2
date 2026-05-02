from __future__ import annotations

from collections import deque

from graph import Graph


class BreadthFirstPaths:
    """Menor caminho em numero de arestas para grafo nao ponderado."""

    def __init__(self, graph: Graph, source: int) -> None:
        self._source = source
        self._marked = [False] * graph.v
        self._edge_to = [-1] * graph.v
        self._dist_to = [float("inf")] * graph.v

        self._bfs(graph, source)

    def _bfs(self, graph: Graph, source: int) -> None:
        queue: deque[int] = deque()
        self._marked[source] = True
        self._dist_to[source] = 0
        queue.append(source)

        while queue:
            vertex = queue.popleft()
            for neighbor in graph.adj(vertex):
                if not self._marked[neighbor]:
                    self._marked[neighbor] = True
                    self._edge_to[neighbor] = vertex
                    self._dist_to[neighbor] = self._dist_to[vertex] + 1
                    queue.append(neighbor)

    def has_path_to(self, vertex: int) -> bool:
        return self._marked[vertex]

    def dist_to(self, vertex: int) -> int:
        if self._dist_to[vertex] == float("inf"):
            return -1
        return int(self._dist_to[vertex])

    def path_to(self, vertex: int) -> list[int] | None:
        if not self.has_path_to(vertex):
            return None

        path: list[int] = []
        current = vertex
        while current != self._source:
            path.append(current)
            current = self._edge_to[current]
        path.append(self._source)
        path.reverse()
        return path
