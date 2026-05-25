class NodoTrie:
    def __init__(self):
        self.filhos = {}
        self.ids_receitas = []

class ArvoreTrie:
    """Árvore Trie para buscas rápidas de texto por prefixo."""
    def __init__(self):
        self.raiz = NodoTrie()

    def inserir(self, palavra, id_receita):
        nodo_atual = self.raiz
        palavra = palavra.lower() 
        for letra in palavra:
            if letra not in nodo_atual.filhos:
                nodo_atual.filhos[letra] = NodoTrie()
            nodo_atual = nodo_atual.filhos[letra]
        if id_receita not in nodo_atual.ids_receitas:
            nodo_atual.ids_receitas.append(id_receita)

    def buscar_prefixo(self, prefixo):
        nodo_atual = self.raiz
        prefixo = prefixo.lower()
        for letra in prefixo:
            if letra not in nodo_atual.filhos:
                return [] 
            nodo_atual = nodo_atual.filhos[letra]
        return self._coletar_ids(nodo_atual)

    def _coletar_ids(self, nodo):
        ids_encontrados = list(nodo.ids_receitas)
        for filho in nodo.filhos.values():
            ids_encontrados.extend(self._coletar_ids(filho))
        return list(set(ids_encontrados))