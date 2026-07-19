# Desafio na Cozinha

Projeto desenvolvido para a disciplina de Algoritmos e Estruturas de Dados II (Trabalho 1 + Trabalho 2).

O sistema simula um ambiente inteligente de gerenciamento de receitas e operações de um restaurante, utilizando estruturas de dados e algoritmos implementados do zero.

---

# Objetivo do Projeto

Auxiliar o chef Erick Jacquin na organização de receitas e, no T2, na logística operacional do restaurante:

- Busca rápida de receitas
- Organização eficiente dos ingredientes
- Recomendação inteligente de cardápios
- Verificação de integridade das receitas
- Dependências de produção (Oficina)
- Otimização de menus VIP
- Rede logística de delivery
- Planejamento inteligente de rotas de entrega

---

# Estruturas e Algoritmos

## T1 — Estruturas obrigatórias

### Tabela Hash
- Armazenamento principal das receitas
- Indexação por categorias e ingredientes
- Detecção de duplicatas no Modo Investigação
- Encadeamento (chaining) + função hash própria

### Árvore Trie
- Busca por prefixo no nome das receitas

### Algoritmo Guloso
- Menu Econômico: maximiza `avaliação / custo`
- Menu Flash: maximiza `avaliação / tempo`

### Integridade (SHA-256)
- Cada receita possui assinatura digital do conteúdo
- Detecta adulterações e duplicatas

## T2 — Novos módulos

### Módulo 5 — Oficina de Produção
- **Estrutura:** grafo dirigido (lista de adjacência)
- **Algoritmo:** Ordenação Topológica (Kahn)
- Detecta ciclos de dependência e gera ordem válida de preparo
- Complexidade: O(V + E)

### Módulo 6 — Menu Degustação VIP
- **Algoritmo:** Programação Dinâmica (Mochila 0/1)
- Maximiza lucro estimado ou avaliação sob orçamento/tempo
- Complexidade: O(n · W), onde W é a capacidade (orçamento em centavos ou minutos)

### Módulo 7 — Pesadelo Logístico
- **Estrutura:** grafo ponderado não-dirigido
- **Kruskal + Union-Find:** Árvore Geradora Mínima (menor rede de conexões)
- **Dijkstra:** caminho operacional de menor custo
- **Edmonds-Karp:** fluxo máximo (capacidade de atendimento)
- Rede gerada: **35 vértices** e **117 arestas** (acima do mínimo 30/50)

### Módulo 8 — Laboratório de Inovação do Chef
**Desafio escolhido:** Planejamento Inteligente de Entregas

- **Algoritmo:** Heurística do Vizinho Mais Próximo (aproximação do Caixeiro Viajante)
- Em cada passo, o entregador vai ao endereço válido mais próximo da posição atual
- Garante rota rápida sem explorar todas as permutações (n!)
- Complexidade: O(n²)
- Limitação: não garante ótimo global; melhorias possíveis: 2-opt, Christofides, etc.

---

# Como Executar

```bash
cd desafio
python main.py
```

Python 3.10+ recomendado. Apenas bibliotecas padrão (`json`, `random`, `hashlib`, `math`).

---

# Menu do Sistema

```txt
1. Modo Consulta Rápida (T1)
2. Modo Chef — Guloso + Menu VIP / PD (T1 + T2 M6)
3. Modo Investigação (T1 + T2)
4. Simular Sabotagem (T1 + ciclo de dependências)
5. Oficina de Produção — Dependências (T2 M5)
6. Modo Logística — Rede, MST, Fluxo (T2 M7)
7. Planejamento de Entregas — Vizinho Mais Próximo (T2 M8)
0. Sair
```

---

# Arquivos

```txt
desafio/
  main.py                 # Interface e integração dos modos
  receita.py              # Modelo + hash de integridade
  carregador.py           # Leitura do train.json
  tabela_hash.py          # Tabela Hash
  arvore_trie.py          # Trie
  algoritmo_guloso.py     # Menus guloso (T1)
  grafo_dependencias.py   # Grafo + Kahn (M5)
  oficina_producao.py     # Cadastro de dependências
  menu_vip.py             # Mochila 0/1 (M6)
  rede_logistica.py       # MST, Dijkstra, Fluxo (M7)
  rota_entregas.py        # Vizinho Mais Próximo (M8)
  train.json              # Base de receitas
```

---

# Justificativa das escolhas (resumo)

| Módulo | Problema | Por que essa solução |
|--------|----------|----------------------|
| M5 | Ordem de preparo com dependências | DAG + Kahn detecta ciclos e produz ordem linear |
| M6 | Melhor menu sob restrições | PD da mochila encontra ótimo (ao contrário do guloso do T1) |
| M7 | Infraestrutura e capacidade | MST minimiza custo de conexão; fluxo modela gargalos |
| M8 | Rota de várias entregas | Vizinho mais próximo é rápido e suficiente para delivery em tempo real |

---

# Integrantes

- Igor Pereira, Rogerio Barros
