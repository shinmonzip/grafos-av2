from __future__ import annotations

from graph import Graph


class Cycle:
    """Deteccao de ciclo em grafo nao direcionado com recuperacao de um ciclo."""

    def __init__(self, graph: Graph) -> None:
        self._marked = [False] * graph.v
        self._edge_to = [-1] * graph.v
        self._cycle: list[int] | None = None

        for vertex in range(graph.v):
            if not self._marked[vertex] and self._cycle is None:
                self._dfs(graph, vertex, -1)

    def _dfs(self, graph: Graph, vertex: int, parent: int) -> None:
        self._marked[vertex] = True

        for neighbor in reversed(graph.adj(vertex)):
            if self._cycle is not None:
                return

            if not self._marked[neighbor]:
                self._edge_to[neighbor] = vertex
                self._dfs(graph, neighbor, vertex)
            elif neighbor != parent:
                self._cycle = self._build_cycle(vertex, neighbor)
                return

    def _build_cycle(self, vertex: int, neighbor: int) -> list[int]:
        cycle = [neighbor]
        current = vertex

        while current != neighbor and current != -1:
            cycle.append(current)
            current = self._edge_to[current]

        cycle.append(neighbor)
        cycle.reverse()
        return cycle

    def has_cycle(self) -> bool:
        return self._cycle is not None

    def cycle_vertices(self) -> list[int] | None:
        return self._cycle
