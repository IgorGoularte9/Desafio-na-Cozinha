class TabelaHash:
    """Implementação de Tabela Hash com método de encadeamento."""
    def __init__(self, tamanho=100):
        self.tamanho = tamanho
        self.tabela = [[] for _ in range(self.tamanho)]

    def _funcao_hash(self, chave):
        if isinstance(chave, str):
            hash_val = 0
            for char in chave:
                hash_val = (hash_val * 31 + ord(char)) % self.tamanho
            return hash_val
        return chave % self.tamanho

    def inserir(self, chave, valor, permite_multiplos=False):
        indice = self._funcao_hash(chave)
        for i, (chave_existente, valores) in enumerate(self.tabela[indice]):
            if chave_existente == chave:
                if permite_multiplos:
                    if valor not in valores:
                        valores.append(valor) 
                else:
                    self.tabela[indice][i] = (chave, [valor]) 
                return
        self.tabela[indice].append((chave, [valor]))

    def buscar(self, chave):
        indice = self._funcao_hash(chave)
        for chave_existente, valores in self.tabela[indice]:
            if chave_existente == chave:
                return valores
        return []

    def buscar_unico(self, chave):
        resultado = self.buscar(chave)
        return resultado[0] if resultado else None