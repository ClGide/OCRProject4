"""Allows the dynamic instantiation of all the rounds in the tournament.
"""

import time
from typing import Dict, Tuple

from models import Round, Tournament


class CreatingRoundStoringInTournament:
    """Instantiates and stores all the rounds in the tournament.

    When instantiated, the class will create all the round objects from the
    the tournament. The start and end datetime of the rounds are calculated
    based on two values. The time the rounds are instantiated and
    the tournament time_control attribute.

    The rounds matches attribute will be let to the default
    value, meaning None.

    The rounds are stored in the tournament's rounds attribute.

    Attributes:
        tournament: the tournament in which the round are stored.
        number_of_rounds: the number of rounds taking place in the tournament.

    Raises:
        IndexError: if a round that should not happen in the tournament was
            being created. E.g. the tournament should have 4 rounds and a 5th
            round was being instantiated.
        ValueError: if the round already have been created and stored
            in the tournament.
    """
    def __init__(self, tournament: Tournament):
        self.tournament = tournament
        self.number_of_rounds: int = self.tournament.number_of_rounds
        self.store_rounds()

    def instantiate_round(self, round_number: int) -> Tuple[str, Round]:
        # round_number is an attribute of the round instance we create,
        # not the total number of rounds
        # in the tournament. The variable holding the
        # latter is self.number_of_rounds.

        round_name = f"Round {round_number}"
        # the rounds will last 20 min if time control is set to rapid,
        # 5 min if time control is
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
            # double-check. The error should be triggered previously
            # when the tournament is instantiated.
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
