def recomendar_menu_guloso(lista_receitas, limite_restricao, tipo_menu="economico"):
    """Cria o melhor cardápio possível sem estourar restrição (Dinheiro/Tempo)."""
    if tipo_menu == "economico":
        receitas_ordenadas = sorted(
            lista_receitas,
            key=lambda r: r.avaliacao / r.custo,
            reverse=True 
        )
    elif tipo_menu == "rapido":
        receitas_ordenadas = sorted(
            lista_receitas,
            key=lambda r: r.avaliacao / r.tempo_preparo,
            reverse=True
        )
    else:
        return [], 0

    menu_recomendado = []
    gasto_acumulado = 0.0

    for receita in receitas_ordenadas:
        peso_atual = receita.custo if tipo_menu == "economico" else receita.tempo_preparo
        if gasto_acumulado + peso_atual <= limite_restricao:
            menu_recomendado.append(receita)
            gasto_acumulado += peso_atual

    return menu_recomendado, gasto_acumulado