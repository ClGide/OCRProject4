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



class Player:
    # this class won't be wrapped by dataclass because we don't know how to create class
    # variable with dataclasses.
    # Here again, how should the date_of_birth be stored ?
    # For each of those attrs, some formatting is necessary. Otherwise, it's unuseful info.

    def __init__(self, last_name, first_name, date_of_birth, sex, ranking,
                 opponents_faced=[], result_field=0):
        self.last_name: str = last_name
        self.first_name: str = first_name
        self.date_of_birth: str = date_of_birth
        self.sex: str = sex
        self.ranking: int = ranking
        self.opponents_faced: List[int] = opponents_faced
        self.result_field: int = result_field
        Player.instances.append(self)

    def add(self, value):
        self.opponents_faced.append(value)

    def __str__(self):
        return f"Player({self.last_name} | ranking: {self.ranking} | " \
               f"result field: {self.result_field} | opponents: {self.opponents_faced} |||)"

    def __repr__(self):
        return self.__str__()


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
    # It seems that I should the id of all the player instances in this list.
    list_of_players_instances: List[Player] = None


@dataclass
class Match:
    player1: Player
    player2: Player
    result: str
    round: Round
