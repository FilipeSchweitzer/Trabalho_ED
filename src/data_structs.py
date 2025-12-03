# src/data_structs.py
from datetime import datetime
from typing import List, Tuple

class Team:
    """
    Classe que representa uma seleção ou time de futebol.
    Atributos: name (nome do time) e score (pontuação acumulada).
    """
    def __init__(self, name: str, score: int = 0):
        self.name = name
        self.score = score

    def __lt__(self, other):
        """Define o comportamento de 'menor que' para ordenação por score."""
        return self.score < other.score

    def __repr__(self):
        """Representação para debug."""
        return f"Team('{self.name}', {self.score})"

class Match:
    """
    Classe que representa uma partida de futebol.
    """
    def __init__(self, date: datetime, home_team_name: str, away_team_name: str, 
                 home_score: int, away_score: int, tournament: str = "", 
                 city: str = "", country: str = "", neutral: bool = False):
        # A classe Match armazena os nomes dos times, não objetos Team, 
        # para facilitar a leitura inicial do CSV.
        self.date = date
        self.home_team_name = home_team_name
        self.away_team_name = away_team_name
        self.home_score = home_score
        self.away_score = away_score
        self.tournament = tournament
        self.city = city
        self.country = country
        self.neutral = neutral

    def total_goals(self) -> int:
        """Calcula e retorna o total de gols na partida."""
        return self.home_score + self.away_score

    def to_list(self) -> List[str]:
        """
        Retorna uma linha para gravação CSV no formato: 
        [ano, país, nome_time_casa, nome_time_visitante, placar (ex: "2-0")]
        """
        year = str(self.date.year)
        score = f"{self.home_score}-{self.away_score}"
        # Formato de score alterado de "2 x 0" para "2-0" conforme o requisito do CSV de saída.
        return [year, self.country, self.home_team_name, self.away_team_name, score]

    def determine_points(self) -> Tuple[int, int]:
        """
        Determina os pontos de cada time (casa, visitante) baseado no resultado.
        Vitória = 3 pontos, Empate = 1 ponto, Derrota = 0 pontos (Etapa 4).
        Retorna: (pontos_casa, pontos_visitante)
        """
        if self.home_score > self.away_score:
            return (3, 0)  # Vitória Casa
        elif self.home_score < self.away_score:
            return (0, 3)  # Vitória Visitante
        else:
            return (1, 1)  # Empate