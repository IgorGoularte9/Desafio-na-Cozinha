import hashlib

class Receita:
    """
    Classe que representa uma receita no sistema.
    Armazena todos os dados e gera uma assinatura digital (hash) para garantir a integridade.
    """
    def __init__(self, id_receita, nome, categoria, ingredientes, tempo_preparo, custo, avaliacao):
        self.id = id_receita
        self.nome = nome
        self.categoria = categoria
        self.ingredientes = ingredientes
        self.tempo_preparo = tempo_preparo
        self.custo = custo
        self.avaliacao = avaliacao

        # Gera o identificador original assim que a receita é criada
        self.hash_integridade = self.gerar_hash()

    def gerar_hash(self):
        """
        Cria uma assinatura digital única baseada no conteúdo da receita.
        O ID foi removido para que possamos detectar duplicatas exatas de conteúdo
        que estejam cadastradas sob IDs diferentes.
        """
        conteudo = f"{self.nome}{self.categoria}{''.join(self.ingredientes)}{self.tempo_preparo}{self.custo}{self.avaliacao}"
        return hashlib.sha256(conteudo.encode('utf-8')).hexdigest()

    def verificar_integridade(self):
        """
        Modo Investigação: Verifica se a receita foi adulterada comparando o hash atual com o original.
        """
        hash_atual = self.gerar_hash()
        return hash_atual == self.hash_integridade