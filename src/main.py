# src/main.py
import csv
from datetime import datetime
from typing import List, Dict, Tuple
# Importações atualizadas
from .data_structs import Match, Team
from .bst_library import BST_A
from .avl import AVLPointsTree_A
from .sorting import (
    calculate_team_scores, 
    calculate_total_goals, 
    merge_sort, 
    generate_top_rankings
)
from .search import linear_search, binary_search

# =====================================================================
# Funções de Leitura e Filtro (Etapa 2)
# =====================================================================

def faltando(valor: str) -> bool:
    """Checa se o dado está faltando."""
    if valor is None:
        return True
    valor_strip = str(valor).strip()
    return valor_strip == "" or valor_strip.lower() in ["na", "n/a", "null", "none", "-"]

def carregar_partidas_csv(caminho_csv: str) -> Tuple[List[Match], int]:
    """Lê o CSV, cria objetos Match e filtra dados faltantes."""
    matches: List[Match] = []
    linhas_filtradas = 0

    with open(caminho_csv, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)

        for row in leitor:
            try:
                # Filtrar campos essenciais
                if (faltando(row["home_team"]) or faltando(row["away_team"]) or 
                    faltando(row["home_score"]) or faltando(row["away_score"]) or
                    faltando(row["date"])):
                    linhas_filtradas += 1
                    continue
                
                # Conversão de tipos
                data_obj = datetime.strptime(row["date"], "%Y-%m-%d")
                home_score = int(row["home_score"])
                away_score = int(row["away_score"])

                # Criar Match (usando nomes dos times, conforme data_structs)
                match = Match(
                    date=data_obj,
                    home_team_name=row["home_team"].strip(),
                    away_team_name=row["away_team"].strip(),
                    home_score=home_score,
                    away_score=away_score,
                    tournament=row.get("tournament", "").strip(),
                    city=row.get("city", "").strip(),
                    country=row.get("country", "").strip(),
                    neutral=str(row.get("neutral", "False")).lower() == "true"
                )
                matches.append(match)

            except Exception as e:
                # print(f"Linha inválida ignorada: {e}. Conteúdo: {row}")
                linhas_filtradas += 1

    return matches, linhas_filtradas

# =====================================================================
# Criação das BSTs (Etapa 3)
# =====================================================================

def criar_bsts(lista_times_pontos: List[Team], lista_times_gols: List[Team]) -> Tuple[BST_A, BST_A]:
    """Cria e popula as duas BSTs (por nome e por gols totais)."""
    bst_nome = BST_A()
    bst_gols = BST_A()
    
    # 1. BST por Nome (Chave = Nome | Valor = Team/Pontos)
    for time in lista_times_pontos:
        bst_nome.insert(time.name, time)
        
    # 2. BST por Gols Totais (Chave = Gols | Valor = Team/Gols)
    for time in lista_times_gols:
        bst_gols.insert(time.score, time)

    return bst_nome, bst_gols

# =====================================================================
# Criação da AVL (Etapa 5)
# =====================================================================

def criar_avl_por_pontos(lista_times: List[Team]) -> AVLPointsTree_A:
    """Cria e popula a AVL com os times ordenados por pontos."""
    avl = AVLPointsTree_A()
    
    for time in lista_times:
        avl.insert(time)
        
    return avl

# =====================================================================
# Geração do CSV (Etapa 6)
# =====================================================================

def gerar_csv_resumo(matches: List[Match], caminho_saida: str):
    """Grava o resumo das partidas no formato exigido."""
    with open(caminho_saida, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Cabeçalho: year,country,home_team,away_team,score (score = "home_score-away_score")
        writer.writerow(["year", "country", "home_team", "away_team", "score"])
        
        for match in matches:
            writer.writerow(match.to_list())

# =====================================================================
# BLOCO PRINCIPAL DE EXECUÇÃO
# =====================================================================

if __name__ == "__main__":
    
    # Paths 
    INPUT_CSV = "data/results.csv"
    OUTPUT_CSV = "output/matches_summary.csv"

    # Etapa 2: Carregar Partidas
    print("--- Etapa 2: Carregando Partidas ---")
    matches, linhas_filtradas = carregar_partidas_csv(INPUT_CSV)
    print(f"Total de partidas carregadas: {len(matches)}")
    print(f"Total de linhas filtradas (dados faltantes/inválidos): {linhas_filtradas}")
    print("-" * 40)

    # Cálculo da pontuação e gols
    lista_times_pontos = calculate_team_scores(matches)
    lista_times_gols = calculate_total_goals(matches)

    # Etapa 3: Criar BSTs
    print("--- Etapa 3: Implementando BSTs ---")
    bst_nome, bst_gols = criar_bsts(lista_times_pontos, lista_times_gols) 
    
    # PRINTS ADICIONADOS AQUI
    print("\n[BST por Nome (Ordem Alfabética - In-order)]")
    # A BST por nome usa o nome como chave, o in-order retorna em ordem alfabética.
    for key, team in bst_nome.inorder()[:10]: # Imprime os primeiros 10
        print(f"  - {team.name} (Pontos: {team.score})")

    print("\n[BST por Gols Totais (Ordem de Gols - In-order)]")
    # A BST por gols usa o score de gols como chave, o in-order retorna em ordem crescente de gols.
    # Note que a chave (key) é o score de gols (value.score).
    for key, team in bst_gols.inorder()[:10]: # Imprime os primeiros 10 (menores scores de gols)
        print(f"  - {team.name} (Gols: {key})")
    # FIM DOS PRINTS DA ETAPA 3
    
    print("-" * 40)
    
    # Etapa 4: Ordenação e Ranking
    print("--- Etapa 4: Ordenação e Rankings ---")
    times_ordenacao = lista_times_pontos[:] 
    
    # Usando o Merge Sort (O(n log n) e estável) para ordenar a lista
    merge_sort(times_ordenacao) # Ordena em ordem crescente por score de pontos
    
    top_more, top_less = generate_top_rankings(times_ordenacao, top_n=10)
    
    # PRINTS ADICIONADOS AQUI
    print("\n[Top 10 Seleções com MAIS pontos (Merge Sort)]")
    for i, team in enumerate(top_more):
        print(f"  {i+1}. {team.name}: {team.score} pontos")
        
    print("\n[Top 10 Seleções com MENOS pontos (Merge Sort)]")
    for i, team in enumerate(top_less):
        print(f"  {i+1}. {team.name}: {team.score} pontos")
    # FIM DOS PRINTS DA ETAPA 4
    
    print("-" * 40)

    # Etapa 5: AVL por Pontos
    print("--- Etapa 5: AVL por Pontos ---")
    avl_points = criar_avl_por_pontos(times_ordenacao)
    print(f"Altura da Árvore AVL: {avl_points.height()}")
    
    # PRINTS ADICIONADOS AQUI
    print("\n[AVL In-Order (Ordenado por Pontos)]")
    # O in-order retorna em ordem crescente de pontuação (score).
    for key, team in avl_points.inorder()[:10]: # Imprime os primeiros 10 (menores scores)
        print(f"  - {team.name} (Pontos: {key})")
    # FIM DOS PRINTS DA ETAPA 5

    print("-" * 40)

    # Etapa 6: Geração do CSV
    print("--- Etapa 6: Gerando CSV de Resumo ---")
    import os
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    gerar_csv_resumo(matches, OUTPUT_CSV)
    print(f"Arquivo de resumo gerado em: {OUTPUT_CSV}")
    print("-" * 40)

    # =====================================================================
    # DEMONSTRAÇÃO DOS ALGORITMOS DE BUSCA (REQUISITO IMPLÍCITO)
    # =====================================================================
    
    team_to_find_name = "Brazil" # Para busca por nome
    
    print("--- Demonstração de Busca ---")

    # 1. Busca na BST (O(log n) no caso médio)
    # A melhor escolha para buscar um time por NOME em uma estrutura dinâmica
    found_team_bst = bst_nome.search(team_to_find_name)
    if found_team_bst:
        print(f"1. Busca BST por Nome (O(log n)): Time '{found_team_bst.name}' encontrado com {found_team_bst.score} pontos.")
    else:
        print(f"1. Busca BST por Nome (O(log n)): Time '{team_to_find_name}' não encontrado.")


    # 2. Busca Linear (O(n))
    # Aplicada na lista de times *não ordenada* (Etapa 2), buscando por nome.
    # Criamos uma lista de nomes para facilitar a busca linear simples.
    names_list = [team.name for team in lista_times_pontos]
    index_linear = linear_search(names_list, team_to_find_name)
    if index_linear != -1:
        print(f"2. Busca Linear por Nome (O(n)): Time '{names_list[index_linear]}' encontrado na posição {index_linear}.")
    else:
        print(f"2. Busca Linear por Nome (O(n)): Time '{team_to_find_name}' não encontrado.")


    # 3. Busca Binária (O(log n))
    # Aplicada na lista de times *ordenada por score* (Etapa 4), buscando o score.
    # Buscamos um score conhecido, por exemplo, o score do primeiro time ordenado.
    target_score = times_ordenacao[0].score if times_ordenacao else -1 
    
    # Criamos uma lista de scores ordenados para a Busca Binária
    scores_list = [team.score for team in times_ordenacao]
    
    index_binary = binary_search(scores_list, target_score)
    
    if index_binary != -1:
        print(f"3. Busca Binária por Score (O(log n)): Score {target_score} encontrado na posição {index_binary}. ({times_ordenacao[index_binary].name}).")
    else:
        print(f"3. Busca Binária por Score (O(log n)): Score {target_score} não encontrado.")
    
    print("-" * 40)