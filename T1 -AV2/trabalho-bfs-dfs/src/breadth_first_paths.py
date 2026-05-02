from collections import deque


class BreadthFirstPaths:
    def __init__(self, graph, source: int):
        self._graph = graph
        self._source = source
        self._marked = [False] * graph.vertices
        self._edge_to = [-1] * graph.vertices
        self.visit_order = []

        self._bfs(source)

    def _bfs(self, source: int) -> None:
        queue = deque([source])
        self._marked[source] = True

        while queue:
            v = queue.popleft()
            self.visit_order.append(v)

            for w in self._graph.adj(v):
                if not self._marked[w]:
                    self._marked[w] = True
                    self._edge_to[w] = v
                    queue.append(w)

    def has_path_to(self, v: int) -> bool:
        return self._marked[v]

    def path_to(self, v: int):
        if not self.has_path_to(v):
            return None

        path = []
        x = v
        while x != self._source:
            path.append(x)
            x = self._edge_to[x]
        path.append(self._source)

        path.reverse()
        return path

    def reachable_vertices(self):
        return [v for v, marked in enumerate(self._marked) if marked]
