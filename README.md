# Trabalho 1 - Algoritmos e Estruturas de Dados II: Desafio na Cozinha

**Alunos:** Igor Pereira e Rogerio Barros

## Sobre o Projeto
Este projeto foi desenvolvido como requisito de avaliação da disciplina de Algoritmos e Estruturas de Dados II. O objetivo principal é implementar um sistema de gerenciamento de receitas culinárias que aplique, do zero, estruturas de dados avançadas e algoritmos de otimização, além de garantir a integridade dos dados armazenados contra alterações indevidas.

## Instruções de Execução
O sistema foi desenvolvido em Python. Para executá-lo corretamente:
1. Certifique-se de ter o arquivo `train.json` e o arquivo do código fonte (`aed_2.py` ou o notebook do Colab) no mesmo diretório.
2. Caso utilize o Google Colab ou Jupyter Notebook, faça o upload do arquivo `train.json` no painel de arquivos do ambiente virtual antes de rodar o código.
3. Execute o script. Um menu interativo será exibido no console do terminal, permitindo a navegação pelas opções através da digitação dos números correspondentes.

## Fonte de Dados
O sistema é populado utilizando um dataset estático no formato JSON (`train.json`), proveniente da base de dados "What's Cooking?" (disponível no Kaggle). 

**Adaptações realizadas:**
O dataset original contém apenas o ID, o tipo de culinária (utilizado aqui como categoria) e a lista de ingredientes. Como os requisitos do trabalho exigem critérios numéricos para ordenação e recomendação (como custo e tempo), o sistema foi programado para gerar dados complementares de forma dinâmica no momento do carregamento da base. Para cada receita, são gerados aleatoriamente:
* Nome (baseado na categoria e ID)
* Tempo de preparo (entre 15 e 120 minutos)
* Custo estimado (entre R$ 20,00 e R$ 150,00)
* Avaliação (entre 3.0 e 5.0)

Além disso, durante a leitura do arquivo, o código força a criação de uma receita duplicada (cópia exata de outra receita, mas com ID diferente) exclusivamente para fins de teste e validação do verificador de fraudes no Modo Investigação.

## Estruturas de Dados Implementadas

Conforme exigido nas especificações do trabalho, as estruturas centrais do sistema foram :

### 1. Tabela Hash
* **Implementação:** Tabela Hash com tratamento de colisões por encadeamento (chaining). A função de hash foi adaptada para suportar tanto chaves numéricas (IDs) quanto strings (textos).
* **Aplicações no sistema:** * **Armazenamento principal:** Guarda os objetos das receitas usando o ID como chave, permitindo acesso em tempo constante O(1).
  * **Índices invertidos:** Foram criadas tabelas auxiliares para mapear Categorias e Ingredientes. A chave é a string (ex: "salt") e o valor é uma lista contendo os IDs de todas as receitas que possuem aquele atributo.
  * **Verificação de duplicatas:** Utilizada no Modo Investigação para armazenar as assinaturas digitais (hashes criptográficos) e identificar se uma mesma receita foi cadastrada com IDs diferentes.

### 2. Árvore Trie (Árvore de Prefixos)
* **Implementação:** Cada nó da árvore guarda um caractere e uma lista de referências (IDs) para as receitas que terminam ou passam por aquele caminho.
* **Aplicação no sistema:** Utilizada no Modo de Consulta Rápida para realizar a busca de receitas por nome ou prefixo.
* **Justificativa:** A Árvore Trie é a estrutura mais eficiente para buscas de strings por prefixo (simulando um autocompletar). A microcomplexidade de busca é proporcional ao tamanho do prefixo digitado pelo usuário, e não ao número total de receitas cadastradas no sistema, garantindo alta performance mesmo com bases de dados maiores.

### 3. Algoritmo Guloso (Greedy)
* **Implementação:** Uma variação do problema da Mochila Fracionária/Inteira. O algoritmo calcula a razão de custo-benefício de cada receita dividindo a sua Avaliação pelo seu Custo.
* **Aplicação no sistema:** Utilizado no "Modo Chef" para recomendar um cardápio otimizado baseado em um teto de gastos (orçamento máximo).
* **Justificativa:** O algoritmo guloso ordena as receitas da maior razão (melhor avaliação e menor custo) para a menor. Ele interage sobre a lista ordenada, selecionando as receitas até atingir o limite do orçamento informado pelo usuário. É uma abordagem rápida e computacionalmente barata para encontrar uma boa solução de otimização nesse contexto.

## Identificador de Segurança e Integridade (Anti-Sabotagem)
Para cumprir o requisito de evitar adulterações misteriosas nas receitas, o sistema implementa um verificador de integridade baseado em criptografia.
* **Bibliotecas de apoio:** `hashlib` (para geração do hash SHA-256).
* **Funcionamento:** Quando o objeto da receita é instanciado na memória, os seus dados (nome, categoria, ingredientes, tempo, custo e avaliação) são concatenados em uma única string e submetidos a uma função de hash SHA-256. Essa assinatura digital é guardada na receita.
* O ID foi propositalmente removido do cálculo desse hash para permitir a detecção de receitas clonadas sob identificadores diferentes.
* No Modo Investigação, o sistema recalcula o hash com os dados atuais e compara com o original. Qualquer alteração indevida de preço ou ingrediente fará com que o novo hash seja diferente, disparando um alerta de sabotagem.
