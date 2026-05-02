"""
graph.py  —  Grafo não direcionado (base algs4-py)

Representa um grafo não direcionado como um array de listas de adjacência.
Permite arestas paralelas e self-loops.

Formato de entrada (algs4):
    V          <- número de vértices
    E          <- número de arestas
    v1 w1      <- arestas (uma por linha)
    v2 w2
    ...
Os vértices devem ser indexados de 0 a V-1.
"""


class Graph:
    """Grafo não direcionado implementado com listas de adjacência."""

    def __init__(self, source):
        """
        Inicializa o grafo a partir de um arquivo (str) ou de um
        número de vértices (int).

        Parameters
        ----------
        source : str | int
            Caminho para o arquivo no formato algs4, ou número de
            vértices para criar um grafo vazio.
        """
        if isinstance(source, int):
            if source < 0:
                raise ValueError("Número de vértices não pode ser negativo")
            self._v = source
            self._e = 0
            self._adj = [[] for _ in range(self._v)]
        elif isinstance(source, str):
            self._read_from_file(source)
        else:
            raise TypeError("source deve ser um caminho de arquivo (str) "
                            "ou um número de vértices (int)")

    # ------------------------------------------------------------------
    # Leitura de arquivo
    # ------------------------------------------------------------------

    def _read_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                tokens = f.read().split()
        except OSError as exc:
            raise ValueError(f"Não foi possível ler '{filename}': {exc}") from exc

        if len(tokens) < 2:
            raise ValueError(
                f"Formato inválido em '{filename}': "
                "esperado número de vértices e arestas nas primeiras linhas"
            )

        idx = 0
        v = int(tokens[idx]); idx += 1
        e_expected = int(tokens[idx]); idx += 1

        if v < 0:
            raise ValueError("Número de vértices não pode ser negativo")
        if e_expected < 0:
            raise ValueError("Número de arestas não pode ser negativo")

        self._v = v
        self._e = 0
        self._adj = [[] for _ in range(v)]

        for i in range(e_expected):
            if idx + 1 >= len(tokens):
                raise ValueError(
                    f"Dados insuficientes em '{filename}': "
                    f"esperava {e_expected} arestas, encontrou apenas {i}"
                )
            a = int(tokens[idx]); idx += 1
            b = int(tokens[idx]); idx += 1
            self._validate_vertex(a)
            self._validate_vertex(b)
            self._add_edge(a, b)

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------

    def _validate_vertex(self, v):
        if v < 0 or v >= self._v:
            raise ValueError(
                f"vértice {v} fora do intervalo [0, {self._v - 1}]"
            )

    def _add_edge(self, v, w):
        self._e += 1
        self._adj[v].append(w)
        self._adj[w].append(v)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def add_edge(self, v, w):
        """Adiciona a aresta não direcionada v-w ao grafo."""
        self._validate_vertex(v)
        self._validate_vertex(w)
        self._add_edge(v, w)

    def V(self):
        """Retorna o número de vértices."""
        return self._v

    def E(self):
        """Retorna o número de arestas."""
        return self._e

    def adj(self, v):
        """Retorna a lista de vértices adjacentes a v."""
        self._validate_vertex(v)
        return self._adj[v]

    def degree(self, v):
        """Retorna o grau do vértice v."""
        self._validate_vertex(v)
        return len(self._adj[v])

    # ------------------------------------------------------------------
    # Representação textual
    # ------------------------------------------------------------------

    def __str__(self):
        lines = [f"{self._v} vertices, {self._e} arestas"]
        for v in range(self._v):
            neighbors = " ".join(str(w) for w in self._adj[v])
            lines.append(f"  {v}: {neighbors}")
        return "\n".join(lines)
