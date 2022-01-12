from typing import List

from controller_1 import time_control, update_all_players_attrs_after_round, \
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


if __name__ == "__main__":
    """ 
    For each new tournament, the script will be run again. Therefore, we know we only need one tournament instance. 
    We get the info from the VIEW.
    """
    # instantiating the tournament
    tournament = Tournament(*collect_tournament_info())

    storing_player_instances_in_tournament = CreatingPlayersStoringInTournament(tournament)

    # setting up the first round
    display_first_round_matches()
    storing_round_instances_in_tournament = CreatingRoundStoringInTournament(tournament)

    # the first round is taking place
    time_control(tournament)

    # the first round happened
    storing_match_instances_in_tournament = CreatingMatchesStoringInRoundOne(1)
    matches_from_last_round = tournament.rounds["Round 1"].dict_of_matches
    update_all_players_attrs_after_round(matches_from_last_round)

    possibly_saving_data = SaveDataInDB(tournament)

    request_new_tournament_description(tournament)
    request_new_player_ranking(tournament)

    if tournament.number_of_rounds > 1:
        for i in range(1, tournament.number_of_rounds):
            # the algorithm used for the first round and for the subsequent rounds are different. Therefore,
            # the first round matches are instantiated out of the loop. The range built-in function starts at
            # 1 but the first round to be instantiated in the loop is round2, that's why the arg passed to the
            # CreatingMatchesStoringInSubsequentRounds class is i+1

            display_subsequent_round_matches()
            time_control(tournament)

            storing_more_match_instances_in_tournament = CreatingMatchesStoringInSubsequentRounds(i + 1)
            matches_from_last_round = tournament.rounds[f"Round {i + 1}"].dict_of_matches
            update_all_players_attrs_after_round(matches_from_last_round)

            possibly_saving_data = SaveDataInDB(tournament)

            request_new_tournament_description(tournament)
            request_new_player_ranking(tournament)

    display_ranking()

    making_a_request = RequestsMenu(tournament)


