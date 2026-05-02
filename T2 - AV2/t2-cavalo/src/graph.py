from __future__ import annotations

from dataclasses import dataclass


class GraphInputError(ValueError):
    """Erro de formato no arquivo de entrada do grafo."""


@dataclass(frozen=True)
class Position:
    row: int
    col: int


class Graph:
    def __init__(self, vertex_count: int) -> None:
        if vertex_count <= 0:
            raise ValueError("O numero de vertices deve ser positivo.")

        self._v = vertex_count
        self._e = 0
        self._adj: list[list[int]] = [[] for _ in range(vertex_count)]

    @property
    def v(self) -> int:
        return self._v

    @property
    def e(self) -> int:
        return self._e

    def _validate_vertex(self, vertex: int) -> None:
        if vertex < 0 or vertex >= self._v:
            raise ValueError(
                f"Vertice invalido: {vertex}. Deve estar entre 0 e {self._v - 1}."
            )

    def add_edge(self, v: int, w: int) -> None:
        self._validate_vertex(v)
        self._validate_vertex(w)

        self._adj[v].append(w)
        self._adj[w].append(v)
        self._e += 1

    def adj(self, vertex: int) -> list[int]:
        self._validate_vertex(vertex)
        return self._adj[vertex]

    def to_adjacency_list_str(self) -> str:
        lines: list[str] = []
        for vertex in range(self._v):
            neighbors = " ".join(str(w) for w in self._adj[vertex])
            lines.append(f"{vertex}: {neighbors}".rstrip())
        return "\n".join(lines)


class GraphReader:
    """Leitura de arquivo no formato algs4: V, E, seguido de E pares v w."""

    @staticmethod
    def from_file(path: str) -> Graph:
        with open(path, "r", encoding="utf-8") as file:
            raw_lines = [line.strip() for line in file if line.strip()]

        if len(raw_lines) < 2:
            raise GraphInputError("Arquivo invalido: faltam as linhas de V e E.")

        try:
            vertex_count = int(raw_lines[0])
            edge_count = int(raw_lines[1])
        except ValueError as exc:
            raise GraphInputError("As duas primeiras linhas devem conter inteiros (V e E).") from exc

        graph = Graph(vertex_count)

        edge_lines = raw_lines[2:]
        if len(edge_lines) != edge_count:
            raise GraphInputError(
                f"Quantidade de arestas invalida: esperado {edge_count}, lido {len(edge_lines)}."
            )

        for index, line in enumerate(edge_lines, start=1):
            tokens = line.split()
            if len(tokens) != 2:
                raise GraphInputError(
                    f"Linha de aresta #{index} invalida: '{line}'. Use formato 'v w'."
                )
            try:
                v, w = int(tokens[0]), int(tokens[1])
            except ValueError as exc:
                raise GraphInputError(
                    f"Linha de aresta #{index} invalida: '{line}'. Vertices devem ser inteiros."
                ) from exc
            graph.add_edge(v, w)

        return graph


def position_to_vertex(position: Position, board_size: int = 3) -> int:
    if position.row < 0 or position.row >= board_size or position.col < 0 or position.col >= board_size:
        raise ValueError("Posicao fora dos limites do tabuleiro.")
    return position.row * board_size + position.col
