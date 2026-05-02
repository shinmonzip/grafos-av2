from __future__ import annotations

import argparse
from pathlib import Path

from bfs_paths import BreadthFirstPaths
from cc import CC
from cycle import Cycle
from graph import GraphInputError, GraphReader, Position, position_to_vertex


def format_vertex_list(vertices: list[int]) -> str:
    return " ".join(str(v) for v in vertices)


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    default_input = project_root / "dados" / "entrada.txt"

    parser = argparse.ArgumentParser(
        description="Analise do grafo do cavalo (tabuleiro 3x3)."
    )
    parser.add_argument(
        "--input",
        dest="input_path",
        default=str(default_input),
        help="Caminho para o arquivo de entrada no formato algs4.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_path)

    try:
        graph = GraphReader.from_file(str(input_path.resolve()))
    except (OSError, GraphInputError, ValueError) as exc:
        print(f"Erro ao carregar o grafo: {exc}")
        return

    print("=== Lista de adjacencia ===")
    print(graph.to_adjacency_list_str())

    print("\n=== Componentes conexas ===")
    cc = CC(graph)
    print(f"Quantidade de componentes: {cc.count}")
    for component_id, vertices in enumerate(cc.components()):
        print(f"Vertices da componente {component_id}: {format_vertex_list(vertices)}")

    print("\n=== Distancia minima entre (0,0) e (2,2) ===")
    source = position_to_vertex(Position(0, 0))
    target = position_to_vertex(Position(2, 2))
    bfs = BreadthFirstPaths(graph, source)
    distance = bfs.dist_to(target)

    if distance == -1:
        print("Nao existe caminho entre as posicoes informadas.")
    else:
        print(f"Distancia minima (em arestas): {distance}")
        path = bfs.path_to(target)
        if path is not None:
            print(f"Um menor caminho encontrado: {format_vertex_list(path)}")

    print("\n=== Analise de ciclo ===")
    cycle = Cycle(graph)
    print(f"O grafo possui ciclo: {'Sim' if cycle.has_cycle() else 'Nao'}")
    print("Complexidade de tempo (DFS): O(V + E)")
    print("Complexidade de espaco (DFS): O(V)")

    if cycle.has_cycle():
        cycle_vertices = cycle.cycle_vertices()
        if cycle_vertices is not None:
            print(f"Um ciclo encontrado: {format_vertex_list(cycle_vertices)}")


if __name__ == "__main__":
    main()
