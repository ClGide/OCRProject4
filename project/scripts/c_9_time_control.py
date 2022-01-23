"""Mocks the time the rounds take.

Moreover, it updates the subsequent rounds' start_datetime and end_datetime
attributes.
"""

import time

from models import Tournament, Round


def time_control(tournament: Tournament):
    """Simulates the duration of the rounds.

    Halt the flow of the program. The duration of the halt corresponds
    to the time control chosen by the user when first instantiating
    the tournament.
    Moreover, displays a message informing the user what's happening.

    Args:
        tournament: The tournament that is taking place.

    Raises:
        ValueError: The time control entered by the user do not match
            any of the implemented time control.
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
    except for the first round (rounds from the same tournament cannot start
    and end at the same time). This functions corrects those values.

    In order to do so, the function uses two values, the time_control attribute
    of the tournament and the start and end datetime of the preceding
    round. In other words, we add the duration of a round to the
    start datetime and end datetime of the preceding round.

    Args:
        round_number: the number of the round which start and end datetime
            will be updated.
        tournament: the tournament that is taking place.
    """
    round: Round = tournament.rounds[f"Round {round_number}"]

    s: float = tournament.rounds[f"Round {round_number - 1}"].start_datetime
    e: float = tournament.rounds[f"Round {round_number - 1}"].end_datetime
    rd_duration = tournament.time_control

    if rd_duration == "bullet" or rd_duration == "BULLET":
        round.start_datetime = s + 180
        round.end_datetime = e + 180
    elif rd_duration == "blitz" or rd_duration == "BLITZ":
        round.start_datetime = s + 300
        round.end_datetime = e + 300
    elif rd_duration == "rapid" or rd_duration == "RAPID":
        round.start_datetime = s + 12000
        round.end_datetime = e + 12000

    # Updates the beautified version of the start and end datetime.
    round.__post_init__()

    tournament.rounds[f"Round {round_number}"] = round
