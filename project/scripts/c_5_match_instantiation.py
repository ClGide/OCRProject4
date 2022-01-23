"""Allows the dynamic instantiation of matches throughout the tournament.

Keep in mind that for the swiss-system algorithm, the pairing for the
first round is different from the one for subsequent rounds.
"""

import itertools
from typing import Dict, List, Tuple

from c_1_pairing_first_round import pairing_for_first_round
from c_2_pairing_subsequent_rounds import avoid_player_meeting_twice
from models import Player, Round, Tournament, Match
from view import collect_results


class CreatingMatchesStoringInRoundOne:
    """Instantiates and stores the matches from round one.

    When instantiated, the class requests to the user the result
    of all the matches in the round. More specifically, collect_results
    from view.py is called once per match.

    With those results, it instantiates the matches that just
    took place. Then, it stores those instances in the tournament's
    rounds attribute.

    More precisely, the rounds attribute is a dictionary storing
    all the rounds taking place in the tournament. The
    first round is retrieved. The instantiated matches are given
    as the value to the matches attribute of the round.

    Attributes:
        tournament: the tournament taking place.
        round_number: the number of the round taking place.
            Should be 1.
    """
    def __init__(self, tournament: Tournament, round_number: int):
        self.tournament = tournament
        self.round_number = round_number
        self.instantiate_and_store_matches_in_round()

    def request_match_results(self) -> List[str]:
        players_pairs: List[Tuple[Player, Player]] = pairing_for_first_round(
            self.tournament.players_instances)

        results = []
        for i in range(len(players_pairs)):
            player1 = players_pairs[i][0]
            match_result = collect_results(player1.last_name)
            results.append(match_result)

        return results

    def gather_matches_info(self) -> List[Tuple[Player, Player, str, Round]]:
        player_pairs_for_first_round = pairing_for_first_round(
            self.tournament.players_instances)

        match_results = self.request_match_results()

        match_round: Round = self.tournament.rounds[
            f"Round {self.round_number}"]

        match_instances_attributes = []
        for i in range(len(player_pairs_for_first_round)):
            match_players_1: Player = player_pairs_for_first_round[i][0]
            match_players_2: Player = player_pairs_for_first_round[i][1]
            match_result: str = match_results[i]
            match_instances_attributes.append(
                (match_players_1, match_players_2, match_result, match_round))

        return match_instances_attributes

    def instantiate_and_store_matches_in_round(self):
        matches_attributes: List[
            Tuple[Player, Player, str, Round]] = self.gather_matches_info()

        matches_instances: Dict[str, Match] = {}

        for i in range(len(matches_attributes)):
            match_name = f'match{i + 1}'
            match_instance = Match(*matches_attributes[i])
            matches_instances[match_name] = match_instance

        self.tournament.rounds[
            f"Round {self.round_number}"].matches = matches_instances


class CreatingMatchesStoringInSubsequentRounds:
    """Instantiates and stores the matches from a subsequent round.

    When instantiated, the class requests to the user the result of
    all the matches in the round. More specifically, collect_results
    from view.py is called once per match.

    With those results, it instantiates the matches that just took place.
    Then, it stores those instances in the tournament's rounds attribute.

    More precisely, the rounds attribute is a dictionary storing
    all the rounds taking place in the tournament. The
    relevant round is retrieved. The instantiated matches are given
    as the value to the matches attribute of the round.

    Attributes:
        tournament: the tournament taking place.
        round_number: the number of the round taking place.
    """
    def __init__(self, tournament: Tournament, round_number: int):
        self.tournament = tournament
        self.round_number = round_number
        self.instantiate_and_store_matches_in_round()

    def request_match_results(self) -> List[str]:
        ranked_players: List[Player] = avoid_player_meeting_twice(
            self.tournament.players_instances)

        results = []
        for i in range(0, len(ranked_players), 2):
            # in subsequent rounds, pl1 meets pl2, pl3 meets pl4 and so on.
            # Therefore, pl1 from match1 is at index 0
            # pl1 from match 2 is at index 2 and so on.
            player1 = ranked_players[i]
            match_result = collect_results(player1.last_name)
            results.append(match_result)

        return results

    def gather_matches_info(self) -> List[Tuple[Player, Player, str, Round]]:
        ranked_players: List[Player] = avoid_player_meeting_twice(
            self.tournament.players_instances)

        match_results: List[str] = self.request_match_results()

        match_round: Round = self.tournament.rounds[
            f"Round {self.round_number}"]

        match_instances_attributes = []

        iterable_pl_pairs = range(0, len(ranked_players), 2)
        # for each two players there is one match,
        # so if there are 10 players in the tournament, we have 5 matches.
        iterable_results = range(len(ranked_players) // 2)

        for i, j in itertools.zip_longest(iterable_pl_pairs, iterable_results):
            match_players_1 = ranked_players[i]
            match_players_2 = ranked_players[i + 1]
            match_result = match_results[j]
            match_instances_attributes.append((match_players_1,
                                               match_players_2,
                                               match_result,
                                               match_round))

        return match_instances_attributes

    def instantiate_and_store_matches_in_round(self):
        matches_attributes: List[
            Tuple[Player, Player, str, Round]] = self.gather_matches_info()

        matches_instances: Dict[str, Match] = {}

        for i in range(len(matches_attributes)):
            match_name = f'match{i + 1}'
            match_instance = Match(*matches_attributes[i])
            matches_instances[match_name] = match_instance

        self.tournament.rounds[
            f"Round {self.round_number}"].matches = matches_instances
