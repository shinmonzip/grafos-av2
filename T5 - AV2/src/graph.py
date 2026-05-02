"""
graph.py  –  Grafo nao-direcionado (estilo algs4).

Representacao por lista de adjacencia.
Formato de entrada (algs4):

    V
    E
    v1 w1
    v2 w2
    ...

Onde V eh o numero de vertices, E o numero de arestas e cada linha
seguinte descreve uma aresta.  Os tokens podem estar distribuidos em
qualquer numero de linhas (o parser le todos os tokens do arquivo).
"""


class Graph:
    """Grafo nao-direcionado com V vertices indexados de 0 a V-1."""

    # ------------------------------------------------------------------
    # Construtores
    # ------------------------------------------------------------------

    def __init__(self, source):
        """Inicializa o grafo.

        Parameters
        ----------
        source : int | file-like
            - int  : cria grafo vazio com *source* vertices.
            - file : le o grafo no formato algs4 a partir do objeto aberto.
        """
        if isinstance(source, int):
            if source < 0:
                raise ValueError("O numero de vertices nao pode ser negativo.")
            self._V = source
            self._E = 0
            self._adj = [[] for _ in range(self._V)]
        else:
            tokens = source.read().split()
            idx = 0

            self._V = int(tokens[idx]); idx += 1
            if self._V < 0:
                raise ValueError("O numero de vertices nao pode ser negativo.")

            self._adj = [[] for _ in range(self._V)]
            self._E = 0

            num_edges = int(tokens[idx]); idx += 1
            if num_edges < 0:
                raise ValueError("O numero de arestas nao pode ser negativo.")

            for _ in range(num_edges):
                v = int(tokens[idx]); idx += 1
                w = int(tokens[idx]); idx += 1
                self._add_edge(v, w)

    # ------------------------------------------------------------------
    # Metodos internos
    # ------------------------------------------------------------------

    def _validate_vertex(self, v):
        if not (0 <= v < self._V):
            raise ValueError(
                f"Vertice {v} fora do intervalo [0, {self._V - 1}]."
            )

    def _add_edge(self, v, w):
        self._validate_vertex(v)
        self._validate_vertex(w)
        self._adj[v].append(w)
        self._adj[w].append(v)
        self._E += 1

    # ------------------------------------------------------------------
    # API publica
    # ------------------------------------------------------------------

    def add_edge(self, v, w):
        """Adiciona a aresta nao-direcionada v-w."""
        self._add_edge(v, w)

    def V(self):
        """Numero de vertices."""
        return self._V

    def E(self):
        """Numero de arestas."""
        return self._E

    def adj(self, v):
        """Retorna a lista de vizinhos do vertice v."""
        self._validate_vertex(v)
        return self._adj[v]

    def degree(self, v):
        """Grau do vertice v."""
        self._validate_vertex(v)
        return len(self._adj[v])

    def __str__(self):
        lines = [f"{self._V} vertices, {self._E} arestas"]
        for v in range(self._V):
            neighbors = "  ".join(str(w) for w in self._adj[v])
            lines.append(f"  {v}: {neighbors}")
        return "\n".join(lines)
