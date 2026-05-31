import sys
import heapq


def solve(input_data: str) -> str:
    """
    Codeforces 449B - Jzzhu and Cities.

    --- Modelagem como grafo ---
    Vertices : as n cidades. Origem s = capital = cidade 1.
    Arestas  : estradas (u, v, x) bidirecionais, peso x >= 1;
               rotas de trem ligando a capital 1 a uma cidade c com peso y.
    Pergunta : maior numero de rotas de trem que podem ser FECHADAS sem alterar
               a distancia minima de NENHUMA cidade ate a capital.

    O grafo e nao-direcionado, logo a distancia "de toda cidade ate a capital"
    e a "da capital ate toda cidade": basta UM Dijkstra a partir do vertice 1.
    Pesos nao-negativos => Dijkstra e aplicavel.

    --- Estrategia (Dijkstra + analise de arestas redundantes) ---
    1) Por cidade so a MENOR rota-trem pode ser util; as demais ja sao fechadas.
    2) Dijkstra sobre estradas + a menor rota-trem de cada cidade.
    3) Para cada cidade c com rota-trem (a menor, de peso y = best_train[c]):
         y > dist[c]                          -> trem nao atinge o minimo: fecha.
         y == dist[c] e alguma ESTRADA atinge dist[c]
                                              -> trem redundante: fecha.
         y == dist[c] e nenhuma estrada atinge dist[c]
                                              -> trem e a unica forma: mantem.

    Implementacao: grafo em formato CSR (arrays planos) e fila de prioridade com
    chaves inteiras (dist << shift | vertice) para Dijkstra rapido em Python.
    """
    data = input_data.split()
    pos = 0
    n = int(data[pos]); m = int(data[pos + 1]); k = int(data[pos + 2]); pos += 3

    # 1a passagem nas estradas: conta grau para montar o CSR.
    eu = [0] * m
    ev = [0] * m
    ew = [0] * m
    deg = [0] * (n + 2)
    for i in range(m):
        u = int(data[pos]); v = int(data[pos + 1]); x = int(data[pos + 2]); pos += 3
        eu[i] = u; ev[i] = v; ew[i] = x
        deg[u] += 1
        deg[v] += 1

    INF = float('inf')
    best_train = [INF] * (n + 1)
    closed = 0
    for _ in range(k):
        c = int(data[pos]); y = int(data[pos + 1]); pos += 2
        if y < best_train[c]:
            if best_train[c] != INF:
                closed += 1
            best_train[c] = y
        else:
            closed += 1

    # numero de arestas-trem reais (uma por cidade que tem trem util)
    train_cities = [c for c in range(2, n + 1) if best_train[c] != INF]
    # cada trem vira aresta bidirecional (1, c): grau +1 no 1 e +1 em c
    deg[1] += len(train_cities)
    for c in train_cities:
        deg[c] += 1

    # offsets do CSR
    start = [0] * (n + 2)
    for v in range(1, n + 1):
        start[v + 1] = start[v] + deg[v]
    total = start[n + 1]

    to = [0] * total
    wt = [0] * total
    is_road = bytearray(total)  # 1 se a aresta e estrada, 0 se e trem
    fill = start[:]  # cursor de preenchimento por vertice

    for i in range(m):
        u = eu[i]; v = ev[i]; x = ew[i]
        p = fill[u]; to[p] = v; wt[p] = x; is_road[p] = 1; fill[u] = p + 1
        p = fill[v]; to[p] = u; wt[p] = x; is_road[p] = 1; fill[v] = p + 1
    for c in train_cities:
        y = best_train[c]
        p = fill[1]; to[p] = c; wt[p] = y; is_road[p] = 0; fill[1] = p + 1
        p = fill[c]; to[p] = 1; wt[p] = y; is_road[p] = 0; fill[c] = p + 1

    # Dijkstra com chaves inteiras: chave = dist * SHIFT + vertice.
    SHIFT = n + 1
    dist = [INF] * (n + 1)
    dist[1] = 0
    pq = [1]  # chave de (dist=0, v=1) = 0*SHIFT + 1
    push = heapq.heappush
    pop = heapq.heappop
    while pq:
        key = pop(pq)
        v = key % SHIFT
        d = key // SHIFT
        if d > dist[v]:
            continue
        s = start[v]; e = start[v + 1]
        for p in range(s, e):
            w = to[p]
            nd = d + wt[p]
            if nd < dist[w]:
                dist[w] = nd
                push(pq, nd * SHIFT + w)

    # Conta quantas ESTRADAS realizam a distancia minima de cada vertice.
    cnt_road = [0] * (n + 1)
    for v in range(1, n + 1):
        dv = dist[v]
        s = start[v]; e = start[v + 1]
        for p in range(s, e):
            if is_road[p] and dv + wt[p] == dist[to[p]]:
                cnt_road[to[p]] += 1

    # Decide cada rota-trem mantida (a menor de cada cidade).
    for c in train_cities:
        y = best_train[c]
        if y > dist[c] or cnt_road[c] > 0:
            closed += 1
        # senao: trem e a unica forma de manter dist[c] -> mantem.

    return str(closed) + "\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
