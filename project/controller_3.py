""" Managing the flow of the tournament's data.

    This module could be split in two. The first part would
    define four functions. Two of them allow the manager to
    override the description of the tournament or one player's
    ranking. The other two are related to the duration of the
    rounds.

    The second part instantiates and calls the previously defined
    classes and functions. The goal is to save or load the data
    the manager needs as the tournament happens.

    For each new tournament, the script will be run again.
    Therefore, we only need one tournament instance per script ran.
"""

import time
from typing import List

from controller_1 import (update_all_players_attrs_after_round,
                          CreatingMatchesStoringInRoundOne,
                          CreatingMatchesStoringInSubsequentRounds,
                          CreatingPlayersStoringInTournament,
                          CreatingRoundStoringInTournament)
from controller_2 import RequestsMenu, SaveDataInDB
from models import Tournament, Round
from view import (collect_tournament_info,
                  override_tournament_description,
                  override_player_ranking,
                  complete_override_player_ranking)
from view_display import (display_ranking,
                          display_first_round_matches,
                          display_subsequent_round_matches)


def request_tournament_new_description(tournament: Tournament):

    """Overrides the description of the tournament.

    The new description is taken from view.py's override_player_ranking
    function. If it's not an empty string, it becomes the value of
    the description attribute of the tournament instance passed as argument.

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

    The new ranking is taken from view.py's override_player_ranking()
    and complete_override_player_ranking() functions. If the return value
    of the former is an empty string, nothing happens.

    Otherwise, the player instance corresponding to the player's last name is
    retrieved. The latter function in view.py is called. The number entered
    by the manager becomes the new value of the
    ranking attribute of the player.

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


def time_control(tournament: Tournament):

    """Simulates the duration of the rounds.

    Halt the flow of the program. The duration of the halt corresponds
    to the time control chosen by the manager when first instantiating
    the tournament.

    Args:
        tournament: The tournament that is taking place.
    """

    rd_duration = tournament.time_control

    if rd_duration == "bullet" or rd_duration == "BULLET":
        print("the round is taking place...")
        return time.sleep(10)
    elif rd_duration == "blitz" or rd_duration == "BLITZ":
        print("the round is taking place...")
        return time.sleep(300)
    elif rd_duration == "rapid" or rd_duration == "RAPID":
        print("the round is taking place...")
        return time.sleep(12000)
    else:
        raise ValueError("something went wrong with the instantiation of the "
                         "tournament, namely it's time-control attribute")


def update_start_end_datetime_round(round_number: int, tournament: Tournament):

    """Corrects the start and end datetime of subsequent rounds.

    All the Round objects are instantiated straight after the tournament is
    instantiated. Their start_datetime attributes are given the same value.
    Idem for their end_datetime attributes. However, those values are false
    except for the first round. This functions corrects those values.


    Args:
        round_number: the number of the round which start and end datetime
            will be updated.
        tournament: the tournament that is taking place.
    """

    round: Round = tournament.rounds[f"Round {round_number}"]

    # In order to update the start and end datetime,
    # we add the duration of a round to the
    # start datetime and end datetime of the preceding round.
    s: float = tournament.rounds[f"Round {round_number-1}"].start_datetime
    e: float = tournament.rounds[f"Round {round_number-1}"].end_datetime
    rd_duration = tournament.time_control

    if rd_duration == "bullet" or rd_duration == "BULLET":
        round.start_datetime = s+180
        round.end_datetime = e+180
    elif rd_duration == "blitz" or rd_duration == "BLITZ":
        round.start_datetime = s+300
        round.end_datetime = e+300
    elif rd_duration == "rapid" or rd_duration == "RAPID":
        round.start_datetime = s+12000
        round.end_datetime = e+12000

    # we also need to update the beautified version
    # of the start and end datetime
    round.__post_init__()

    tournament.rounds[f"Round {round_number}"] = round


if __name__ == "__main__":

    # instantiating the tournament
    tournament = Tournament(*collect_tournament_info())

    creating_pl_instances = CreatingPlayersStoringInTournament(tournament)

    # setting up the first round
    display_first_round_matches(tournament)
    creating_round_instances = CreatingRoundStoringInTournament(tournament)

    for i in range(1, tournament.number_of_rounds):
        update_start_end_datetime_round(i + 1, tournament)

    # the first round is taking place
    time_control(tournament)

    # the first round happened. Collecting the results.
    creating_match_instances = CreatingMatchesStoringInRoundOne(tournament, 1)
    last_round_matches = tournament.rounds["Round 1"].matches
    update_all_players_attrs_after_round(last_round_matches)

    # checking if the manager wants to override some data.
    request_tournament_new_description(tournament)
    request_player_new_ranking(tournament)

    # checking if the manager wants to save some data.
    possibly_saving_data = SaveDataInDB(tournament)

    if tournament.number_of_rounds > 1:
        for i in range(1, tournament.number_of_rounds):
            # the algorithms used for setting up the first round matches
            # is different from the one used for setting up the
            # subsequent rounds matches. Therefore, the first round matches
            # are instantiated out of the loop.
            # Also, the range function starts at 1 but the first round
            # to be instantiated in the loop is round2. Thus the arg passed
            # to the CreatingMatchesStoringInSubsequentRounds class is i+1

            display_subsequent_round_matches(tournament)

            time_control(tournament)

            creating_more_matches = CreatingMatchesStoringInSubsequentRounds(
                tournament, i + 1)
            last_round_matches = tournament.rounds[f"Round {i + 1}"].matches
            update_all_players_attrs_after_round(last_round_matches)

            request_tournament_new_description(tournament)
            request_player_new_ranking(tournament)

            possibly_saving_data = SaveDataInDB(tournament)

    display_ranking(tournament)

    making_a_request = RequestsMenu(tournament)
