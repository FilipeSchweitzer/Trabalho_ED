# src/main.py
import csv
from datetime import datetime
from typing import List, Dict, Tuple
from .data_structs import Match, Team
from .bst_library import BST_A
from .avl import AVLPointsTree_A
from .sorting import calculate_team_scores, merge_sort, bubble_sort, generate_top_rankings
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

def criar_bsts(lista_times: List[Team]) -> Tuple[BST_A, BST_A]:
    """Cria e popula as duas BSTs (por nome e por score)."""
    bst_nome = BST_A()
    bst_score = BST_A() # O requisito usa 'gols', mas agora estamos usando 'score' (pontos)
    
    # Inserir os times nas duas árvores
    for time in lista_times:
        # BST 1 → Chave = Nome (ordenada alfabeticamente)
        bst_nome.insert(time.name, time)
        
        # BST 2 → Chave = Score (ordenada por pontos)
        bst_score.insert(time.score, time)

    return bst_nome, bst_score

# =====================================================================
# Criação da AVL (Etapa 5)
# =====================================================================

def criar_avl_por_pontos(lista_times: List[Team]) -> AVLPointsTree_A:
    """Cria e popula a AVL com os times ordenados por pontos."""
    avl = AVLPointsTree_A()
    
    # A lista já está ordenada da Etapa 4, o que testará bem o balanceamento da AVL
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
    
    # Paths (assumindo que estamos na raiz do projeto 'Trabalho')
    INPUT_CSV = "data/results.csv"
    OUTPUT_CSV = "output/matches_summary.csv"

    # Etapa 2: Carregar Partidas
    print("--- Etapa 2: Carregando Partidas ---")
    matches, linhas_filtradas = carregar_partidas_csv(INPUT_CSV)
    print(f"Total de partidas carregadas: {len(matches)}")
    print(f"Total de linhas filtradas (dados faltantes/inválidos): {linhas_filtradas}")
    print("-" * 40)

    # Cálculo da pontuação dos times (Base para Etapas 3, 4, 5)
    lista_times = calculate_team_scores(matches)

    # Etapa 3: Criar BSTs
    print("--- Etapa 3: Implementando BSTs ---")
    bst_nome, bst_score = criar_bsts(lista_times)
    
    print("\n[BST por Nome (Ordem Alfabética)]")
    # Acessamos o valor (objeto Team) do nó
    for _, time_obj in bst_nome.inorder():
        print(f"  {time_obj.name}: {time_obj.score} pontos")

    print("\n[BST por Score (Ordem de Pontos)]")
    for score, time_obj in bst_score.inorder():
        print(f"  {time_obj.name}: {time_obj.score} pontos")
    print("-" * 40)
    
    # Etapa 4: Ordenação e Ranking
    print("--- Etapa 4: Ordenação e Rankings ---")
    # Criamos uma cópia da lista para ordenar
    times_ordenacao = lista_times[:] 
    
    # Usando o Merge Sort (O(n log n)) para ordenar a lista
    merge_sort(times_ordenacao) 
    
    top_more, top_less = generate_top_rankings(times_ordenacao, top_n=10)
    
    print("\n[Top 10 Seleções com MAIS pontos (Merge Sort)]")
    for i, team in enumerate(top_more):
        print(f"{i+1}. {team.name}: {team.score} pts")

    print("\n[Top 10 Seleções com MENOS pontos (Merge Sort)]")
    for i, team in enumerate(top_less):
        print(f"{i+1}. {team.name}: {team.score} pts")
    print("-" * 40)

    # Etapa 5: AVL por Pontos
    print("--- Etapa 5: AVL por Pontos ---")
    # Usamos a lista já ordenada pela Etapa 4 (times_ordenacao)
    avl_points = criar_avl_por_pontos(times_ordenacao)
    print(f"Altura da Árvore AVL: {avl_points.height()}")
    
    print("\n[AVL In-Order (Ordenado por Pontos)]")
    for score, time_obj in avl_points.inorder():
        print(f"  {time_obj.name}: {score} pontos")
    print("-" * 40)

    # Etapa 6: Geração do CSV
    print("--- Etapa 6: Gerando CSV de Resumo ---")
    # Certifique-se de que a pasta 'output' existe
    import os
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    gerar_csv_resumo(matches, OUTPUT_CSV)
    print(f"Arquivo de resumo gerado em: {OUTPUT_CSV}")
    print("-" * 40)

    # Exemplo de Busca (Para demonstração de complexidade O(log n))
    team_to_find = "Brazil"
    # Para usar a busca binária, a lista precisa estar ordenada pela chave de busca.
    # Usamos o resultado do Merge Sort (times_ordenacao)
    found_team = bst_nome.search(team_to_find)
    if found_team:
        print(f"Busca: {found_team.name} encontrado com {found_team.score} pontos.")
    else:
        print(f"Busca: {team_to_find} não encontrado.")