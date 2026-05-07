# Trabalho Pratico 1 - Grafos (DFS e BFS)

Implementacao em Python para o grafo dos estados do Nordeste.

## Estrutura do projeto

```text
trabalho-bfs-dfs/
├── README.md
├── dados/
│   └── nordeste.txt
└── src/
    ├── main.py
    ├── graph.py
    ├── depth_first_paths.py
    └── breadth_first_paths.py
```

## Como executar

1. Entre na pasta do projeto.
2. Execute:

```bash
python3 src/main.py
```

3. Informe origem (`X`) e destino (`Y`) pelas siglas dos estados:
   - `AL, BA, CE, MA, PB, PE, PI, RN, SE`

## Modelagem do grafo

Mapeamento de vertices em ordem alfabetica (exigencia do enunciado):

- `0: AL`
- `1: BA`
- `2: CE`
- `3: MA`
- `4: PB`
- `5: PE`
- `6: PI`
- `7: RN`
- `8: SE`

Arestas em ordem crescente (`v w`) no arquivo `dados/nordeste.txt`.

## Vídeo
https://drive.google.com/file/d/1rDaZFnKcF8r3mN7vOo0jVGmyfGJ49nys/view?usp=drive_link
