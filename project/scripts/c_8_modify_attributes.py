"""Overrides tournament description and/or player ranking.
"""

from typing import List

from models import Tournament
from view import (override_tournament_description,
                  override_player_ranking,
                  complete_override_player_ranking)


def request_tournament_new_description(tournament: Tournament):
    """Overrides the description of the tournament.

    The new description is taken from view.py's override_player_ranking
    function. If it's not an empty string, it becomes the value of
    the tournament's description attribute.

    Args:
        tournament: The tournament that is taking place.
    """
    new_description: str = override_tournament_description()
    if new_description == "":
        pass
    else:
        tournament.description = new_description


def request_player_new_ranking(tournament: Tournament):
    """Overrides the ranking of a player.

    The new ranking is taken from view.py's override_player_ranking
    and complete_override_player_ranking functions. If the return value
    of the former is an empty string, nothing happens.

    Otherwise, the player instance corresponding to the player's last name is
    retrieved from the tournament. The latter function from view.py is called.
    The number entered by the user becomes the value of the retrieved player's
    ranking attribute.

    Args:
        tournament: The tournament that is taking place.

    Raises:
         ValueError: If the string inputted by the manager in view.py's
            override_player_ranking() function
            isn't in the tournament's list of player last names.
    """
    player_instances = tournament.players_instances
    which_player: str = override_player_ranking()
    if which_player == "":
        pass
    else:
        list_of_player_names: List[str] = [
            player.last_name
            for player
            in player_instances]

        if which_player in list_of_player_names:
            new_ranking: str = complete_override_player_ranking()
            new_ranking: int = int(new_ranking)
            player_index = list_of_player_names.index(which_player)
            player_instances[player_index].ranking = new_ranking
        else:
            raise ValueError("We didn't find the player in the DB. Please,"
                             "check the spelling of the LAST name.")
