from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

from directed_edge import DirectedEdge
from directed_eulerian_cycle import DirectedEulerianCycle
from edge_weighted_digraph import EdgeWeightedDigraph


def resolve_input_path(argument: str | None) -> Path:
    project_root = Path(__file__).resolve().parent.parent
    default_path = project_root / "dados" / "entrada_eulerizada.txt"

    if argument is None:
        return default_path

    candidate = Path(argument)
    if candidate.is_absolute():
        return candidate

    # Caminho relativo sempre eh resolvido a partir da raiz do projeto.
    return (project_root / candidate).resolve()


def parse_input_file(file_path: Path) -> Tuple[EdgeWeightedDigraph, int, int]:
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {file_path}")

    with file_path.open("r", encoding="utf-8") as fp:
        lines = [line.strip() for line in fp if line.strip() and not line.startswith("#")]

    if len(lines) < 2:
        raise ValueError("Entrada invalida: sao necessarias pelo menos 2 linhas (V e E).")

    try:
        expected_vertices = int(lines[0])
        expected_edges = int(lines[1])
    except ValueError as exc:
        raise ValueError("As duas primeiras linhas devem ser inteiros (V e E).") from exc

    graph = EdgeWeightedDigraph(expected_vertices=expected_vertices)

    for index, line in enumerate(lines[2:], start=3):
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(
                f"Linha {index} invalida: esperado formato 'v w peso', recebido: {line}"
            )

        source, target, weight_text = parts

        try:
            weight = int(weight_text)
        except ValueError as exc:
            raise ValueError(f"Linha {index} invalida: peso deve ser inteiro.") from exc

        graph.add_edge(DirectedEdge(source=source, target=target, weight=weight))

    if graph.edge_count() != expected_edges:
        raise ValueError(
            "Quantidade de arestas inconsistente: "
            f"E={expected_edges}, lidas={graph.edge_count()}."
        )

    vertices_read = len(graph.vertices())
    if vertices_read > expected_vertices:
        raise ValueError(
            "Quantidade de vertices distinta do cabecalho: "
            f"V={expected_vertices}, distintos_lidos={vertices_read}."
        )

    return graph, expected_vertices, expected_edges


def print_degrees(graph: EdgeWeightedDigraph) -> None:
    print("Graus dos vertices")
    print("vertice | entrada | saida | saldo")
    print("---------------------------------")

    for vertex in graph.vertices():
        in_degree = graph.in_degree(vertex)
        out_degree = graph.out_degree(vertex)
        delta = out_degree - in_degree
        print(f"{vertex:<7} | {in_degree:>7} | {out_degree:>5} | {delta:>5}")


def load_original_cost_if_available(input_path: Path) -> int | None:
    """Retorna o custo do grafo original quando houver arquivo correspondente."""
    if input_path.name != "entrada_eulerizada.txt":
        return None

    original_path = input_path.with_name("entrada_original.txt")
    if not original_path.exists():
        return None

    original_graph, _, _ = parse_input_file(original_path)
    return original_graph.total_weight()


def main() -> int:
    file_arg = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        input_path = resolve_input_path(file_arg)
        graph, expected_vertices, expected_edges = parse_input_file(input_path)

        print(f"Arquivo lido: {input_path}")
        print(f"Vertices: {expected_vertices} | Arestas: {expected_edges}")
        print()

        print_degrees(graph)
        print()

        if not graph.is_balanced():
            print("Erro: o grafo nao esta balanceado. Nao existe circuito euleriano.")
            return 1

        if not graph.is_strongly_connected_on_active_vertices():
            print("Erro: o grafo nao eh fortemente conexo nos vertices ativos.")
            return 1

        solver = DirectedEulerianCycle(graph)
        cycle = solver.find_cycle()

        if not cycle:
            print("Erro: nao foi possivel encontrar circuito euleriano.")
            return 1

        print("Circuito euleriano")
        print(" -> ".join(cycle))
        print()

        total_cost = solver.total_cost()
        original_cost = load_original_cost_if_available(input_path)

        if original_cost is not None:
            additional_cost = total_cost - original_cost
            print(f"Custo original: {original_cost}")
            print(f"Custo adicional (eulerizacao): {additional_cost}")
            print(f"Custo total: {total_cost}")
        else:
            print(f"Custo total: {total_cost}")

        return 0
    except Exception as exc:
        print(f"Falha na execucao: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
