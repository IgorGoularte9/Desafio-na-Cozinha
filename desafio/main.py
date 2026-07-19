from tabela_hash import TabelaHash
from arvore_trie import ArvoreTrie
from carregador import carregar_dados_json
from algoritmo_guloso import recomendar_menu_guloso
from menu_vip import otimizar_menu_vip
from oficina_producao import montar_oficina_producao, injetar_ciclo_invalido
from rede_logistica import (
    criar_rede_regioes,
    arvore_geradora_minima,
    dijkstra,
    criar_rede_capacidade,
)
from rota_entregas import vizinho_mais_proximo, gerar_pontos_entrega


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
    print("\n" + "=" * 60)
    print(" 🍳 SISTEMA DE GERENCIAMENTO: DESAFIO NA COZINHA ")
    print("=" * 60)
    print("1.  Modo Consulta Rápida (Por Nome, Categoria, Ingrediente ou ID)")
    print("2.  Modo Chef (Sugerir cardápio por orçamento ou tempo)")
    print("3.  Modo Investigação (Auditar e buscar inconsistências)")
    print("4.  Simular Sabotagem (Alterar dados de uma receita)")
    print("5.  Oficina de Produção (Dependências entre preparos)")
    print("6.  Modo Logística (Rotas, rede e capacidade de entrega)")
    print("7.  Planejamento de Entregas (Otimizar rota do entregador)")
    print("0.  Sair do Sistema")
    print("=" * 60)


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

    grafo_producao = montar_oficina_producao(receitas)
    rede_regioes = criar_rede_regioes()

    print(f"[{len(receitas)} receitas carregadas e indexadas!]")
    print(f"[{len(grafo_producao.adjacencia)} preparos cadastrados na oficina]")
    print(f"[Rede logística pronta: {rede_regioes.num_vertices()} pontos e {rede_regioes.num_arestas()} conexões]")

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
            print("a. Menu Econômico (Melhor custo-benefício dentro de um orçamento)")
            print("b. Menu Flash (Pratos mais bem avaliados em menor tempo)")
            print("c. Menu Degustação VIP (Melhor combinação sob restrições)")
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

            elif sub_op == 'c':
                print("\n--- MENU DEGUSTAÇÃO VIP ---")
                print("O que você quer priorizar?")
                print("1. Maior lucro estimado")
                print("2. Melhor avaliação")
                crit = input("Escolha (1/2): ").strip()
                criterio = "avaliacao" if crit == "2" else "lucro"

                try:
                    raw_orc = input("Orçamento máximo em R$ (Enter para ignorar): ").strip()
                    raw_tmp = input("Tempo máximo em minutos (Enter para ignorar): ").strip()
                    orcamento = float(raw_orc) if raw_orc else None
                    tempo = int(raw_tmp) if raw_tmp else None

                    if orcamento is None and tempo is None:
                        print("[!] Informe ao menos uma restrição (orçamento ou tempo).")
                        continue

                    menu, custo, tempo_tot, lucro = otimizar_menu_vip(
                        receitas, orcamento_max=orcamento, tempo_max=tempo, criterio=criterio
                    )

                    print("\n--- Menu VIP Recomendado ---")
                    if not menu:
                        print("Nenhuma combinação válida encontrada com as restrições informadas.")
                    else:
                        for prato in menu:
                            print(
                                f" -> {prato.nome} | Nota: {prato.avaliacao} | "
                                f"Custo: R$ {prato.custo:.2f} | Tempo: {prato.tempo_preparo} min"
                            )
                        print("-" * 65)
                        print(f"Pratos: {len(menu)} | Custo: R$ {custo:.2f} | Tempo: {tempo_tot} min | Lucro est.: R$ {lucro:.2f}")
                except ValueError:
                    print("[!] Erro: valores numéricos inválidos.")
            else:
                print("Opção inválida.")

        elif opcao == '3':
            print("\n--- MODO INVESTIGAÇÃO ---")
            print("a. Verificar integridade de uma receita específica (ID)")
            print("b. Varredura completa (Buscar inconsistências e duplicatas)")
            print("c. Auditar dependências de produção")
            print("d. Verificar se a rede de entregas está conectada")
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

            elif sub_op == 'c':
                print("\nAuditando dependências da Oficina de Produção...")
                if grafo_producao.existe_erro_dependencia():
                    print("[!] ERRO: existe ciclo nas dependências — sequência de produção impossível.")
                else:
                    ordem, _ = grafo_producao.ordenacao_topologica()
                    print("Status: OK — nenhuma dependência circular detectada.")
                    print(f"Sequência viável possui {len(ordem)} etapas.")

            elif sub_op == 'd':
                print("\nVerificando se a rede de entregas está toda conectada...")
                mst, custo = arvore_geradora_minima(rede_regioes)
                esperado = rede_regioes.num_vertices() - 1
                if len(mst) < esperado:
                    print(f"[!] Problema: a rede está desconexa ({len(mst)} conexões, esperado {esperado}).")
                    print("Existem regiões isoladas que não conseguem ser interligadas.")
                else:
                    print(f"Status: OK — rede conectada com {len(mst)} conexões | custo total: {custo}")
            else:
                print("Opção inválida.")

        elif opcao == '4':
            print("\n--- SIMULADOR DE SABOTAGEM ESPECÍFICA ---")
            print("a. Sabotar uma receita (custo/ingredientes)")
            print("b. Sabotar dependências (criar ciclo inválido)")
            sub_op = input("Escolha: ").lower()

            if sub_op == 'a':
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

            elif sub_op == 'b':
                injetar_ciclo_invalido(grafo_producao)
                print("Ciclo inválido injetado entre BASE_CALDO, BASE_MOLHO e BASE_CREME.")
                print("-> Vá na opção 3 (subopção C) ou na opção 5 para detectar o erro.")
            else:
                print("Opção inválida.")

        elif opcao == '5':
            print("\n--- OFICINA DE PRODUÇÃO ---")
            print("a. Sequência correta para produzir o menu do dia")
            print("b. Existe algum erro de dependência?")
            print("c. Quais preparos precisam ser concluídos antes da receita X?")
            sub_op = input("Escolha: ").lower()

            if sub_op == 'a':
                ordem, tem_ciclo = grafo_producao.ordenacao_topologica()
                if tem_ciclo:
                    print("[!] Impossível gerar sequência: há ciclo de dependências.")
                else:
                    print("\nOrdem válida de produção:")
                    for i, id_p in enumerate(ordem[:25], 1):
                        print(f"  {i:02d}. {grafo_producao.nome(id_p)}")
                    if len(ordem) > 25:
                        print(f"  ... e mais {len(ordem) - 25} etapas.")
                    print(f"\nTotal de etapas: {len(ordem)}")

            elif sub_op == 'b':
                if grafo_producao.existe_erro_dependencia():
                    print("[!] SIM — há erro de dependência (ciclo detectado).")
                else:
                    print("NÃO — o grafo de dependências está acíclico e executável.")

            elif sub_op == 'c':
                try:
                    id_rec = int(input("Digite o ID da receita: "))
                    chave = f"REC_{id_rec}"
                    if chave not in grafo_producao.adjacencia:
                        print("[!] Receita não possui preparo cadastrado na oficina (use IDs das primeiras 40).")
                    else:
                        prereqs = grafo_producao.pre_requisitos(chave)
                        print(f"\nPreparos necessários antes de '{grafo_producao.nome(chave)}':")
                        if not prereqs:
                            print("  (nenhuma dependência)")
                        for pid in prereqs:
                            print(f"  -> {grafo_producao.nome(pid)}")
                except ValueError:
                    print("[!] ID inválido.")
            else:
                print("Opção inválida.")

        elif opcao == '6':
            print("\n--- MODO LOGÍSTICA ---")
            print("a. Menor rede de conexões entre os pontos operacionais")
            print("b. Caminho mais curto entre dois pontos")
            print("c. Capacidade máxima de atendimento")
            print("d. Ver tamanho da rede (vértices e arestas)")
            sub_op = input("Escolha: ").lower()

            if sub_op == 'a':
                mst, custo = arvore_geradora_minima(rede_regioes)
                print("\nMenor rede para interligar todos os pontos operacionais:")
                for u, v, peso in mst[:20]:
                    print(f"  {rede_regioes.nomes[u]} -- {rede_regioes.nomes[v]} | custo {peso}")
                if len(mst) > 20:
                    print(f"  ... e mais {len(mst) - 20} conexões.")
                print(f"\nConexões usadas: {len(mst)} | Custo total da infraestrutura: {custo}")

            elif sub_op == 'b':
                print("Exemplos: R0 (restaurante), C1..C4 (cozinhas), P1..P10 (pontos), B1..B20 (bairros)")
                origem = input("Origem: ").strip().upper()
                destino = input("Destino: ").strip().upper()
                caminho, dist = dijkstra(rede_regioes, origem, destino)
                if not caminho:
                    print("[!] Não existe caminho entre os pontos informados.")
                else:
                    nomes = " -> ".join(rede_regioes.nomes.get(v, v) for v in caminho)
                    print(f"\nRota: {nomes}")
                    print(f"Custo operacional: {dist}")

            elif sub_op == 'c':
                try:
                    n_coz = int(input("Nº de cozinhas (ex: 3): ") or "3")
                    ped = int(input("Capacidade por cozinha (ex: 4): ") or "4")
                    n_ent = int(input("Nº de entregadores (ex: 5): ") or "5")
                    rede, fonte, sumidouro = criar_rede_capacidade(n_coz, ped, n_ent)
                    fluxo = rede.fluxo_maximo(fonte, sumidouro)
                    print(f"\nCapacidade máxima de pedidos simultâneos: {fluxo}")
                    print(f"Limite de produção: {n_coz * ped} | Limite de entrega: {n_ent * 2}")
                    if fluxo < n_coz * ped:
                        print("[!] Gargalo: entregadores ou conexões limitam a operação.")
                    else:
                        print("Produção e entrega estão equilibradas neste cenário.")
                except ValueError:
                    print("[!] Valores inválidos.")

            elif sub_op == 'd':
                print(f"Pontos: {rede_regioes.num_vertices()} | Conexões: {rede_regioes.num_arestas()}")
            else:
                print("Opção inválida.")

        elif opcao == '7':
            print("\n--- PLANEJAMENTO DE ENTREGAS ---")
            try:
                qtd = int(input("Quantas entregas nesta viagem? (2 a 12, padrão 8): ") or "8")
                qtd = max(2, min(12, qtd))
            except ValueError:
                qtd = 8

            origem = (0.0, 0.0)
            pontos = gerar_pontos_entrega(qtd)
            rota, dist_total = vizinho_mais_proximo(origem, pontos)

            print("\nRota sugerida para o entregador:")
            print("  00. Restaurante Central (0.0, 0.0)")
            passo = 1
            for item in rota[1:]:
                if isinstance(item, dict):
                    x, y = item["coord"]
                    print(f"  {passo:02d}. {item['nome']} em ({x:.1f}, {y:.1f})")
                    passo += 1
            print("-" * 65)
            print(f"Distância total percorrida (ida + volta): {dist_total:.2f} unidades")
            print("O entregador sempre segue para o endereço mais próximo ainda pendente.")

        elif opcao == '0':
            print("\nEncerrando o sistema. Obrigado por ajudar o Jacquin!")
            break
        else:
            print("\n[!] Opção inválida. Escolha um número de 0 a 7.")


if __name__ == "__main__":
    iniciar_sistema()
