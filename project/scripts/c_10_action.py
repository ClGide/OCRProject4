""" Pairing players, storing and/or retrieving data about the tournament.
"""

from c_2_pairing_subsequent_rounds import update_all_players_attrs_after_round
from c_5_match_instantiation import (CreatingMatchesStoringInRoundOne,
                                     CreatingMatchesStoringInSubsequentRounds)
from c_4_round_instantiation import CreatingRoundStoringInTournament
from c_3_player_instantiation import CreatingPlayersStoringInTournament
from c_6_save_data import SaveDataInDB
from c_7_retrieve_data import RequestsMenu
from c_8_modify_attributes import (request_tournament_new_description,
                                   request_player_new_ranking)
from c_9_time_control import (time_control,
                              update_start_end_datetime_round)
from models import Tournament
from view import collect_tournament_info
from view_display import (display_ranking,
                          display_first_round_matches,
                          display_subsequent_round_matches)

if __name__ == "__main__":

    # instantiating the tournament.
    tournament = Tournament(*collect_tournament_info())

    creating_pl_instances = CreatingPlayersStoringInTournament(tournament)

    # setting up the first round.
    display_first_round_matches(tournament)
    creating_round_instances = CreatingRoundStoringInTournament(tournament)

    for i in range(1, tournament.number_of_rounds):
        update_start_end_datetime_round(i + 1, tournament)

    # the first round is taking place.
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

    # the algorithms used for setting up the first round matches
    # is different from the one used for setting up the
    # subsequent rounds matches. Therefore, the first round matches
    # are instantiated before the loop.
    # Also, the range function starts at 1 but the first round
    # to be instantiated in the loop is round2. Thus, the arg passed
    # to CreatingMatchesStoringInSubsequentRounds is i+1
    if tournament.number_of_rounds > 1:
        for i in range(1, tournament.number_of_rounds):
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
