"""
tree_isomorphism.py  —  Análise de isomorfismo em árvores via codificação canônica

Implementa os três passos exigidos pelo trabalho:
  1. Validação: verifica se o grafo é de fato uma árvore (conexo, V-1 arestas).
  2. Centros: encontra 1 ou 2 centros por remoção iterativa de folhas.
  3. Codificação canônica: representação textual única, independente da
     rotulação e da ordem de inserção das arestas.

Uso:
    from graph import Graph
    from tree_isomorphism import TreeIsomorphism

    g = Graph("arvore.txt")
    ti = TreeIsomorphism(g)
    print(ti.get_validation_message())
    print(ti.get_centers())
    print(ti.get_canonical_encoding())
"""

from graph import Graph


class TreeIsomorphism:
    """
    Analisa um Graph para determinar se é uma árvore válida, encontra
    seu(s) centro(s) e calcula sua codificação canônica.
    """

    def __init__(self, graph):
        if graph is None:
            raise ValueError("graph não pode ser None")
        self._graph = graph
        self._is_valid = None
        self._validation_msg = None
        self._centers = None
        self._canonical = None
        # Valida imediatamente para guardar resultado em cache
        self._validate()

    # ------------------------------------------------------------------
    # 1. Validação
    # ------------------------------------------------------------------

    def _validate(self):
        """
        Uma árvore não direcionada com n vértices deve ter exatamente
        n-1 arestas e ser conexa.  Qualquer desvio (ciclo, floresta,
        grafo desconexo) invalida a entrada.
        """
        g = self._graph
        n = g.V()
        e = g.E()

        # Caso especial: grafo vazio
        if n == 0:
            self._is_valid = True
            self._validation_msg = "Válido: árvore vazia (0 vértices)"
            return

        # Verificação 1 — número de arestas
        if e != n - 1:
            self._is_valid = False
            self._validation_msg = (
                f"Inválido: {n} vértices e {e} arestas "
                f"(uma árvore com {n} vértices deve ter exatamente "
                f"{n - 1} aresta{'s' if n - 1 != 1 else ''})"
            )
            return

        # Verificação 2 — conectividade por DFS iterativa
        visited = [False] * n
        stack = [0]
        visited[0] = True
        count = 1
        while stack:
            u = stack.pop()
            for v in g.adj(u):
                if not visited[v]:
                    visited[v] = True
                    count += 1
                    stack.append(v)

        if count != n:
            self._is_valid = False
            self._validation_msg = (
                f"Inválido: grafo não é conexo "
                f"({count} de {n} vértices alcançados a partir do vértice 0)"
            )
        else:
            self._is_valid = True
            self._validation_msg = (
                f"Válido: é uma árvore ({n} vértice{'s' if n != 1 else ''}, "
                f"{e} aresta{'s' if e != 1 else ''})"
            )

    def is_tree(self):
        """Retorna True se o grafo é uma árvore válida."""
        return self._is_valid

    def get_validation_message(self):
        """Retorna a mensagem descritiva do resultado da validação."""
        return self._validation_msg

    # ------------------------------------------------------------------
    # 2. Centros
    # ------------------------------------------------------------------

    def get_centers(self):
        """
        Encontra o(s) centro(s) da árvore por remoção iterativa de folhas.

        O algoritmo mantém os graus efetivos dos vértices não removidos e
        remove repetidamente as folhas atuais até restar 1 ou 2 vértices —
        os centros.

        Returns
        -------
        list[int]
            Lista com 1 ou 2 vértices que são os centros da árvore.

        Raises
        ------
        RuntimeError
            Se chamado em um grafo que não é uma árvore válida.
        """
        if not self._is_valid:
            raise RuntimeError(
                "Não é possível calcular centros de um grafo inválido"
            )

        if self._centers is not None:
            return self._centers

        g = self._graph
        n = g.V()

        # Caso base: árvore com um único vértice
        if n == 1:
            self._centers = [0]
            return self._centers

        # Graus efetivos (decrementados à medida que vizinhos são removidos)
        degree = [g.degree(v) for v in range(n)]
        removed = [False] * n

        # Folhas iniciais: vértices com grau 0 ou 1
        leaves = [v for v in range(n) if degree[v] <= 1]
        processed = len(leaves)

        while processed < n:
            new_leaves = []
            for u in leaves:
                removed[u] = True
                for v in g.adj(u):
                    if not removed[v]:
                        degree[v] -= 1
                        # Quando um vértice fica com grau 1 é a próxima folha
                        if degree[v] == 1:
                            new_leaves.append(v)
            processed += len(new_leaves)
            leaves = new_leaves

        # 'leaves' agora contém 1 ou 2 centros
        self._centers = leaves
        return self._centers

    # ------------------------------------------------------------------
    # 3. Codificação canônica
    # ------------------------------------------------------------------

    def get_canonical_encoding(self):
        """
        Gera a codificação canônica da árvore.

        A codificação é uma string de parênteses que representa
        univocamente a estrutura da árvore, independente da rotulação
        dos vértices e da ordem de inserção das arestas.

        Quando a árvore tem dois centros, os dois sub-códigos são
        ordenados lexicograficamente antes de serem combinados, garantindo
        que duas árvores isomorfas com centros em ordens diferentes produzam
        o mesmo resultado.

        Returns
        -------
        str
            Código canônico no formato de parênteses aninhados.

        Raises
        ------
        RuntimeError
            Se chamado em um grafo que não é uma árvore válida.
        """
        if not self._is_valid:
            raise RuntimeError(
                "Não é possível calcular a codificação de um grafo inválido"
            )

        if self._canonical is not None:
            return self._canonical

        centers = self.get_centers()

        if len(centers) == 1:
            # Árvore com centro único: enraiza no centro e codifica
            self._canonical = self._encode(centers[0], -1)
        else:
            # Árvore com dois centros c1 e c2:
            # Cada centro enxerga o outro como seu "pai" na direção da raiz.
            # Ordenamos os dois sub-códigos para garantir determinismo.
            c1, c2 = centers[0], centers[1]
            code1 = self._encode(c1, c2)
            code2 = self._encode(c2, c1)
            parts = sorted([code1, code2])
            self._canonical = "(" + "".join(parts) + ")"

        return self._canonical

    def _encode(self, v, parent):
        """
        Codifica recursivamente a subárvore enraizada em v, com 'parent'
        como vértice pai (evita retroceder).

        Algoritmo:
          1. Se v é folha (sem filhos), retorna "()"
          2. Para cada filho, calcula seu código recursivamente
          3. Ordena os códigos lexicograficamente (garante determinismo)
          4. Concatena e envolve entre parênteses
        """
        child_codes = sorted(
            self._encode(u, v)
            for u in self._graph.adj(v)
            if u != parent
        )
        return "(" + "".join(child_codes) + ")"
