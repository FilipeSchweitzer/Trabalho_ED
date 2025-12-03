# src/main.py

import csv
import pandas as pd
from data_structs import Match, Team
from bst_library import BST_A
from src.sorting import calculate_team_scores, generate_top_rankings

# Função para checar se o dado está faltando
def faltando(valor: str):
    if valor is None:
        return True

    valor = valor.strip()  # remove espaços

    # Valores considerados como "faltantes"
    return valor == "" or valor.lower() in ["na", "n/a", "null", "none", "-"]



def carregar_partidas_csv(caminho_csv: str):
    matches = []               # Lista de partidas
    times_unicos = set()       # Conjunto para contar times sem repetir
    linhas_filtradas = 0       # Contador de linhas descartadas

    with open(caminho_csv, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)

        for row in leitor:
            try:
                # Verificar campos essenciais
                if (faltando(row["home_team"]) or 
                    faltando(row["away_team"]) or 
                    faltando(row["home_score"]) or 
                    faltando(row["away_score"]) or
                    faltando(row["date"])):

                    print("Linha ignorada (dados faltantes):", row)
                    linhas_filtradas += 1
                    continue

                # Atualizar times únicos
                times_unicos.add(row["home_team"].strip())
                times_unicos.add(row["away_team"].strip())

                # Criar times
                home = Team(row["home_team"], int(row["home_score"]))
                away = Team(row["away_team"], int(row["away_score"]))

                # Criar Match
                match = Match(
                    date=row["date"],
                    home_team=home,
                    away_team=away,
                    tournament=row["tournament"],
                    city=row["city"],
                    country=row["country"],
                    neutral=str(row["neutral"]).lower() == "true"
                )

                matches.append(match)

            except Exception as e:
                print(f"Linha inválida ignorada: {e}\nConteúdo da linha:", row)
                linhas_filtradas += 1

    return matches, times_unicos, linhas_filtradas



if __name__ == "__main__":
    matches, times_unicos, linhas_filtradas = carregar_partidas_csv("data/results.csv")

    print("\n==== RESULTADOS ====")
    print("Total de partidas carregadas:", len(matches))
    print("Total de times únicos:", len(times_unicos))
    print("Total de linhas filtradas:", linhas_filtradas)
    print("====================\n")

    # Exibir algumas partidas
    for m in matches[:50]:
        print(m)

def carregar_times(caminho_csv: str):
    df = pd.read_csv(caminho_csv)

    times = {}  # dicionário

    for _, row in df.iterrows():
        home = row["home_team"]
        away = row["away_team"]

        home_score = int(row["home_score"])
        away_score = int(row["away_score"])

        # Criar time se ainda não existe
        if home not in times:
            times[home] = Team(home, 0)
        if away not in times:
            times[away] = Team(away, 0)

        # Somar gols
        times[home].score += home_score
        times[away].score += away_score

    return list(times.values())

# =====================================================================
# ETAPA 3: CRIAR AS DUAS BSTs
# =====================================================================
def criar_bsts(lista_times):
    # BST 1 → ordenada pelo nome da seleção
    bst_nome = BST_A(key=lambda t: t.name)

    # BST 2 → ordenada pela quantidade de gols
    bst_gols = BST_A(key=lambda t: t.score)

    # Inserir os times nas duas árvores
    for time in lista_times:
        bst_nome.insert(time)
        bst_gols.insert(time)

    return bst_nome, bst_gols



if __name__ == "__main__":

    # ----- Carregar times e somar gols -----
    lista_times = carregar_times("data/results.csv") # pyright: ignore[reportUndefinedVariable]

    # ----- Criar as duas BSTs -----
    bst_nome, bst_gols = criar_bsts(lista_times)

    # ----- Mostrar resultado -----
    print("\n=== Times ordenados alfabeticamente ===")
    for t in bst_nome.inorder():
        print(f"{t.name}: {t.score} gols")

    print("\n=== Times ordenados pela quantidade de gols ===")
    for t in bst_gols.inorder():
        print(f"{t.name}: {t.score} gols")


# =====================================================================
# ETAPA 4: ORDENAÇÃO
# =====================================================================

# 1. Calcular Pontos dos Times
all_teams = calculate_team_scores(matches)

# 2. Gerar Rankings usando Merge Sort (O(n log n) e Estável)
generate_top_rankings(all_teams, algorithm_name='Merge Sort')

# 3. Gerar Rankings usando Bubble Sort (O(n²)) - Para Comparação
generate_top_rankings(all_teams, algorithm_name='Bubble Sort')