def _lucro_estimado(receita):
    """Valor de venda estimado a partir do custo e da avaliação."""
    valor_venda = round(receita.custo * (1.25 + receita.avaliacao / 10.0), 2)
    return valor_venda - receita.custo, valor_venda


def otimizar_menu_vip(lista_receitas, orcamento_max=None, tempo_max=None, criterio="lucro"):
    """
    Módulo 6 — Menu Degustação VIP.
    Programação Dinâmica (Mochila 0/1) para maximizar lucro ou avaliação
    respeitando orçamento e/ou tempo máximo.
    """
    if not lista_receitas:
        return [], 0.0, 0, 0.0

    # Pré-filtro pela restrição que NÃO será a dimensão da DP
    filtradas = []
    for r in lista_receitas:
        if orcamento_max is not None and tempo_max is not None:
            if r.custo > orcamento_max or r.tempo_preparo > tempo_max:
                continue
        elif orcamento_max is not None and r.custo > orcamento_max:
            continue
        elif tempo_max is not None and r.tempo_preparo > tempo_max:
            continue
        filtradas.append(r)

    if not filtradas:
        return [], 0.0, 0, 0.0

    # Dimensão da mochila: prioriza orçamento; senão tempo
    usar_orcamento = orcamento_max is not None
    if usar_orcamento:
        capacidade = int(round(orcamento_max * 100))
        pesos = [int(round(r.custo * 100)) for r in filtradas]
    else:
        capacidade = tempo_max if tempo_max is not None else sum(r.tempo_preparo for r in filtradas)
        pesos = [r.tempo_preparo for r in filtradas]

    valores = []
    for r in filtradas:
        lucro, _ = _lucro_estimado(r)
        if criterio == "avaliacao":
            valores.append(int(round(r.avaliacao * 10)))
        else:
            valores.append(int(round(lucro * 100)))

    n = len(filtradas)
    # dp[i][w] = melhor valor com os i primeiros itens e capacidade w
    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        peso = pesos[i - 1]
        val = valores[i - 1]
        for w in range(capacidade + 1):
            dp[i][w] = dp[i - 1][w]
            if peso <= w:
                candidato = dp[i - 1][w - peso] + val
                if candidato > dp[i][w]:
                    dp[i][w] = candidato

    # Reconstrução
    menu = []
    w = capacidade
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            menu.append(filtradas[i - 1])
            w -= pesos[i - 1]
    menu.reverse()

    # Se ambas as restrições existem, a DP usou orçamento; remove o que estoura tempo
    if orcamento_max is not None and tempo_max is not None:
        ajustado = []
        tempo_acc = 0
        for r in menu:
            if tempo_acc + r.tempo_preparo <= tempo_max:
                ajustado.append(r)
                tempo_acc += r.tempo_preparo
        menu = ajustado

    custo_total = sum(r.custo for r in menu)
    tempo_total = sum(r.tempo_preparo for r in menu)
    lucro_total = sum(_lucro_estimado(r)[0] for r in menu)
    return menu, custo_total, tempo_total, lucro_total
