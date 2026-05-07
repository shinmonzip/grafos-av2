# T6 - Identificação de Isomorfismo em Árvores

Implementação em **Python** do Trabalho Prático 6 da disciplina
**Resolução de Problemas com Grafos**.

## Estrutura

```text
T6/
├── README.md
├── T6.md
├── ROTEIRO.md
├── dados/
│   ├── invalid-ciclo3.txt
│   ├── iso-path4-a.txt
│   ├── iso-path4-b.txt
│   ├── nao-iso-estrela5.txt
│   ├── nao-iso-path5.txt
│   ├── unico-centro-a.txt
│   └── unico-centro-b.txt
└── src/
    ├── graph.py
    ├── tree_isomorphism.py
    └── main.py
```

## Requisitos

- Python 3.6 ou superior (sem dependências externas)

## Execução

Execute sempre a partir da **raiz do projeto**:

```bash
python3 src/main.py <arquivo1> <arquivo2>
```

### Fixtures de teste

```bash
python3 src/main.py dados/iso-path4-a.txt dados/iso-path4-b.txt
python3 src/main.py dados/nao-iso-path5.txt dados/nao-iso-estrela5.txt
python3 src/main.py dados/unico-centro-a.txt dados/unico-centro-b.txt
python3 src/main.py dados/invalid-ciclo3.txt dados/iso-path4-a.txt
```

## Vídeo

Parte 1: https://drive.google.com/file/d/15aj0-ETncOLYOv-ADStiNKpzQs7Dn3q6/view?usp=drive_link
Parte 2: https://drive.google.com/file/d/1YKr41VI9oGSC3yQxtKkmqzqJRo2T-qn1/view?usp=drive_link
