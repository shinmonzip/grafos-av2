from __future__ import annotations

from typing import Dict, List, Tuple

from edge_weighted_digraph import EdgeWeightedDigraph


class DirectedEulerianCycle:
    """Implementa o metodo de Hierholzer para digrafos."""

    def __init__(self, graph: EdgeWeightedDigraph) -> None:
        self._graph = graph
        self._cycle_vertices: List[str] | None = None
        self._cycle_edges: List[Tuple[str, str, int]] | None = None

    def has_eulerian_cycle(self) -> bool:
        if self._graph.edge_count() == 0:
            return False
        if not self._graph.is_balanced():
            return False
        return self._graph.is_strongly_connected_on_active_vertices()

    def find_cycle(self) -> List[str]:
        if not self.has_eulerian_cycle():
            return []

        if self._cycle_vertices is not None:
            return list(self._cycle_vertices)

        adjacency_positions: Dict[str, int] = {
            vertex: 0 for vertex in self._graph.vertices()
        }
        adjacency = {
            vertex: self._graph.adjacency(vertex) for vertex in self._graph.vertices()
        }

        start = next(
            vertex
            for vertex in self._graph.vertices()
            if self._graph.out_degree(vertex) > 0
        )

        stack: List[str] = [start]
        circuit: List[str] = []

        while stack:
            vertex = stack[-1]
            pos = adjacency_positions[vertex]
            if pos < len(adjacency[vertex]):
                edge = adjacency[vertex][pos]
                adjacency_positions[vertex] += 1
                stack.append(edge.target)
            else:
                circuit.append(stack.pop())

        circuit.reverse()

        if len(circuit) != self._graph.edge_count() + 1:
            return []

        used_edges = self._materialize_cycle_edges(circuit, adjacency)
        if not used_edges:
            return []

        self._cycle_vertices = circuit
        self._cycle_edges = used_edges
        return list(self._cycle_vertices)

    def _materialize_cycle_edges(
        self,
        cycle_vertices: List[str],
        adjacency: Dict[str, List],
    ) -> List[Tuple[str, str, int]]:
        cursor_by_vertex: Dict[str, int] = {
            vertex: 0 for vertex in self._graph.vertices()
        }
        edge_list: List[Tuple[str, str, int]] = []

        for i in range(len(cycle_vertices) - 1):
            source = cycle_vertices[i]
            target = cycle_vertices[i + 1]

            found = None
            cursor = cursor_by_vertex[source]
            while cursor < len(adjacency[source]):
                edge = adjacency[source][cursor]
                cursor += 1
                if edge.target == target:
                    found = edge
                    break
            cursor_by_vertex[source] = cursor

            if found is None:
                return []

            edge_list.append((found.source, found.target, found.weight))

        if len(edge_list) != self._graph.edge_count():
            return []

        return edge_list

    def total_cost(self) -> int:
        if self._cycle_edges is None:
            self.find_cycle()
        if self._cycle_edges is None:
            return 0
        return sum(weight for _, _, weight in self._cycle_edges)
