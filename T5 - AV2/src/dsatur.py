"""
dsatur.py  –  Algoritmo DSatur para coloracao de vertices.

Referencia: Brelaz, D. (1979). New methods to color the vertices of a graph.
Communications of the ACM, 22(4), 251-256.

Descricao do algoritmo
----------------------
1. Colorir o vertice de maior grau com a cor 1.
2. R <- V \ {v}
3. Enquanto R != vazio:
   a. Para cada v' em R, calcular DS(v') = numero de cores distintas na
      vizinhanca ja colorida de v'.
   b. Escolher v' com maximo DS(v'); empate: maior grau; empate: arbitrario.
   c. Atribuir a v' a menor cor k >= 1 que nao conflite com vizinhos.
   d. Se k > colors: colors <- k
   e. R <- R \ {v'}
"""


class GraphColoringDSatur:
    """Heuristica DSatur para coloracao de vertices de um grafo."""

    def __init__(self, graph):
        if graph is None:
            raise ValueError("graph nao pode ser None.")
        self._graph = graph
        self._color = None          # cor de cada vertice (1-indexado); -1 = sem cor
        self._coloring_order = None # ordem em que os vertices foram coloridos
        self._color_count = 0       # total de cores utilizadas

    # ------------------------------------------------------------------
    # Execucao principal
    # ------------------------------------------------------------------

    def color(self):
        """Executa o algoritmo DSatur e preenche a coloracao."""
        V = self._graph.V()
        self._color = [-1] * V
        self._coloring_order = []
        self._color_count = 0

        if V == 0:
            return

        # Pre-computa o grau de cada vertice (imutavel durante o algoritmo)
        degree = [self._graph.degree(v) for v in range(V)]

        # Passo 1: colorir o vertice de maior grau (empate: menor indice)
        first = max(range(V), key=lambda v: (degree[v], -v))
        self._color[first] = 1
        self._coloring_order.append(first)
        self._color_count = 1

        remaining = set(range(V))
        remaining.remove(first)

        # sat[v] = conjunto de cores distintas ja presentes na vizinhanca de v
        sat = [set() for _ in range(V)]
        for w in self._graph.adj(first):
            sat[w].add(1)

        # Passo 2: colorir os demais vertices
        while remaining:
            # Escolher o vertice com maior grau de saturacao;
            # desempate pelo maior grau estatico; segundo desempate: menor indice.
            best = max(
                remaining,
                key=lambda v: (len(sat[v]), degree[v], -v),
            )

            # Menor cor disponivel nao presente na vizinhanca de best
            used = sat[best]
            k = 1
            while k in used:
                k += 1

            self._color[best] = k
            if k > self._color_count:
                self._color_count = k

            self._coloring_order.append(best)
            remaining.remove(best)

            # Atualiza o grau de saturacao dos vizinhos ainda nao coloridos
            for w in self._graph.adj(best):
                if self._color[w] == -1:
                    sat[w].add(k)

    # ------------------------------------------------------------------
    # Consultas pos-execucao
    # ------------------------------------------------------------------

    def get_color(self, vertex):
        """Retorna a cor atribuida ao vertice (1-indexada)."""
        return self._color[vertex]

    def get_color_count(self):
        """Retorna o total de cores utilizadas."""
        return self._color_count

    def get_coloring_order(self):
        """Retorna a lista de vertices na ordem em que foram coloridos."""
        return list(self._coloring_order)

    def is_valid_coloring(self):
        """Retorna True se nenhum par de vertices adjacentes tem a mesma cor."""
        for v in range(self._graph.V()):
            for w in self._graph.adj(v):
                if self._color[v] == self._color[w]:
                    return False
        return True
