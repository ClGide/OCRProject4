"""Allows the dynamic instantiation of all the players in the tournament.
"""

from typing import List, Tuple

from models import Player, Tournament
from view import collect_player_info


class CreatingPlayersStoringInTournament:
    """Instantiates and stores all the competitors in the tournament.

    When instantiated, the class will create all the player objects in the
    the tournament.

    In order to instantiate the players, we format the data from view.py.
    More precisely, collect_player_info from view.py is called once for
    every player in the tournament. With that formatted data, the players
    are iteratively instantiated.

    Attributes:
        tournament: the tournament in which the players compete.
        players_number: the number of players competing in the
            tournament.
    """
    def __init__(self, tournament: Tournament):
        self.tournament = tournament
        self.players_number: int = tournament.players_number
        self.create_and_store_player_instances()

    def requesting_players_info(self) -> List[Tuple[str, str, str, str, str]]:
        players_info = []

        for _ in range(self.players_number):
            player_info = collect_player_info()
            players_info.append(player_info)

        return players_info

    def create_and_store_player_instances(self):
        players_info = self.requesting_players_info()

        player_instances: List[Player] = []
        for player_info in players_info:
            player_instance = Player(*player_info)
            player_instances.append(player_instance)

        self.tournament.players_instances = player_instances
