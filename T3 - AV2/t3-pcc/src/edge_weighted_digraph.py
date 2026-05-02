from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, Iterable, List, Set

from directed_edge import DirectedEdge


class EdgeWeightedDigraph:
    """Digrafo ponderado que permite arestas repetidas."""

    def __init__(self, expected_vertices: int = 0) -> None:
        self.expected_vertices = expected_vertices
        self._adj: Dict[str, List[DirectedEdge]] = defaultdict(list)
        self._in_degree: Dict[str, int] = defaultdict(int)
        self._out_degree: Dict[str, int] = defaultdict(int)
        self._vertices: Set[str] = set()
        self._edge_count = 0

    def add_edge(self, edge: DirectedEdge) -> None:
        self._adj[edge.source].append(edge)
        self._out_degree[edge.source] += 1
        self._in_degree[edge.target] += 1
        self._vertices.add(edge.source)
        self._vertices.add(edge.target)
        self._edge_count += 1

    def vertices(self) -> List[str]:
        return sorted(self._vertices)

    def adjacency(self, vertex: str) -> List[DirectedEdge]:
        return list(self._adj.get(vertex, []))

    def in_degree(self, vertex: str) -> int:
        return self._in_degree.get(vertex, 0)

    def out_degree(self, vertex: str) -> int:
        return self._out_degree.get(vertex, 0)

    def edge_count(self) -> int:
        return self._edge_count

    def is_balanced(self) -> bool:
        for vertex in self.vertices():
            if self.in_degree(vertex) != self.out_degree(vertex):
                return False
        return True

    def active_vertices(self) -> List[str]:
        return [
            vertex
            for vertex in self.vertices()
            if self.in_degree(vertex) > 0 or self.out_degree(vertex) > 0
        ]

    def _bfs_reachable(self, start: str, graph: Dict[str, List[str]]) -> Set[str]:
        visited: Set[str] = set()
        queue: deque[str] = deque([start])
        visited.add(start)

        while queue:
            current = queue.popleft()
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return visited

    def is_strongly_connected_on_active_vertices(self) -> bool:
        active = self.active_vertices()
        if not active:
            return True

        active_set = set(active)
        directed: Dict[str, List[str]] = defaultdict(list)
        reverse: Dict[str, List[str]] = defaultdict(list)

        for vertex in active:
            directed[vertex]
            reverse[vertex]

        for vertex in active:
            for edge in self._adj.get(vertex, []):
                if edge.target in active_set:
                    directed[edge.source].append(edge.target)
                    reverse[edge.target].append(edge.source)

        root = active[0]
        reachable = self._bfs_reachable(root, directed)
        if len(reachable) != len(active):
            return False

        reachable_reverse = self._bfs_reachable(root, reverse)
        return len(reachable_reverse) == len(active)

    def total_weight(self) -> int:
        weight_sum = 0
        for vertex in self._adj:
            for edge in self._adj[vertex]:
                weight_sum += edge.weight
        return weight_sum

    def iter_edges(self) -> Iterable[DirectedEdge]:
        for vertex in self.vertices():
            for edge in self._adj.get(vertex, []):
                yield edge
