class GrafoNaoDirecionado:
    """Grafo ponderado não-dirigido com lista de adjacência."""

    def __init__(self):
        self.adjacencia = {}
        self.nomes = {}

    def adicionar_vertice(self, id_v, nome=""):
        if id_v not in self.adjacencia:
            self.adjacencia[id_v] = []
        self.nomes[id_v] = nome or str(id_v)

    def adicionar_aresta(self, u, v, peso):
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)
        self.adjacencia[u].append((v, peso))
        self.adjacencia[v].append((u, peso))

    def vertices(self):
        return list(self.adjacencia.keys())

    def num_vertices(self):
        return len(self.adjacencia)

    def num_arestas(self):
        total = sum(len(viz) for viz in self.adjacencia.values())
        return total // 2


class UnionFind:
    """Estrutura Union-Find (Disjoint Set) para o algoritmo de Kruskal."""

    def __init__(self, elementos):
        self.pai = {e: e for e in elementos}
        self.rank = {e: 0 for e in elementos}

    def encontrar(self, x):
        if self.pai[x] != x:
            self.pai[x] = self.encontrar(self.pai[x])
        return self.pai[x]

    def unir(self, a, b):
        ra, rb = self.encontrar(a), self.encontrar(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.pai[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.pai[rb] = ra
        else:
            self.pai[rb] = ra
            self.rank[ra] += 1
        return True


def arvore_geradora_minima(grafo):
    """
    Kruskal — menor rede de conexões entre pontos operacionais.
    Retorna lista de arestas (u, v, peso) e custo total.
    """
    arestas = []
    vistos = set()
    for u in grafo.adjacencia:
        for v, peso in grafo.adjacencia[u]:
            chave = tuple(sorted((u, v)))
            if chave not in vistos:
                vistos.add(chave)
                arestas.append((peso, u, v))

    arestas.sort()
    uf = UnionFind(grafo.vertices())
    mst = []
    custo = 0

    for peso, u, v in arestas:
        if uf.unir(u, v):
            mst.append((u, v, peso))
            custo += peso
            if len(mst) == grafo.num_vertices() - 1:
                break

    return mst, custo


def dijkstra(grafo, origem, destino):
    """Caminho de menor custo entre dois vértices."""
    if origem not in grafo.adjacencia or destino not in grafo.adjacencia:
        return [], float("inf")

    dist = {v: float("inf") for v in grafo.adjacencia}
    anterior = {v: None for v in grafo.adjacencia}
    dist[origem] = 0
    visitados = set()

    while len(visitados) < len(grafo.adjacencia):
        u = None
        melhor = float("inf")
        for v in grafo.adjacencia:
            if v not in visitados and dist[v] < melhor:
                melhor = dist[v]
                u = v
        if u is None:
            break
        visitados.add(u)
        if u == destino:
            break
        for viz, peso in grafo.adjacencia[u]:
            nova = dist[u] + peso
            if nova < dist[viz]:
                dist[viz] = nova
                anterior[viz] = u

    if dist[destino] == float("inf"):
        return [], float("inf")

    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]
    caminho.reverse()
    return caminho, dist[destino]


class RedeFluxo:
    """
    Rede de fluxo para capacidade operacional (cozinhas -> pedidos -> entregadores).
    Edmonds-Karp (Ford-Fulkerson com BFS).
    """

    def __init__(self):
        self.capacidade = {}
        self.adj = {}

    def adicionar_aresta(self, u, v, cap):
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.capacidade[(u, v)] = self.capacidade.get((u, v), 0) + cap
        self.capacidade[(v, u)] = self.capacidade.get((v, u), 0)

    def _bfs(self, fonte, sumidouro, pai):
        visitado = {fonte}
        fila = [fonte]
        while fila:
            u = fila.pop(0)
            for v in self.adj.get(u, []):
                if v not in visitado and self.capacidade.get((u, v), 0) > 0:
                    visitado.add(v)
                    pai[v] = u
                    if v == sumidouro:
                        return True
                    fila.append(v)
        return False

    def fluxo_maximo(self, fonte, sumidouro):
        pai = {}
        fluxo = 0
        while self._bfs(fonte, sumidouro, pai):
            caminho_cap = float("inf")
            v = sumidouro
            while v != fonte:
                u = pai[v]
                caminho_cap = min(caminho_cap, self.capacidade[(u, v)])
                v = u
            v = sumidouro
            while v != fonte:
                u = pai[v]
                self.capacidade[(u, v)] -= caminho_cap
                self.capacidade[(v, u)] += caminho_cap
                v = u
            fluxo += caminho_cap
            pai = {}
        return fluxo


def criar_rede_regioes():
    """
    Cria a rede logística da cidade (>= 30 vértices e >= 50 arestas).
    Vértices: restaurante central, cozinhas, pontos de retirada e bairros.
    """
    g = GrafoNaoDirecionado()

    # 1 restaurante + 4 cozinhas + 10 pontos de retirada + 20 bairros = 35 vértices
    g.adicionar_vertice("R0", "Restaurante Central")
    for i in range(1, 5):
        g.adicionar_vertice(f"C{i}", f"Cozinha Satelite {i}")
    for i in range(1, 11):
        g.adicionar_vertice(f"P{i}", f"Ponto Retirada {i}")
    for i in range(1, 21):
        g.adicionar_vertice(f"B{i}", f"Bairro {i}")

    # Conexões restaurante <-> cozinhas
    for i in range(1, 5):
        g.adicionar_aresta("R0", f"C{i}", 3 + i)

    # Cozinhas <-> pontos de retirada
    for i in range(1, 5):
        for j in range(1, 11):
            if (i + j) % 3 == 0 or j % 4 == i % 4:
                g.adicionar_aresta(f"C{i}", f"P{j}", 2 + ((i + j) % 5))

    # Pontos <-> bairros
    for j in range(1, 11):
        for k in range(1, 21):
            if (j * 2 + k) % 5 == 0 or k % 10 == j % 10:
                g.adicionar_aresta(f"P{j}", f"B{k}", 1 + ((j + k) % 7))

    # Arestas extras entre bairros vizinhos (malha urbana)
    for k in range(1, 21):
        g.adicionar_aresta(f"B{k}", f"B{(k % 20) + 1}", 2 + (k % 4))
        if k + 2 <= 20:
            g.adicionar_aresta(f"B{k}", f"B{k + 2}", 3 + (k % 3))

    return g


def criar_rede_capacidade(num_cozinhas=3, pedidos_por_cozinha=4, num_entregadores=5):
    """
    Fonte -> Cozinhas -> Pedidos -> Entregadores -> Sumidouro
    Capacidade = quantos pedidos simultâneos o sistema aguenta.
    """
    rede = RedeFluxo()
    fonte, sumidouro = "S", "T"

    for c in range(1, num_cozinhas + 1):
        rede.adicionar_aresta(fonte, f"Coz{c}", pedidos_por_cozinha)
        for p in range(1, pedidos_por_cozinha + 1):
            pedido = f"Ped{c}_{p}"
            rede.adicionar_aresta(f"Coz{c}", pedido, 1)
            for e in range(1, num_entregadores + 1):
                # Cada pedido pode ir para qualquer entregador
                if (c + p + e) % 2 == 0 or e == ((c + p) % num_entregadores) + 1:
                    rede.adicionar_aresta(pedido, f"Ent{e}", 1)

    for e in range(1, num_entregadores + 1):
        # Cada entregador aguenta no máximo 2 pedidos por vez
        rede.adicionar_aresta(f"Ent{e}", sumidouro, 2)

    return rede, fonte, sumidouro
