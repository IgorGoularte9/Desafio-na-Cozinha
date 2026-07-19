import math


def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def vizinho_mais_proximo(origem, pontos):

    if not pontos:
        return [origem], 0.0

    restantes = list(pontos)
    rota = [origem]
    atual = origem
    distancia_total = 0.0

    while restantes:
        melhor_idx = 0
        melhor_dist = distancia(atual, restantes[0]["coord"])
        for i in range(1, len(restantes)):
            d = distancia(atual, restantes[i]["coord"])
            if d < melhor_dist:
                melhor_dist = d
                melhor_idx = i

        escolhido = restantes.pop(melhor_idx)
        rota.append(escolhido)
        distancia_total += melhor_dist
        atual = escolhido["coord"]

    # Retorno ao restaurante
    distancia_total += distancia(atual, origem)
    rota.append({"id": "RETORNO", "nome": "Volta ao Restaurante", "coord": origem})
    return rota, distancia_total


def gerar_pontos_entrega(quantidade=8):
    """Gera endereços de entrega simulados ao redor do restaurante."""
    # Coordenadas fixas (seed manual) para demonstração previsível na apresentação
    coordenadas = [
        (2.0, 5.0), (4.5, 1.0), (7.0, 3.5), (1.5, 8.0),
        (6.0, 7.0), (9.0, 2.0), (3.0, 3.0), (8.0, 6.5),
        (5.0, 9.0), (0.5, 2.5), (7.5, 8.0), (4.0, 4.5)
    ]
    pontos = []
    for i in range(min(quantidade, len(coordenadas))):
        x, y = coordenadas[i]
        pontos.append({
            "id": f"E{i + 1}",
            "nome": f"Cliente {i + 1} (pedido #{100 + i})",
            "coord": (x, y)
        })
    return pontos
