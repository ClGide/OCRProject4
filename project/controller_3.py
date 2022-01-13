from typing import List

import time

from controller_1 import update_all_players_attrs_after_round, \
    CreatingMatchesStoringInRoundOne, CreatingMatchesStoringInSubsequentRounds, \
    CreatingPlayersStoringInTournament, CreatingRoundStoringInTournament
from controller_2 import RequestsMenu, SaveDataInDB
from models import Tournament
from view import collect_tournament_info, override_tournament_description, override_player_ranking, \
    complete_override_player_ranking
from view_display import display_ranking, display_first_round_matches, display_subsequent_round_matches


def request_new_tournament_description(tournament: Tournament):
    new_description: str = override_tournament_description()
    if new_description == "":
        pass
    else:
        tournament.description = new_description


def request_new_player_ranking(tournament: Tournament):
    which_player: str = override_player_ranking()
    if which_player == "":
        pass
    else:
        list_of_player_names: List[str] = [player.last_name for player in tournament.list_of_players_instances]
        if which_player in list_of_player_names:
            new_ranking: str = complete_override_player_ranking()
            player_index = list_of_player_names.index(which_player)
            tournament.list_of_players_instances[player_index].ranking = new_ranking
        else:
            raise ValueError("the player you're searching isn't playing in this tournament")


def time_control(tournament: Tournament):
    # this function simulates the time each round takes depending on the time control chose
    # by the manager when instantiating the tournament.
    if tournament.time_control == "bullet" or tournament.time_control == "BULLET":
        print("the round is taking place...")
        return time.sleep(10)
    elif tournament.time_control == "blitz" or tournament.time_control == "BLITZ":
        print("the round is taking place...")
        return time.sleep(300)
    elif tournament.time_control == "rapid" or tournament.time_control == "RAPID":
        print("the round is taking place...")
        return time.sleep(12000)
    else:
        raise ValueError("something went wrong with the instantiation of the tournament, "
                         "namely it's time-control attribute")


def update_start_end_datetime_round(round_number: int, tournament: Tournament):

    round = tournament.rounds[f"Round {round_number}"]

    value_s = round.start_datetime
    value_e = round.end_datetime
    name_s = "start_datetime"
    name_e = "end_datetime"

    if tournament.time_control == "bullet":
        round.__setattr__(name_s, value_s+180)
        round.__setattr__(name_e, value_e+180)
    elif tournament.time_control == "blitz":
        round.__setattr__(name_s, value_s+300)
        round.__setattr__(name_e, value_e+300)
    elif tournament.time_control == "rapid":
        round.__setattr__(name_s, value_s+12000)
        round.__setattr__(name_e, value_e+12000)


if __name__ == "__main__":
    """ 
    For each new tournament, the script will be run again. 
    Therefore, we only need one tournament instance per script ran. 
    """
    # instantiating the tournament
    tournament = Tournament(*collect_tournament_info())

    storing_player_instances_in_tournament = CreatingPlayersStoringInTournament(tournament)

    # setting up the first round
    display_first_round_matches(tournament)
    storing_round_instances_in_tournament = CreatingRoundStoringInTournament(tournament)

    # the first round is taking place
    time_control(tournament)

    # the first round happened
    storing_match_instances_in_tournament = CreatingMatchesStoringInRoundOne(tournament, 1)
    matches_from_last_round = tournament.rounds["Round 1"].dict_of_matches
    update_all_players_attrs_after_round(matches_from_last_round)

    request_new_tournament_description(tournament)
    request_new_player_ranking(tournament)

    possibly_saving_data = SaveDataInDB(tournament)

    if tournament.number_of_rounds > 1:
        for i in range(1, tournament.number_of_rounds):
            # the algorithm used for the first round and for the subsequent rounds are different. Therefore,
            # the first round matches are instantiated out of the loop. The range built-in function starts at
            # 1 but the first round to be instantiated in the loop is round2, that's why the arg passed to the
            # CreatingMatchesStoringInSubsequentRounds class is i+1

            display_subsequent_round_matches(tournament)
            time_control(tournament)

            storing_more_match_instances_in_tournament = CreatingMatchesStoringInSubsequentRounds(tournament, i + 1)
            matches_from_last_round = tournament.rounds[f"Round {i + 1}"].dict_of_matches
            update_start_end_datetime_round(i+1, tournament)
            update_all_players_attrs_after_round(matches_from_last_round)

            request_new_tournament_description(tournament)
            request_new_player_ranking(tournament)

            possibly_saving_data = SaveDataInDB(tournament)

    display_ranking(tournament)

    making_a_request = RequestsMenu(tournament)


