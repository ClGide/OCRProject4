from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Round:
    # the two date times should be clearly epoch date
    name_field: str
    tournament: str  # the right type hint is Tournament, but I would get an error
    dict_of_matches: Dict[str, str] = None  # the third type hint is not str but Match
    start_datetime: int = 0
    end_datetime: int = 0

    def __str__(self):
        return f'the {self.name_field} from {self.tournament}'

    def __repr__(self):
        return self.__str__()


class Player:
    # this class won't be wrapped by dataclass because we don't know how to create class
    # variable with dataclasses.
    # Here again, how should the date_of_birth be stored ?
    # For each of those attrs, some formatting is necessary. Otherwise, it's unuseful info.

    def __init__(self, last_name, first_name, date_of_birth, sex, ranking,
                 opponents_faced=None, result_field=0):
        self.last_name: str = last_name
        self.first_name: str = first_name
        self.date_of_birth: str = date_of_birth
        self.sex: str = sex
        self.ranking: int = ranking
        self.opponents_faced: List[str] = opponents_faced
        self.result_field: int = result_field
        self.avoid_mutable_default_value_issue()
        self.correct_attributes_type()

    def add_opponent(self, value):
        self.opponents_faced.append(value)

    def avoid_mutable_default_value_issue(self):
        self.opponents_faced = []

    def correct_attributes_type(self):
        self.ranking = int(self.ranking)

    def __str__(self):
        return f"Player({self.last_name}  ranking: {self.ranking} | " \
               f"result field: {self.result_field} | opponents: {self.opponents_faced} ///)"

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
    rounds: Dict[str, Round] = None
    # It seems that I should the id of all the player instances in this list.
    list_of_players_instances: List[Player] = None

    def correct_attributes_type(self):
        # the input is necessarily a string. Let's convert the attrs we want to integers.
        self.players_number = int(self.players_number)
        self.number_of_rounds = int(self.number_of_rounds)

    def __str__(self):
        return f'tournament {self.name} that took place in {self.venue}'

    def __repr__(self):
        return self.__str__()

    def __post_init__(self):
        self.correct_attributes_type()


@dataclass
class Match:
    player1: Player
    player2: Player
    result: str
    round: Round

    def convert_match_result_into_points(self):
        # We take the needed letter from the view and we return the results in the correct format
        if self.result == "W":
            points_player1 = 1
            points_player2 = 0
        elif self.result == "L":
            points_player1 = 0
            points_player2 = 1
        elif self.result == "D":
            points_player1 = 0.5
            points_player2 = 0.5
        else:
            print('please enter "W", "L" or "D"')
            raise TypeError
        results = [(self.player1, points_player1), (self.player2, points_player2)]
        return results
