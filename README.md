# 🍳 Desafio na Cozinha

Projeto desenvolvido para a disciplina de Algoritmos e Estruturas de Dados II.

O sistema simula um ambiente inteligente de gerenciamento de receitas para um restaurante, utilizando estruturas de dados implementadas do zero para garantir buscas rápidas, organização eficiente e detecção de inconsistências nas receitas cadastradas.

---

# 👨‍🍳 Objetivo do Projeto

O projeto foi desenvolvido com o objetivo de auxiliar o chef Erick Jacquin na organização de receitas culinárias, permitindo:

- Busca rápida de receitas
- Organização eficiente dos ingredientes
- Recomendação inteligente de cardápios
- Verificação de integridade das receitas
- Detecção de sabotagens e duplicatas

Além disso, o sistema demonstra a aplicação prática de estruturas de dados e algoritmos estudados na disciplina.

---

# 🧠 Estruturas de Dados Utilizadas

O projeto implementa do zero as seguintes estruturas obrigatórias:

## ✅ Tabela Hash

Utilizada para:

- Armazenamento principal das receitas
- Busca rápida por ID
- Indexação por categorias
- Indexação por ingredientes
- Verificação de duplicatas no Modo Investigação

### Implementação:
A tabela hash foi implementada utilizando:

- Encadeamento (chaining)
- Função hash personalizada
- Suporte para chaves numéricas e textuais

---

## ✅ Árvore Trie

Utilizada para:

- Busca eficiente por prefixo do nome das receitas

### Exemplo:

Buscar:

```txt
Greek
```

Retorna:

```txt
Greek Prato 12
Greek Prato 27
Greek Prato 88
```

A Trie permite buscas rápidas mesmo com grande volume de dados.

---

## ✅ Algoritmo Guloso

Utilizado no:

- Modo Chef
- Recomendação de cardápios

### Estratégias implementadas:

#### 🍽️ Menu Econômico
Seleciona receitas com melhor relação:

```txt
Avaliação / Custo
```

#### ⚡ Menu Flash
Seleciona receitas com melhor relação:

```txt
Avaliação / Tempo de preparo
```

O algoritmo escolhe receitas enquanto respeita:

- orçamento máximo
ou
- tempo máximo disponível

---

# 📦 Fonte de Dados

Os dados foram carregados a partir de um arquivo JSON contendo receitas culinárias.

## Informações utilizadas:

Cada receita possui:

- ID
- Categoria
- Ingredientes

---

# ⚙️ Funcionalidades do Sistema

# 📖 Módulo 1 — Livro de Receitas

Responsável por:

- Carregar receitas do arquivo JSON
- Criar objetos Receita
- Armazenar receitas no sistema

---

# 🔍 Módulo 2 — Consulta Rápida

Permite:

- Buscar receitas por nome
- Buscar por prefixo
- Buscar por categoria
- Buscar por ingrediente
- Buscar por ID

---

# 🧂 Módulo 3 — Organização dos Ingredientes

Relaciona ingredientes às receitas cadastradas utilizando Tabela Hash.

Permite encontrar rapidamente receitas contendo determinado ingrediente.

---

# 👨‍🍳 Modo Chef

Sistema de recomendação automática de cardápios.

## Funcionalidades:

- Menu econômico
- Menu rápido
- Restrições de orçamento
- Restrições de tempo
- Priorização por avaliação

---

# 🕵️ Modo Investigação

Responsável por detectar:

- Alterações indevidas
- Receitas adulteradas
- Duplicatas
- Inconsistências

---

# 🔐 Verificação de Integridade

Cada receita possui um identificador único gerado utilizando:

```python
hashlib.sha256()
```

O hash é baseado em:

- Nome
- Categoria
- Ingredientes
- Tempo
- Custo
- Avaliação

Quando uma receita é modificada, o sistema detecta automaticamente a alteração.

---

# 💣 Simulador de Sabotagem

O sistema possui uma funcionalidade para testar a auditoria.

Ela altera:

- Ingredientes
- Custos

Após isso, o Modo Investigação consegue identificar a corrupção dos dados.

---

# ▶️ Como Executar

## 1. Instale o Python

Versão recomendada:

```txt
Python 3.10+
```

---

## 2. Coloque os arquivos na mesma pasta

Arquivos necessários:

```txt
arquivo ......
train.json
```

---

## 3. Execute o programa

No terminal:

```bash
python main.py
```

---

# 🧪 Exemplo de Uso

Ao iniciar o sistema, será exibido o menu principal:

```txt
1. Consulta Rápida
2. Modo Chef
3. Modo Investigação
4. Simular Sabotagem
0. Sair
```

---

# 📚 Bibliotecas Utilizadas

Bibliotecas padrão do Python:

```python
json
random
hashlib
```

Nenhuma biblioteca externa foi utilizada para substituir as estruturas principais exigidas pelo trabalho.

---

# 👥 Integrantes

- Igor Pereira, Rogerio Barros

---
