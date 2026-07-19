class GrafoDependencias:
    """
    Módulo 5 — Oficina de Produção.
    Grafo dirigido: A -> B significa "A depende de B" (B deve ser feito antes de A).
    Usa lista de adjacência implementada do zero + Ordenação Topológica (Kahn).
    """

    def __init__(self):
        self.adjacencia = {}
        self.nomes = {}

    def adicionar_preparo(self, id_preparo, nome):
        if id_preparo not in self.adjacencia:
            self.adjacencia[id_preparo] = []
        self.nomes[id_preparo] = nome

    def adicionar_dependencia(self, id_origem, id_destino):
        """id_origem depende de id_destino (destino deve vir antes)."""
        if id_origem not in self.adjacencia:
            self.adjacencia[id_origem] = []
        if id_destino not in self.adjacencia:
            self.adjacencia[id_destino] = []
        if id_destino not in self.adjacencia[id_origem]:
            self.adjacencia[id_origem].append(id_destino)

    def _grau_entrada(self):
        # Se A depende de B, A precisa esperar B terminar => grau de entrada de A sobe
        grau = {v: 0 for v in self.adjacencia}
        for origem, deps in self.adjacencia.items():
            grau[origem] = len(deps)
        return grau

    def _grafo_invertido(self):
        """Converte 'A depende de B' em arestas B -> A para a ordenação."""
        invertido = {v: [] for v in self.adjacencia}
        for origem, deps in self.adjacencia.items():
            for dep in deps:
                invertido[dep].append(origem)
        return invertido

    def ordenacao_topologica(self):
        """
        Algoritmo de Kahn.
        Retorna (ordem_valida, tem_ciclo).
        """
        grau = self._grau_entrada()
        invertido = self._grafo_invertido()
        fila = [v for v in grau if grau[v] == 0]
        ordem = []

        while fila:
            atual = fila.pop(0)
            ordem.append(atual)
            for vizinho in invertido[atual]:
                grau[vizinho] -= 1
                if grau[vizinho] == 0:
                    fila.append(vizinho)

        tem_ciclo = len(ordem) != len(self.adjacencia)
        return ordem, tem_ciclo

    def existe_erro_dependencia(self):
        _, tem_ciclo = self.ordenacao_topologica()
        return tem_ciclo

    def pre_requisitos(self, id_preparo):
        """Retorna todos os preparos que precisam ser concluídos antes de id_preparo."""
        if id_preparo not in self.adjacencia:
            return []

        visitados = set()
        pilha = list(self.adjacencia[id_preparo])

        while pilha:
            atual = pilha.pop()
            if atual in visitados:
                continue
            visitados.add(atual)
            for dep in self.adjacencia.get(atual, []):
                if dep not in visitados:
                    pilha.append(dep)

        return list(visitados)

    def nome(self, id_preparo):
        return self.nomes.get(id_preparo, str(id_preparo))
