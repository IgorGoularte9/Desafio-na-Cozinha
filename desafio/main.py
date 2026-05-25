from tabela_hash import TabelaHash
from arvore_trie import ArvoreTrie
from carregador import carregar_dados_json
from algoritmo_guloso import recomendar_menu_guloso

def varredura_investigacao(lista_receitas):
    print("\nIniciando varredura completa do sistema...")
    hash_vistos = TabelaHash(tamanho=500)
    inconsistentes = 0
    duplicadas = 0

    for r in lista_receitas:
        if not r.verificar_integridade():
            print(f"[!] INCONSISTÊNCIA DETECTADA: Receita ID {r.id} ({r.nome}) foi adulterada!")
            inconsistentes += 1

        hash_atual = r.gerar_hash()
        ids_com_mesmo_hash = hash_vistos.buscar(hash_atual)

        if ids_com_mesmo_hash:
            print(f"[!] DUPLICATA DETECTADA: Receita ID {r.id} tem o conteúdo idêntico à Receita ID {ids_com_mesmo_hash[0]}!")
            duplicadas += 1
        else:
            hash_vistos.inserir(hash_atual, r.id, permite_multiplos=True)

    print(f"\nVarredura concluída. Inconsistências: {inconsistentes} | Duplicatas: {duplicadas}")

def exibir_menu():
    print("\n" + "="*60)
    print(" 🍳 SISTEMA DE GERENCIAMENTO: DESAFIO NA COZINHA ")
    print("="*60)
    print("1.  Modo Consulta Rápida (Por Nome, Categoria, Ingrediente ou ID)")
    print("2.  Modo Chef (Sugerir cardápio por orçamento ou tempo)")
    print("3.  Modo Investigação (Auditar e buscar duplicatas)")
    print("4.  Simular Sabotagem (Alterar dados de uma receita)")
    print("0.  Sair do Sistema")
    print("="*60)

def iniciar_sistema():
    print("Inicializando o sistema e carregando banco de dados...")
    receitas = carregar_dados_json('train.json', limite=100)

    if not receitas:
        print("Sistema abortado: Sem dados para carregar.")
        return

    cofre_receitas = TabelaHash(tamanho=200)
    indice_categorias = TabelaHash(tamanho=50)
    indice_ingredientes = TabelaHash(tamanho=500)
    indice_nomes = ArvoreTrie()

    for r in receitas:
        cofre_receitas.inserir(r.id, r, permite_multiplos=False)
        indice_nomes.inserir(r.nome, r.id)
        indice_categorias.inserir(r.categoria.lower(), r.id, permite_multiplos=True)
        for ingrediente in r.ingredientes:
            ingrediente_limpo = ingrediente.lower().strip()
            indice_ingredientes.inserir(ingrediente_limpo, r.id, permite_multiplos=True)

    print(f"[{len(receitas)} receitas carregadas e indexadas em Tabelas Hash e Árvores Trie!]\n")

    while True:
        exibir_menu()
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            print("\n--- CONSULTA RÁPIDA ---")
            print("a. Buscar por Nome (Prefixo) - Usando Árvore Trie")
            print("b. Filtrar por Categoria - Usando Tabela Hash")
            print("c. Buscar por Ingrediente - Usando Tabela Hash")
            print("d. Buscar por ID único - Usando Tabela Hash")
            sub_op = input("Escolha o tipo de busca: ").lower()

            ids_encontrados = []
            if sub_op == 'a':
                prefixo = input("Digite o início do nome da receita (ex: 'Greek', 'Indian'): ")
                ids_encontrados = indice_nomes.buscar_prefixo(prefixo)
            elif sub_op == 'b':
                categoria = input("Digite a categoria (ex: 'italian', 'mexican'): ").lower()
                ids_encontrados = indice_categorias.buscar(categoria)
            elif sub_op == 'c':
                ingrediente = input("Digite o ingrediente (ex: 'salt', 'chicken'): ").lower()
                ids_encontrados = indice_ingredientes.buscar(ingrediente)
            elif sub_op == 'd':
                try:
                    id_busca = int(input("Digite o ID da receita: "))
                    rec = cofre_receitas.buscar_unico(id_busca)
                    if rec:
                        ids_encontrados = [rec.id]
                except ValueError:
                    print("[!] Erro: ID deve ser um número inteiro.")
            else:
                print("Opção inválida.")
                continue

            if not ids_encontrados:
                print("Nenhuma receita encontrada para a busca informada.")
            else:
                print(f"Foram encontradas {len(ids_encontrados)} receitas:")
                for id_rec in ids_encontrados[:10]:
                    rec = cofre_receitas.buscar_unico(id_rec)
                    if rec:
                        print(f" -> {rec.nome} (ID: {rec.id}) | Categoria: {rec.categoria} | Nota: {rec.avaliacao}")
                if len(ids_encontrados) > 10:
                    print(f"... e mais {len(ids_encontrados) - 10} ocultas.")

        elif opcao == '2':
            print("\n--- MODO CHEF ---")
            print("Qual é o seu objetivo hoje?")
            print("a.  Menu Econômico (Melhor custo-benefício dentro de um orçamento)")
            print("b.  Menu Flash (Pratos mais bem avaliados em menor tempo)")
            sub_op = input("Escolha a estratégia: ").lower()

            if sub_op == 'a':
                try:
                    orcamento = float(input("Qual o orçamento máximo? R$ "))
                    menu_escolhido, custo_final = recomendar_menu_guloso(receitas, orcamento, tipo_menu="economico")

                    print("\n--- Cardápio Recomendado (Foco: Economia e Sabor) ---")
                    for prato in menu_escolhido:
                        print(f" -> {prato.nome} | Nota: {prato.avaliacao} | Custo: R$ {prato.custo:.2f} | Tempo: {prato.tempo_preparo} min")
                    print("-" * 65)
                    print(f"Custo Total: R$ {custo_final:.2f} (Sobra no orçamento: R$ {orcamento - custo_final:.2f})")
                except ValueError:
                    print("[!] Erro: Por favor, digite um valor numérico válido.")
            
            elif sub_op == 'b':
                try:
                    tempo_max = int(input("Qual o tempo máximo total de preparo que você tem? (minutos): "))
                    menu_escolhido, tempo_final = recomendar_menu_guloso(receitas, tempo_max, tipo_menu="rapido")

                    print("\n--- Cardápio Recomendado (Foco: Rapidez e Sabor) ---")
                    for prato in menu_escolhido:
                        print(f" -> {prato.nome} | Nota: {prato.avaliacao} | Tempo: {prato.tempo_preparo} min | Custo: R$ {prato.custo:.2f}")
                    print("-" * 65)
                    print(f"Tempo Total: {tempo_final} minutos (Sobra de tempo: {tempo_max - tempo_final} min)")
                except ValueError:
                    print("[!] Erro: Por favor, digite um número inteiro válido para os minutos.")
            else:
                print("Opção inválida.")

        elif opcao == '3':
            print("\n--- MODO INVESTIGAÇÃO ---")
            print("a. Verificar integridade de uma receita específica (ID)")
            print("b. Varredura completa (Buscar Inconsistências e Duplicatas)")
            sub_op = input("Escolha a opção: ").lower()

            if sub_op == 'a':
                try:
                    id_busca = int(input("Digite o ID da receita para auditar: "))
                    receita_auditada = cofre_receitas.buscar_unico(id_busca)

                    if receita_auditada:
                        print(f"Analisando: {receita_auditada.nome}...")
                        if receita_auditada.verificar_integridade():
                            print("Status:  INTEGRIDADE CONFIRMADA. Nenhuma alteração detectada.")
                        else:
                            print("Status:  ALERTA DE SABOTAGEM! Os dados desta receita foram corrompidos.")
                    else:
                        print("[!] Receita não encontrada no cofre.")
                except ValueError:
                    print("[!] Erro: Digite um ID numérico válido.")

            elif sub_op == 'b':
                varredura_investigacao(receitas)
            else:
                print("Opção inválida.")

        elif opcao == '4':
            print("\n--- SIMULADOR DE SABOTAGEM ESPECÍFICA ---")
            try:
                id_alvo = int(input("Digite o ID da receita que deseja sabotar: "))
                receita_alvo = cofre_receitas.buscar_unico(id_alvo)

                if receita_alvo:
                    print(f"\nAlvo localizado: {receita_alvo.nome}")
                    print(f"Custo original: R$ {receita_alvo.custo:.2f}")

                    receita_alvo.custo = 9999.99
                    receita_alvo.ingredientes.append("Veneno de Rato")

                    print(" Sabotagem concluída com sucesso! (Custo e ingredientes adulterados)")
                    print(f"-> Vá na opção 3 (subopção A) e audite o ID {id_alvo} para o sistema detectar o crime.")
                else:
                    print("[!] Receita não encontrada no cofre. Tente outro ID.")
            except ValueError:
                print("[!] Erro: Digite um ID numérico válido.")

        elif opcao == '0':
            print("\nEncerrando o sistema. Obrigado por ajudar o Jacquin!")
            break
        else:
            print("\n[!] Opção inválida. Escolha um número de 0 a 4.")

if __name__ == "__main__":
    iniciar_sistema()