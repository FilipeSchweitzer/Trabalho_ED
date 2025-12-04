# 🏆 Trabalho Final: Estrutura de Dados (Global Football Goalscorers Analysis)

Este projeto é o trabalho final da Unidade Curricular de Estrutura de Dados, do curso Bacharel em Ciência de Dados e Inteligência Artificial do Centro Universitário SENAI (UniSENAI).

O objetivo principal é demonstrar o domínio sobre diversas estruturas de dados básicas e avançadas (como **BSTs** e **AVLs**) e algoritmos de **ordenção** e **busca**, aplicados à manipulação e análise de um conjunto de dados real sobre partidas de futebol internacionais.

---

### 🎯 Visão Geral e Tópicos Abordados

O projeto utiliza o arquivo `results.csv` do *Global Football Goalscorers Dataset* e cobre os seguintes tópicos essenciais:

* **Modelagem Orientada a Objetos (OOP):** Classes `Match` e `Team`.
* **Manipulação de Arquivos:** Leitura e filtro de dados CSV.
* **Estruturas de Dados Básicas:** Listas e Dicionários.
* **Árvores de Busca:** Implementação de Árvore Binária de Busca Simples (**BST**). 

[Image of Binary Search Tree structure]

* **Árvore Balanceada:** Implementação da Árvore **AVL**, incluindo todas as rotações necessárias. 

[Image of AVL tree showing left rotation]

* **Algoritmos de Ordenação:** Implementação de um algoritmo O(n log n) (**Merge Sort**) e um O(n²) (**Bubble Sort**).
* **Algoritmos de Busca:** Demonstração de Busca Linear e Busca Binária.
* **Análise Assintótica (Big O):** Descrição e comparação das complexidades.

---

## 🛠️ Estrutura do Projeto

O projeto segue a seguinte organização de arquivos e módulos:

---

### 🚀 Como Executar o Projeto

1.  **Pré-requisito:** Certifique-se de que o arquivo `results.csv` esteja presente na pasta `data/`.
2.  **Instalação (se necessário):** O projeto utiliza apenas bibliotecas padrão do Python (como `csv`, `datetime`, `os`).
3.  **Execução:**
    Para rodar o script e direcionar todas as saídas de console para o arquivo `prints.txt` (conforme solicitado), use o seguinte comando no terminal (a partir do diretório raiz do projeto):

    ```bash
    python3 src/main.py > prints.txt
    ```

4.  **Verificação:** Após a execução, verifique os arquivos gerados:
    * `output/matches_summary.csv`
    * `prints.txt` (contendo os logs da execução, BSTs, AVL, e Rankings)

---

### 🤝 Colaboradores

Este trabalho foi desenvolvido em grupo e cada membro contribuiu para as etapas de modelagem, implementação de estruturas de dados e análise de complexidade.

| Nome do Estudante | Linkedin | GitHub |
| :--- | :--- | :--- |
| **Filipe Schweitzer** | linkedin.com/in/filipe-schweitzer-03245049 | https://github.com/FilipeSchweitzer Assintótica. |
| **[Nome do Aluno 2]** | Especialista em Algoritmos | Ordenação (Merge Sort, Bubble Sort) e Busca (Linear, Binária) (Etapa 4). |
| **[Nome do Aluno 3]** | Arquiteto de Dados | Modelagem de Classes (`data_structs.py`), Leitura e Geração de CSV (Etapas 1, 2 e 6). |
| **[Nome do Aluno 4]** | Testes e Documentação | Teste de todas as funções, elaboração do `report.md` (Etapa 7). |
| **[Nome do Aluno 5]** | Gerente de Projeto | Integração de módulos, revisão de código e organização dos entregáveis. |