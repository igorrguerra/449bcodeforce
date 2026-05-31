# Trabalho Prático 2 — Caminhos Mínimos (Unidade 3)

## Problema
- **Nome:** Jzzhu and Cities
- **Plataforma:** Codeforces
- **Link:** https://codeforces.com/problemset/problem/449/B
- **Grupo:** F

## Integrantes do grupo
- *(preencher: nome — matrícula)*
- *(preencher: nome — matrícula)*
- *(preencher: nome — matrícula)*

## Linguagem utilizada
Python 3 (apenas biblioteca padrão: `sys` e `heapq`).

## Como executar
A solução lê da entrada padrão e escreve na saída padrão (formato do Codeforces).

```bash
# a partir da raiz do repositório
python3 src/main.py < dados/exemplo1.txt    # saída esperada: 2
python3 src/main.py < dados/exemplo2.txt    # saída esperada: 2
```

Ou digitando a entrada manualmente:

```bash
python3 src/main.py
```

Requisitos: Python 3.8+ (testado em 3.10+). Não há dependências externas.

## Modelagem do problema e representação adotada
O país tem `n` cidades; a capital é a cidade 1. Modelamos como um **grafo
não-direcionado ponderado**:

- **Vértices:** as `n` cidades. A origem é `s = 1` (capital).
- **Arestas de estrada:** cada estrada `(u, v, x)` é uma aresta bidirecional de
  peso `x`.
- **Rotas de trem:** cada rota liga a capital 1 a uma cidade `c` com peso `y`,
  modelada como uma aresta bidirecional `(1, c, y)`.

Como o grafo é não-direcionado, a distância mínima *de cada cidade até a
capital* é igual à distância *da capital até cada cidade*. Portanto, basta **um
único Dijkstra a partir do vértice 1**. Todos os pesos são `≥ 1` (não
negativos), o que justifica o uso de Dijkstra.

**Representação:** lista de adjacência em formato **CSR** (Compressed Sparse
Row) — arrays planos `to[]`, `wt[]` e offsets `start[]` — para reduzir o
overhead de objetos do Python em grafos grandes. Um vetor de bytes `is_road[]`
marca quais arestas são estradas (para distinguir de trens na análise final).

## Algoritmo utilizado
**Algoritmo de Dijkstra** (fonte única) com fila de prioridade mínima (`heapq`).
A lógica de inicialização de distâncias, relaxamento de arestas, seleção do
próximo vértice e a fila de prioridade foram implementadas pelo grupo, conforme
a base conceitual `algs4` (classe `DijkstraSP`). Não foi usada nenhuma
biblioteca pronta de grafos ou de caminhos mínimos.

Detalhe de implementação: a fila de prioridade armazena **chaves inteiras**
`dist * (n+1) + v`, em vez de tuplas `(dist, v)`. A comparação de inteiros é
mais barata que a de tuplas, o que acelera o Dijkstra em Python sem alterar a
ordem de processamento.

## Variação de Dijkstra usada
Não é uma variação algorítmica do Dijkstra em si: é **um Dijkstra padrão sobre o
grafo combinado (estradas + trens) seguido de uma análise de arestas
redundantes**. A pergunta do problema — quantos trens podem ser fechados sem
alterar nenhuma distância mínima — é respondida decidindo, trem a trem, se ele é
necessário:

1. **Pré-filtragem por cidade.** Para cada cidade, apenas a **menor** rota de
   trem pode ser útil (`best_train[c]`). Qualquer rota que não seja a menor da
   sua cidade já pode ser fechada de imediato.

2. **Dijkstra** sobre estradas + as menores rotas de trem incluídas como
   arestas reais.

3. **Decisão por cidade `c` com trem** (peso `y = best_train[c]`):
   - `y > dist[c]` → o trem nem atinge a distância mínima → **fecha**.
   - `y == dist[c]` e **alguma estrada** atinge `dist[c]` (existe vizinho `u`
     com `dist[u] + peso(u,c) == dist[c]`) → o trem é redundante → **fecha**.
   - `y == dist[c]` e **nenhuma estrada** atinge `dist[c]` → o trem é a única
     forma de manter a distância mínima → **mantém** (uma única rota basta;
     trens iguais adicionais para a mesma cidade já foram fechados no passo 1).

A contagem de estradas que realizam a distância mínima de cada vértice
(`cnt_road[]`) é feita em uma varredura `O(V + E)` após o Dijkstra, usando
apenas as arestas marcadas como estrada.

## Análise de complexidade
Seja `V = n`, `E = m` arestas de estrada e `k` rotas de trem.

- Construção do grafo e pré-filtragem dos trens: `O(V + E + k)`.
- Dijkstra com heap binário: `O((V + E) log V)`. As menores rotas de trem
  somam no máximo `V - 1` arestas extras, então não alteram a ordem assintótica.
- Varredura final para `cnt_road[]` e decisão dos trens: `O(V + E + k)`.

**Tempo total:** `O((V + E) log V + k)`.
**Espaço:** `O(V + E)` para o grafo (CSR) e os vetores `dist[]`, `cnt_road[]`,
`best_train[]`.

## Casos especiais tratados
- **Múltiplas estradas entre o mesmo par de cidades** e **múltiplos trens para a
  mesma cidade**: a pré-filtragem mantém a melhor de cada tipo; o Dijkstra lida
  naturalmente com arestas paralelas.
- **Empate entre trem e estrada** na distância mínima: o trem é fechado (a
  estrada já garante a distância).
- **Dois ou mais trens com o mesmo peso mínimo para uma cidade sem estrada
  equivalente**: mantém-se apenas um; os demais são fechados.
- **Pesos grandes** (`x, y ≤ 10^9`) e somas de caminho que ultrapassam 32 bits:
  Python usa inteiros de precisão arbitrária, então não há risco de overflow.
- **Conectividade garantida pelo enunciado** (toda cidade alcança a capital),
  então não há vértices inalcançáveis a tratar.

## Evidência de Accepted
Ver `evidencias/accepted.png` (substituir pelo print real da submissão aceita no
Codeforces).
