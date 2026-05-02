from pathlib import Path

from breadth_first_paths import BreadthFirstPaths
from depth_first_paths import DepthFirstPaths
from graph import Graph

STATE_BY_ID = ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"]
ID_BY_STATE = {state: idx for idx, state in enumerate(STATE_BY_ID)}


def format_path(path):
    if path is None:
        return "nao existe caminho"
    return " -> ".join(STATE_BY_ID[v] for v in path)


def format_vertices(vertices):
    return ", ".join(STATE_BY_ID[v] for v in vertices)


def read_state(prompt):
    while True:
        state = input(prompt).strip().upper()
        if state in ID_BY_STATE:
            return state
        print("Estado invalido. Use uma sigla valida do Nordeste (AL, BA, CE, MA, PB, PE, PI, RN, SE).")


def main():
    base_dir = Path(__file__).resolve().parent
    data_path = (base_dir / ".." / "dados" / "nordeste.txt").resolve()

    if not data_path.is_file():
        raise FileNotFoundError(f"Arquivo de dados nao encontrado: {data_path}")

    graph = Graph.from_file(str(data_path))

    print("Estados disponiveis:", ", ".join(STATE_BY_ID))
    origem = read_state("Informe o estado de origem (X): ")
    destino = read_state("Informe o estado de destino (Y): ")

    source = ID_BY_STATE[origem]
    target = ID_BY_STATE[destino]

    dfs = DepthFirstPaths(graph, source)
    bfs = BreadthFirstPaths(graph, source)

    print("\n========== RESULTADOS ==========")

    alcanca = dfs.has_path_to(target)
    print(f"1) E possivel sair de {origem} e chegar em {destino}? {'SIM' if alcanca else 'NAO'}")

    print(f"2) Caminho encontrado por DFS: {format_path(dfs.path_to(target))}")
    print(f"3) Caminho encontrado por BFS: {format_path(bfs.path_to(target))}")

    print(f"4) Estados alcancaveis a partir de {origem}: {format_vertices(dfs.reachable_vertices())}")

    print(f"5) Ordem de visita na DFS: {format_vertices(dfs.visit_order)}")
    print(f"6) Ordem de visita na BFS: {format_vertices(bfs.visit_order)}")


if __name__ == "__main__":
    main()
