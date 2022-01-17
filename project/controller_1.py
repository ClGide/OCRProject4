"""
Allowing the dynamic instantiation of the classes defined in models.

This module is organized in two parts. The first
"""


import itertools
import time
from operator import attrgetter
from typing import Dict, List, Tuple

from models import Player, Round, Tournament, Match
from view import collect_player_info, collect_results


def shorten_player_repr(players: List[Player]):
    overriding_method = {
        '__str__': lambda self: self.__getattribute__('last_name')}
    for player in players:
        player.__class__ = type(
            'class_with_shorter_representation_inheriting_from_Player',
            (Player,),
            overriding_method)
        yield player


def lengthen_player_repr(players: List[Player]):
    for player in players:
        player.__class__ = Player
        yield player


def beautify_player_representation(func):
    """

    Args:
        func:

    Returns:

    """

    def wrapper(tournament: Tournament):
        """shortening the player's obj repr to make it more readable"""
        shortened_representation_players = []
        for player in shorten_player_repr(tournament.players_instances):
            shortened_representation_players.append(player)

        func(tournament)

        # restore the object representation for further uses.
        restored_representation_players = []
        for player in lengthen_player_repr(tournament.players_instances):
            restored_representation_players.append(player)

    return wrapper


def pairing_for_first_round(
        players: List[Player]) -> List[Tuple[Player, Player]]:
    half = len(players) // 2
    first_group = players[:half]
    second_group = players[half:]

    pairing = []
    for first_group_pl, second_group_pl in zip(first_group, second_group):
        pairing.append((first_group_pl, second_group_pl))
    return pairing


@beautify_player_representation
def announce_pairing_for_first_round(tournament):
    # should this go directly in the view ? probably not, because there is some method overriding.
    # for a 16 player tournament, pairs[0] should meet pairs[8], pairs[1] should meet pairs[9] and so on.
    pairs = pairing_for_first_round(tournament.players_instances)

    pairing_announcement = ["For the first round"]
    for pair in pairs:
        pairing_announcement.append(f'{pair[0]} will meet {pair[1]}')

    print(f"\nthe matches for the following round are:"
          f"\n{pairing_announcement}\n")

    return pairing_announcement


class CreatingPlayersStoringInTournament:
    """
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
        """formats data from view.py in the view of creating player instances.

        collect_player_info from view.py is called once for every player in
        the tournament. Each tuple can be passed as an argument to the Player
        constructor(preceded by the unpacking *).

        Returns:
            player_info: values describing the player in the tournament.
        """
        players_info = []

        for _ in range(self.players_number):
            player_info = collect_player_info()
            players_info.append(player_info)

        return players_info

    def create_and_store_player_instances(self):

        """Instantiates players with data formatted in requesting_players_info.
        """

        players_info = self.requesting_players_info()

        player_instances: List[Player] = []
        for player_info in players_info:
            player_instance = Player(*player_info)
            player_instances.append(player_instance)

        self.tournament.players_instances = player_instances


class CreatingRoundStoringInTournament:
    """

    Attributes:
        tournament: the tournament in which the round are stored.
        number_of_rounds: the number of rounds taking place in the tournament.

    """
    def __init__(self, tournament: Tournament):
        self.tournament = tournament
        self.number_of_rounds: int = self.tournament.number_of_rounds
        self.store_rounds()

    def instantiate_round(self, round_number: int) -> Tuple[str, Round]:
        # round_number is an attribute of the Round instance we create, not the total number of rounds
        # in the tournament. The variable holding the latter is self.number_of_rounds.

        round_name = f"Round {round_number}"
        # the rounds will last 20 min if time control is set to rapid, 5 min if time control is
        # set to blitz, 3 min if time control is set to bullet.
        round_start_datetime: float = time.time()
        if (self.tournament.time_control == "bullet" or
                self.tournament.time_control == "BULLET"):
            round_end_datetime: float = round_start_datetime + 180
        elif (self.tournament.time_control == "blitz" or
              self.tournament.time_control == "BLITZ"):
            round_end_datetime: float = round_start_datetime + 300
        elif (self.tournament.time_control == "rapid" or
              self.tournament.time_control == "RAPID"):
            round_end_datetime: float = round_start_datetime + 12000
        else:
            raise ValueError("something went wrong with the"
                             " instantiation of the tournament, "
                             "namely it's time-control attribute")
        round_instance = Round(round_name, self.tournament,
                               round_start_datetime, round_end_datetime)

        return round_name, round_instance

    def store_rounds(self):
        round_instances: Dict[str, Round] = {}
        for i in range(self.number_of_rounds):
            # appending the round instance to the dict round_instances
            round_name, round_instance = self.instantiate_round(i + 1)
            if round_instance not in round_instances.values():
                round_instances[round_name] = round_instance

            # catching eventual errors in the process
            else:
                raise ValueError("this round have already been"
                                 " instantiated and stored")
            if len(round_instances) > self.tournament.number_of_rounds:
                raise IndexError("there are more rounds"
                                 " than originally declared")

        # storing the dict containing the rounds in the tournament instance
        self.tournament.rounds = round_instances


class CreatingMatchesStoringInRoundOne:

    """

    Attributes:
        tournament: the tournament in which the matches are taking place.
        round_number: the

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

    def collect_matches_info(self) -> List[Tuple[Player, Player, str, Round]]:

        player_pairs_for_first_round = pairing_for_first_round(
            self.tournament.players_instances)

        match_results = self.request_match_results()

        match_round: Round = self.tournament.rounds[f"Round {self.round_number}"]

        match_instances_attributes = []
        for i in range(len(player_pairs_for_first_round)):
            match_players_1: Player = player_pairs_for_first_round[i][0]
            match_players_2: Player = player_pairs_for_first_round[i][1]
            match_result: str = match_results[i]
            match_instances_attributes.append((match_players_1, match_players_2, match_result, match_round))

        return match_instances_attributes

    def instantiate_and_store_matches_in_round(self):

        matches_attributes: List[
            Tuple[Player, Player, str, Round]] = self.collect_matches_info()

        matches_instances: Dict[str, Match] = {}

        for i in range(len(matches_attributes)):
            match_name = f'match{i + 1}'
            match_instance = Match(*matches_attributes[i])
            matches_instances[match_name] = match_instance

        self.tournament.rounds[
            f"Round {self.round_number}"].matches = matches_instances


class CreatingMatchesStoringInSubsequentRounds:

    """

    Attributes:
        tournament: the tournament in which the matches are taking place.
        round_number: the number of the round in which the matches happen.
            If everything goes fine, should be 1.

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
            # pl1 meets pl2, pl3 meets pl4 and so on in subsequent rounds. Therefore, pl1 from match1 is
            # at index 0, pl1 from match 2 is at index 2 and so on. Keep in mind the algorithms pairing
            # players for the first round and for subsequent rounds are different.
            player1 = ranked_players[i]
            match_result = collect_results(player1.last_name)
            results.append(match_result)

        return results

    def gather_matches_info(self) -> List[Tuple[Player, Player, str, Round]]:

        ranked_players: List[Player] = avoid_player_meeting_twice(
            self.tournament.players_instances)

        match_results: List[str] = self.request_match_results()

        match_round: Round = self.tournament.rounds[f"Round {self.round_number}"]

        match_instances_attributes = []

        iterable_pl_pairs = range(0, len(ranked_players), 2)
        # for each two players there is one match, so if there are 10 players in the tournament, we have 5 matches.
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


def check_match_result(player1: Player, player2: Player, match: Match):

    results: List[
        Tuple[Player, float]] = match.convert_match_result_into_points()

    # We should give the right players the right results
    player1_from_results = results[0][0]
    player2_from_results = results[1][0]
    if player1_from_results != player1 or player2_from_results != player2:
        raise TypeError("the players you entered"
                        " do not match the players from the match")

    return results


def change_players_result_field(player1: Player, player2: Player, match: Match):

    results: List[
        Tuple[Player, float]] = check_match_result(player1, player2, match)

    # Updating the result_field attr of the player
    player1_result = results[0][1]
    player2_result = results[1][1]
    player1.result_field += player1_result
    player2.result_field += player2_result


def update_player_faced_opponents_attr(match: Match):

    player1: Player = match.player1
    player1_opponent: Player = match.player2
    player2: Player = match.player2
    player2_opponent: Player = match.player1

    # for more readability, we will only add the player's last name to the record
    player1_opponent: str = player1_opponent.last_name
    player2_opponent: str = player2_opponent.last_name

    # updating the player's attribute opponents_faced
    player1.add_opponent(player1_opponent)
    player2.add_opponent(player2_opponent)


def update_all_players_attrs_after_round(matches: Dict[str, Match]):

    for match in matches.values():
        player1: Player = match.player1
        player2: Player = match.player2
        change_players_result_field(player1, player2, match)
        update_player_faced_opponents_attr(match)


def rank_players_for_subsequent_round(
        players_ranked_in_previous_round: List[Player]):

    # The goal is to sort by points in decreasing order
    # then, ONLY IF multiple players have an equal number of points, sort those players by rank in ascending order.
    # The sorting is done in two steps. First, I'm negating the rank of each player,
    # then I'm sorting by points and rank in decreasing order

    for player in players_ranked_in_previous_round:
        player.ranking = -player.__getattribute__("ranking")

    players_sorted_by_points_then_rank = sorted(
        players_ranked_in_previous_round,
        key=attrgetter("result_field", 'ranking'),
        reverse=True)

    # Restoring the rank of each player for further uses.
    for player in players_ranked_in_previous_round:
        player.ranking = -player.__getattribute__("ranking")

    # Updating players' rank attribute in accordance
    # to the ranking we just done.
    # remember that index starts at 0 but rankings starts at 1.
    for player in players_sorted_by_points_then_rank:
        player.ranking = players_sorted_by_points_then_rank.index(player) + 1

    return players_sorted_by_points_then_rank


def avoid_player_meeting_twice(
        players_ranked_in_previous_round: List[Player]) -> List[Player]:

    players_ranked_for_subsequent_round = rank_players_for_subsequent_round(
        players_ranked_in_previous_round)

    # rearranging the list in order to avoid duplicate. The logic is the following. If two players are
    # about to meet, and already met, we need to swap one of the players w/ another one located two indexes further
    # in the list.
    p = players_ranked_for_subsequent_round
    for _ in range(len(p)):
        for i in range(len(p)):
            if i == 0:
                continue
            if p[i - 1].last_name in p[i].opponents_faced:
                p[i], p[(i + 2) % (len(p))] = p[(i + 2) % (len(p))], p[i]
    players_paired_without_duplicate = p

    return players_paired_without_duplicate


@beautify_player_representation
def announce_pairing_for_subsequent_round(tournament: Tournament) -> List[str]:

    paired_players: List[Player] = avoid_player_meeting_twice(
        tournament.players_instances)

    p = paired_players
    pairing_announcement = [f'{p[0]} will meet {p[1]}']
    for i in range(len(p)):
        if i == 0 or i == 1 or i == 2:
            continue
        if i >= 3 and (i % 2) != 0:
            pairing_announcement.append(f'{p[i - 1]} will meet {p[i]}')

    print(f"\nthe matches for the following round are:"
          f"\n{pairing_announcement}\n")

    return pairing_announcement


@beautify_player_representation
def announce_ranking(
        tournament: Tournament) -> List[str]:

    ranking_announcement = []
    p = rank_players_for_subsequent_round(tournament.players_instances)
    for i in range(len(p)):
        ranking_announcement.append(f'{p[i]} is number {i + 1}')

    print(f"\nthe final ranking is :\n{ranking_announcement}\n")

    return ranking_announcement
