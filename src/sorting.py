# src/sorting.py
from typing import List, Dict, Tuple
from .data_structs import Match, Team

# =====================================================================
# Funções Auxiliares de Pontuação (Score)
# =====================================================================

def calculate_team_scores(matches: List[Match]) -> List[Team]:
    """
    Calcula a pontuação (score) de todos os times com base nas partidas.
    Regra: Vitória = 3, Empate = 1, Derrota = 0.
    Retorna uma lista de objetos Team com seus scores totais.
    """
    team_points: Dict[str, int] = {}
    
    # Acumula os pontos
    for match in matches:
        home_points, away_points = match.determine_points()
        
        # Inicializa se não existir e soma os pontos
        team_points[match.home_team_name] = team_points.get(match.home_team_name, 0) + home_points
        team_points[match.away_team_name] = team_points.get(match.away_team_name, 0) + away_points

    # Cria a lista final de objetos Team
    lista_times = []
    for name, score in team_points.items():
        lista_times.append(Team(name, score))
        
    return lista_times

def calculate_total_goals(matches: List[Match]) -> List[Team]:
    """
    Calcula o total de GOLS MARCADOS (acumulados) por todos os times.
    Esta lista é usada para a BST 2 da Etapa 3.
    Retorna uma lista de objetos Team com seus GOLS TOTAIS.
    """
    team_goals: Dict[str, int] = {}
    
    # Acumula os gols
    for match in matches:
        # Gols marcados por quem jogou em casa
        team_goals[match.home_team_name] = team_goals.get(match.home_team_name, 0) + match.home_score
        
        # Gols marcados por quem jogou fora
        team_goals[match.away_team_name] = team_goals.get(match.away_team_name, 0) + match.away_score

    # Cria a lista final de objetos Team
    lista_times_gols = []
    for name, goals in team_goals.items():
        # Usamos o atributo 'score' da classe Team para armazenar os gols
        lista_times_gols.append(Team(name, goals))
        
    return lista_times_gols


def generate_top_rankings(teams: List[Team], top_n: int = 10) -> Tuple[List[Team], List[Team]]:
    """
    Gera o ranking Top N com mais pontos e o Top N com menos pontos.
    """
    # Ordenação decrescente (mais pontos)
    sorted_teams_desc = sorted(teams, key=lambda t: t.score, reverse=True)
    
    # Ordenação crescente (menos pontos)
    sorted_teams_asc = sorted(teams, key=lambda t: t.score, reverse=False)
    
    top_more = sorted_teams_desc[:top_n]
    top_less = sorted_teams_asc[:top_n]
    
    return top_more, top_less


# =====================================================================
# Algoritmos de Ordenação
# =====================================================================

def bubble_sort(arr: List[Team]):
    """
    Algoritmo de ordenação Bubble Sort (O(n²)).
    Ordena a lista 'arr' em ordem crescente pelo score.
    """
    n = len(arr)
    for i in range(n):
        swapped = False # Otimização
        for j in range(0, n - i - 1):
            # Compara score usando a sobrecarga do operador '<' (Team.__lt__)
            if arr[j + 1] < arr[j]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

def merge_sort(arr: List[Team]):
    """
    Algoritmo de ordenação Merge Sort (O(n log n)).
    Estável e eficiente. Ordena a lista 'arr' em ordem crescente pelo score.
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]  # Parte esquerda
        R = arr[mid:]  # Parte direita
        
        merge_sort(L)  # Ordena recursivamente L
        merge_sort(R)  # Ordena recursivamente R
        
        i = j = k = 0
        
        # Mescla as partes ordenadas
        while i < len(L) and j < len(R):
            # Compara score usando a sobrecarga do operador '<' (Team.__lt__)
            if L[i] < R[j]: 
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            
        # Adiciona elementos restantes, se houver
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1