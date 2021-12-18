from dataclasses import dataclass
from dataclasses import field
from typing import List



@dataclass
class Round:
    # the two date times should be clearly epoch date
    name_field: str
    tournament: str  # Tournament instance, but I would get an error
    list_of_matches: list = None
    start_datetime: int = 0
    end_datetime: int = 0


@dataclass
class Tournament:
    # for date, there are four possibilities - str, int(epoch date) or list of str or
    # meaningful list of successful int.
    # player should be a list of indices and I still don't know what time control should do

    name: str
    venue: str
    date: str
    # The tournament should be defined just before the rounds and each time we define a new round
    # with the relevant name of the tournament, we need to append a round to the tournament. We need to
    # take the tournament name from the view and give it to the rounds creator.
    players_number: int
    description: str
    time_control: str
    number_of_rounds: int = 4
    rounds: List[Round] = None

@dataclass
class Player:
    # Here again, how should the date_of_birth be stored ?
    # For each of those attrs, some formatting is necessary. Otherwise, it's unuseful info.

    last_name: str
    first_name: str
    date_of_birth: str
    sex: str
    ranking: int
    opponents_faced: List[int] = field(default_factory=list)
    result_field: int = 0

    def add(self, value):
        self.opponents_faced.append(value)


    def __str__(self):
        return f"Player({self.last_name} | ranking: {self.ranking} | " \
               f"result field: {self.result_field} | opponents: {self.opponents_faced} |||)"

    def __repr__(self):
        return self.__str__()

@dataclass
class Match:
    player1: Player
    player2: Player
    result: str
    round: Round
