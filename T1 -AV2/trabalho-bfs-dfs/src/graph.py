class Graph:
    def __init__(self, vertices: int):
        if vertices <= 0:
            raise ValueError("O numero de vertices deve ser maior que zero")

        self._v = vertices
        self._e = 0
        self._adj = [[] for _ in range(vertices)]

    @property
    def vertices(self) -> int:
        return self._v

    @property
    def edges(self) -> int:
        return self._e

    def _validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self._v:
            raise ValueError(f"Vertice invalido: {v}")

    def add_edge(self, v: int, w: int) -> None:
        self._validate_vertex(v)
        self._validate_vertex(w)

        self._adj[v].append(w)
        self._adj[w].append(v)
        self._e += 1

    def adj(self, v: int):
        self._validate_vertex(v)
        return self._adj[v]

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if not first_line:
                raise ValueError("Arquivo de grafo vazio")

            parts = first_line.split()
            if len(parts) != 2:
                raise ValueError("Primeira linha deve conter V e E")

            vertices, expected_edges = map(int, parts)
            graph = cls(vertices)

            edge_count = 0
            for line in f:
                line = line.strip()
                if not line:
                    continue

                v_str, w_str = line.split()
                graph.add_edge(int(v_str), int(w_str))
                edge_count += 1

            if edge_count != expected_edges:
                raise ValueError(
                    f"Quantidade de arestas inconsistente: esperado {expected_edges}, lido {edge_count}"
                )

            for v in range(graph.vertices):
                graph._adj[v].sort()

            return graph
