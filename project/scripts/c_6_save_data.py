"""Saves data about the tournament the user needs in a JSON database.
"""

from typing import Dict, List

from tinydb import TinyDB

from models import Tournament
from view import (what_table_to_save)

db = TinyDB('db.json', indent=4, separators=(',', ': '))


class SaveDataInDB:
    """requests user needs and saves data about the tournament accordingly.

    All the data about the tournament can be saved either in a player table
    or a tournament table. When instantiated, this class asks the user if
    he needs the player or the tournament table or both.

    To requests user needs, what_table_to_save from view.py is called. To
    format the data in order to store it in a JSON db, we use object methods
    defined in models.py.

    Attributes:
        tournament: The tournament that is taking place.

    Raises:
        ValueError: The user doesn't enter a number corresponding
            to one of the possible actions.
    """
    def __init__(self, tournament: Tournament):
        self.what_table_to_save = what_table_to_save()
        self.tournament = tournament

        if self.what_table_to_save == "1":
            self.save_the_tournament(self.tournament.name)
        elif self.what_table_to_save == "2":
            self.save_players_from_tournament()
        elif self.what_table_to_save == "3":
            self.save_the_tournament(self.tournament.name)
            self.save_players_from_tournament()
        elif self.what_table_to_save == "4":
            pass
        else:
            raise ValueError("if you need something, "
                             "please only enter the number corresponding "
                             "to your need")

    def save_players_from_tournament(self):
        serialized_players: List[Dict[str, str]] = []
        for player in self.tournament.players_instances:
            serialized_player: Dict[str, str] = player.serialize_player()
            serialized_players.append(serialized_player)

        player_table_name = f"players_competing_in_{self.tournament.name}"
        players_table = db.table(player_table_name)
        players_table.truncate()
        players_table.insert_multiple(serialized_players)

    def save_the_tournament(self, tournament_table_name: str):

        serialized_tournament = self.tournament.serialize_tournament()

        tournament_table = db.table(tournament_table_name)
        tournament_table.truncate()
        tournament_table.insert(serialized_tournament)
