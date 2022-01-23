"""Pairs players for the first round.
"""

from typing import List, Tuple, Callable

from models import Player, Tournament


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


def beautify_player_representation(func: Callable) -> Callable:
    """Modifies the representation of the player object.

    Decorator overriding the __repr__ method of the object. Makes it more
    readable for the user. After the decorated function returns its value,
    the __repr__ method of the objects is set back to original.

    Args:
        func: A function taking a tournament instance as sole argument. The
            decoration only makes sense if the function
            displays data about the player objects contained in the
            player_instances attribute of the tournament.

    Returns: Decorated function.

    """
    def wrapper(tournament: Tournament):
        # shortening the player's obj repr to make it more readable.
        shortened_representation_players = []
        for player in shorten_player_repr(tournament.players_instances):
            shortened_representation_players.append(player)

        func(tournament)

        # restoring the object representation for further uses.
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
def announce_pairing_for_first_round(tournament: Tournament) -> List[str]:
    """Displays the matches that will take place in the first round.

    Player pairing is done according to the swiss-system algorithm.
    For a 16-player tournament, the first ranked player should meet the ninth
    ranked player, the second ranked player should meet the tenth ranked
    player and so on.

    The function is called from view_display.py.

    Args:
        tournament: The tournament that is taking place.

    Returns: The matches that will take place.
    """
    pairs = pairing_for_first_round(tournament.players_instances)

    pairing_announcement = ["For the first round"]
    for pair in pairs:
        pairing_announcement.append(f'{pair[0]} will meet {pair[1]}')

    print(f"\nthe matches for the following round are:"
          f"\n{pairing_announcement}\n")

    return pairing_announcement
