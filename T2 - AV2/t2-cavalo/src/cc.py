from __future__ import annotations

from graph import Graph


class CC:
    """Componentes conexas por DFS."""

    def __init__(self, graph: Graph) -> None:
        self._marked = [False] * graph.v
        self._id = [-1] * graph.v
        self._count = 0

        for vertex in range(graph.v):
            if not self._marked[vertex]:
                self._dfs(graph, vertex)
                self._count += 1

    def _dfs(self, graph: Graph, vertex: int) -> None:
        self._marked[vertex] = True
        self._id[vertex] = self._count
        for neighbor in graph.adj(vertex):
            if not self._marked[neighbor]:
                self._dfs(graph, neighbor)

    @property
    def count(self) -> int:
        return self._count

    def id(self, vertex: int) -> int:
        return self._id[vertex]

    def components(self) -> list[list[int]]:
        groups: list[list[int]] = [[] for _ in range(self._count)]
        for vertex, component_id in enumerate(self._id):
            groups[component_id].append(vertex)
        return groups
