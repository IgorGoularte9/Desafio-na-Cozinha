import json
import random
from receita import Receita

def carregar_dados_json(caminho_arquivo, limite=100):
    """Lê o arquivo JSON e transforma os dicionários em objetos da classe Receita."""
    receitas_carregadas = []
    random.seed(42)

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

            for item in dados[:limite]: 
                id_receita = item['id']
                categoria = item['cuisine']
                ingredientes = item['ingredients']

                nome = f"{categoria.capitalize()} Prato {id_receita}"
                tempo_preparo = random.randint(15, 120) 
                custo = round(random.uniform(20.0, 150.0), 2) 
                avaliacao = round(random.uniform(3.0, 5.0), 1) 

                nova_receita = Receita(id_receita, nome, categoria, ingredientes, tempo_preparo, custo, avaliacao)
                receitas_carregadas.append(nova_receita)

        # Forçando duplicata para testar o Modo Investigação
        if receitas_carregadas:
            molde = receitas_carregadas[0]
            receita_duplicada = Receita(
                id_receita=999999, 
                nome=molde.nome + " (CLONE)",   
                categoria=molde.categoria,
                ingredientes=molde.ingredientes.copy(),
                tempo_preparo=molde.tempo_preparo,
                custo=molde.custo,
                avaliacao=molde.avaliacao
            )
            receitas_carregadas.append(receita_duplicada)

    except FileNotFoundError:
        print(f"[ERRO] O arquivo {caminho_arquivo} não foi encontrado na mesma pasta.")

    return receitas_carregadas