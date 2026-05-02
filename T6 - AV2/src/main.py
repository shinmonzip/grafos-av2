"""
main.py  —  Ponto de entrada do Trabalho Prático 6

Uso (execute sempre a partir da raiz do projeto):
    python3 src/main.py <arquivo1> <arquivo2>

Exemplo:
    python3 src/main.py dados/iso-path4-a.txt dados/iso-path4-b.txt

O programa:
  1. Lê dois grafos não direcionados no formato algs4;
  2. Exibe a lista de adjacência de cada grafo;
  3. Valida se cada entrada representa uma árvore;
  4. Informa o(s) centro(s) de cada árvore válida;
  5. Informa a codificação canônica de cada árvore válida;
  6. Informa o veredito final de isomorfismo.
"""

import os
import sys

# Garante que o diretório src/ esteja no caminho de importação,
# independente de onde o script é chamado (macOS, Windows, Linux).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import Graph
from tree_isomorphism import TreeIsomorphism


# ------------------------------------------------------------------
# Utilitários de exibição
# ------------------------------------------------------------------

_SEP_WIDTH = 58


def _section(title):
    print()
    print("=" * _SEP_WIDTH)
    print(f"  {title}")
    print("=" * _SEP_WIDTH)


# ------------------------------------------------------------------
# Função principal
# ------------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 src/main.py <arquivo1> <arquivo2>")
        print()
        print("Exemplos:")
        print("  python3 src/main.py dados/iso-path4-a.txt dados/iso-path4-b.txt")
        print("  python3 src/main.py dados/nao-iso-path5.txt dados/nao-iso-estrela5.txt")
        print("  python3 src/main.py dados/unico-centro-a.txt dados/unico-centro-b.txt")
        print("  python3 src/main.py dados/invalid-ciclo3.txt dados/iso-path4-a.txt")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]

    # ------------------------------------------------------------------
    # 1. Leitura dos grafos
    # ------------------------------------------------------------------
    try:
        tree1 = Graph(file1)
    except Exception as exc:
        print(f"Erro ao ler '{file1}': {exc}")
        sys.exit(1)

    try:
        tree2 = Graph(file2)
    except Exception as exc:
        print(f"Erro ao ler '{file2}': {exc}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 2. Listas de adjacência
    # ------------------------------------------------------------------
    _section(f"Lista de adjacencia — Arvore 1  [{file1}]")
    print(tree1)

    _section(f"Lista de adjacencia — Arvore 2  [{file2}]")
    print(tree2)

    # ------------------------------------------------------------------
    # 3. Validação
    # ------------------------------------------------------------------
    analysis1 = TreeIsomorphism(tree1)
    analysis2 = TreeIsomorphism(tree2)

    _section("Validacao das entradas")
    print(f"  Arvore 1: {analysis1.get_validation_message()}")
    print(f"  Arvore 2: {analysis2.get_validation_message()}")

    if not analysis1.is_tree() or not analysis2.is_tree():
        print()
        print("  Comparacao abortada: entrada invalida detectada.")
        print()
        sys.exit(0)

    # Arvores com número de vértices diferentes não podem ser isomorfas
    # (isomorfismo exige bijeção entre os conjuntos de vértices)
    if tree1.V() != tree2.V():
        _section("Veredito")
        print(f"  AS ARVORES NAO SAO ISOMORFAS.")
        print(f"  (numeros de vertices diferentes: {tree1.V()} vs {tree2.V()})")
        print()
        sys.exit(0)

    # ------------------------------------------------------------------
    # 4. Centros
    # ------------------------------------------------------------------
    centers1 = analysis1.get_centers()
    centers2 = analysis2.get_centers()

    _section("Centro(s) de cada arvore")
    label1 = "unico centro" if len(centers1) == 1 else "dois centros"
    label2 = "unico centro" if len(centers2) == 1 else "dois centros"
    print(f"  Arvore 1: {centers1}  ({label1})")
    print(f"  Arvore 2: {centers2}  ({label2})")

    # ------------------------------------------------------------------
    # 5. Codificação canônica
    # ------------------------------------------------------------------
    enc1 = analysis1.get_canonical_encoding()
    enc2 = analysis2.get_canonical_encoding()

    _section("Codificacao canonica")
    print(f"  Arvore 1: {enc1}")
    print(f"  Arvore 2: {enc2}")

    # ------------------------------------------------------------------
    # 6. Veredito
    # ------------------------------------------------------------------
    _section("Veredito")
    if enc1 == enc2:
        print("  AS ARVORES SAO ISOMORFAS.")
        print("  (mesma codificacao canonica)")
    else:
        print("  AS ARVORES NAO SAO ISOMORFAS.")
        print("  (codificacoes canonicas diferentes)")
    print()


if __name__ == "__main__":
    main()
