<img src="imgs/UNIFOR_logo1b.png" width="400">

# T4 - Execucao

## Requisitos

- Java JDK 8+ instalado
- Terminal aberto na raiz do projeto (pasta que contém `src/` e `dados/`)

## Compilacao

Entre na pasta `src` e compile os arquivos:

```bash
cd src
javac Main.java Point.java Tour.java TSPVisualizer.java In.java StdIn.java StdOut.java StdDraw.java
```

## Execucao principal

Ainda na pasta `src`, execute com a instancia oficial:

```bash
java Main ../dados/usa13509.txt
```

Para depuracao rapida, use a instancia pequena:

```bash
java Main ../dados/tsp10.txt
```

## Abrir apenas o visualizador

```bash
java TSPVisualizer ../dados/tsp10.txt
```

## Observacao sobre caminhos (macOS e Windows)

Os comandos usam caminhos relativos, sem dependencia de caminho absoluto da
maquina local. Se preferir no Windows, tambem funciona usar barra invertida:

```bat
java Main ..\dados\usa13509.txt
```
