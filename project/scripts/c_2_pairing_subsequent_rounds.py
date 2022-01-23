"""Pairs players for subsequent rounds (all rounds except the first).
"""

from operator import attrgetter
from typing import Dict, List, Tuple

from c_1_pairing_first_round import beautify_player_representation
from models import Player, Tournament, Match


def check_match_result(player1: Player, player2: Player, match: Match):
    results: List[
        Tuple[Player, float]] = match.convert_match_result_into_points()

    player1_from_results = results[0][0]
    player2_from_results = results[1][0]
    if player1_from_results != player1 or player2_from_results != player2:
        raise TypeError("the players you entered"
                        " do not match the players from the match")

    return results


def change_players_result_field(player1: Player, player2: Player,
                                match: Match):
    """Makes sure the right players receive the correct number of points.

    Updates the player1 and player2 result_field attribute in accordance
    with the match result.

    Args:
        player1: One of the opponent.
        player2: The other opponent.
        match: The match where the two players competed.

    Raises:
        TypeError: Raised if the first two args do not match the first two
            attributes of the of third arg. Avoids erroneously modifying the
            players result_field attribute.
    """
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

    # for more readability, we will only add the player's
    # last name to the record
    player1_opponent: str = player1_opponent.last_name
    player2_opponent: str = player2_opponent.last_name

    # updating the player's attribute opponents_faced
    player1.add_opponent(player1_opponent)
    player2.add_opponent(player2_opponent)


def update_all_players_attrs_after_round(matches: Dict[str, Match]):
    """Updates players relevant attributes in accordance to match results.

    Modifies the opponents_faced and result_field attribute of the players
    competing in each match of the dictionary.

    Example:
        If the following dictionary is passed as an arg:
        {match1: Match(player1='A', player2='B', result='W', round='round1'))
        the function will add 1 to A's result_field and 0 to B's result_field.
        Also, it will add A's last name to B's opponents_faced attribute and
        B's last name to A's opponents_faced attribute.

    Attributes:
        matches: conceived for the rounds attribute of the relevant tournament.
    """
    for match in matches.values():
        player1: Player = match.player1
        player2: Player = match.player2
        change_players_result_field(player1, player2, match)
        update_player_faced_opponents_attr(match)


def rank_players_for_subsequent_round(
        players_ranked_in_previous_round: List[Player]) -> List[Player]:
    """Ranks the players in accordance to the swiss system algorithm.

    In subsequent rounds the first ranked player competes with the second,
    the third ranked player competes with the fourth, the fifth ranked
    player competes with the sixth and so on.

    Therefore, the goal is to sort by points in decreasing order then, ONLY IF
    multiple players have an equal number of points, sort those players
    by rank in ascending order.

    The sorting is done in two steps. First, negating the rank of each player.
    Second, sorting by points and rank in decreasing order.

    Args:
        players_ranked_in_previous_round: Players instances with their
            result_field attribute up to date.

    Returns: players with their ranking attribute up to date.
    """
    for player in players_ranked_in_previous_round:
        player.ranking = -player.__getattribute__("ranking")

    players_sorted_by_points_then_rank = sorted(
        players_ranked_in_previous_round,
        key=attrgetter("result_field", 'ranking'),
        reverse=True)

    # Restoring the rank of each player for further uses.
    for player in players_ranked_in_previous_round:
        player.ranking = -player.__getattribute__("ranking")

    # Updating the players' rank attribute in accordance
    # to the ranking we just done.
    # remember that index starts at 0 but rankings starts at 1.
    for player in players_sorted_by_points_then_rank:
        player.ranking = players_sorted_by_points_then_rank.index(player) + 1

    return players_sorted_by_points_then_rank


def avoid_player_meeting_twice(
        players_ranked_in_previous_round: List[Player]) -> List[Player]:
    """Avoids as much as possible match duplicate.

    If two players are about to meet, and already met, the function swaps
    one of the players w/ another one located two indexes further in the list.

    Args:
        players_ranked_in_previous_round: Players instances with their
            result_field and opponents_faced attribute up to date

    Returns: The players ranked in order to avoid duplicate.
    """
    players_ranked_for_subsequent_round = rank_players_for_subsequent_round(
        players_ranked_in_previous_round)

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
    """Returns the matches taking place in the subsequent rounds.

    Args:
        tournament: The tournament taking place with the player
            objects' attributes up to date. The players will be retrieved
            from the players_instances attribute of the tournament.
    """
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
    """Returns the rank of each player.

    Conceived to display the ranking at the end of the tournament.

    Args:
        tournament: The tournament that took place.
    """
    ranking_announcement = []
    p = rank_players_for_subsequent_round(tournament.players_instances)
    for i in range(len(p)):
        ranking_announcement.append(f'{p[i]} is number {i + 1}')

    print(f"\nthe final ranking is :\n{ranking_announcement}\n")

    return ranking_announcement
