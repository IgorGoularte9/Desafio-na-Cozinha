from grafo_dependencias import GrafoDependencias


def montar_oficina_producao(lista_receitas):
    """
    Cadastra preparações intermediárias e dependências entre receitas.
    Inclui um ciclo opcional (sabotagem de cadastro) para o Modo Investigação.
    """
    g = GrafoDependencias()

    # Bases / preparações intermediárias
    bases = [
        ("BASE_MOLHO", "Molho Base da Casa"),
        ("BASE_MASSA", "Massa Fresca"),
        ("BASE_CALDO", "Caldo de Legumes"),
        ("BASE_ARROZ", "Arroz Temperado"),
        ("BASE_CREME", "Creme de Confeitaria"),
    ]
    for id_b, nome in bases:
        g.adicionar_preparo(id_b, nome)

    # Dependências entre bases
    g.adicionar_dependencia("BASE_MOLHO", "BASE_CALDO")
    g.adicionar_dependencia("BASE_CREME", "BASE_CALDO")

    # Liga as primeiras receitas a bases (conforme categoria)
    for receita in lista_receitas[:40]:
        id_r = f"REC_{receita.id}"
        g.adicionar_preparo(id_r, receita.nome)
        cat = receita.categoria.lower()

        if cat in ("italian", "greek", "spanish", "french"):
            g.adicionar_dependencia(id_r, "BASE_MOLHO")
            g.adicionar_dependencia(id_r, "BASE_MASSA")
        elif cat in ("indian", "thai", "vietnamese", "chinese", "japanese", "korean"):
            g.adicionar_dependencia(id_r, "BASE_ARROZ")
            g.adicionar_dependencia(id_r, "BASE_CALDO")
        elif cat in ("southern_us", "british", "irish", "cajun_creole"):
            g.adicionar_dependencia(id_r, "BASE_MOLHO")
        else:
            g.adicionar_dependencia(id_r, "BASE_CALDO")

        # Sobremesas / pratos doces usam creme
        if any(ing in ("sugar", "butter", "flour", "eggs") for ing in [i.lower() for i in receita.ingredientes[:5]]):
            if "dessert" in cat or receita.id % 7 == 0:
                g.adicionar_dependencia(id_r, "BASE_CREME")

    return g


def injetar_ciclo_invalido(grafo):
    """Simula erro de cadastro criando dependência circular entre bases."""
    grafo.adicionar_dependencia("BASE_CALDO", "BASE_MOLHO")
    grafo.adicionar_dependencia("BASE_MOLHO", "BASE_CREME")
    grafo.adicionar_dependencia("BASE_CREME", "BASE_CALDO")
