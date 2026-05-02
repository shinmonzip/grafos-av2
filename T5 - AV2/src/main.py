"""
main.py  –  Ponto de entrada do Trabalho Pratico 5.

Uso (a partir da raiz do projeto):
    python3 src/main.py dados/brasil.txt
    python3 src/main.py dados/teste-triangulo.txt
    ...
"""

import os
import sys

# Garante que os modulos graph e dsatur sejam encontrados independentemente
# de onde o script e invocado (macOS, Windows, Linux).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import Graph
from dsatur import GraphColoringDSatur

# Mapeamento obrigatorio: estados em ordem alfabetica por sigla (T5.md)
_BRAZIL_LABELS = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF",   #  0-6
    "ES", "GO", "MA", "MG", "MS", "MT", "PA",   #  7-13
    "PB", "PE", "PI", "PR", "RJ", "RN", "RO",   # 14-20
    "RR", "RS", "SC", "SE", "SP", "TO",          # 21-26
]


def _label(vertex, use_brazil):
    return _BRAZIL_LABELS[vertex] if use_brazil else str(vertex)


def _separator(char="-", width=60):
    return char * width


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 src/main.py <arquivo>")
        print("Exemplo: python3 src/main.py dados/brasil.txt")
        sys.exit(1)

    filepath = sys.argv[1]

    # Leitura do grafo ---------------------------------------------------
    with open(filepath, "r", encoding="utf-8") as f:
        graph = Graph(f)

    n = graph.V()
    is_brasil = (os.path.basename(filepath) == "brasil.txt") and n == 27
    lbl = lambda v: _label(v, is_brasil)

    print(_separator("="))
    print(f"Arquivo : {filepath}")
    print(f"Grafo   : {n} vertices, {graph.E()} arestas")
    print(_separator("="))

    # Lista de adjacencia ------------------------------------------------
    print("\nLista de adjacencia:")
    print(_separator())
    for v in range(n):
        neighbors = "  ".join(lbl(w) for w in graph.adj(v))
        print(f"  {lbl(v):4s}: {neighbors}")

    # Execucao do DSatur -------------------------------------------------
    print()
    print(_separator())
    dsatur = GraphColoringDSatur(graph)
    dsatur.color()

    # Ordem de coloracao
    order = dsatur.get_coloring_order()
    print("\nOrdem de coloracao (DSatur):")
    print("  " + " -> ".join(lbl(v) for v in order))

    # Cor de cada vertice
    print("\nCor de cada vertice:")
    print(_separator())
    for v in range(n):
        print(f"  {lbl(v):4s}: cor {dsatur.get_color(v)}")

    # Resumo
    total = dsatur.get_color_count()
    print()
    print(_separator())
    print(f"Total de cores utilizadas: {total}")

    # Validacao
    valid = dsatur.is_valid_coloring()
    status = "VALIDA  [OK]" if valid else "INVALIDA [ERRO]"
    print(f"Coloracao {status}")
    print(_separator("="))


if __name__ == "__main__":
    main()
