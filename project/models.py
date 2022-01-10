import datetime
import json
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Round:
    # the two date times should be clearly epoch date
    name_field: str
    tournament: str  # the right type hint is Tournament, but I would get an error
    start_datetime: float = 0
    end_datetime: float = 0
    dict_of_matches: Dict[str, str] = None  # the third type hint is not str but Match

    def serialize_matches(self):
        serialized_matches = {}
        matches = list(self.dict_of_matches.values())
        for i in range(len(matches)):
            serialized_matches[str(i+1)] = matches[i].serialize_match()
        return serialized_matches

    def serialize_round(self):
        serialized_matches = self.serialize_matches()
        serialized_round = {
            "tournament": self.tournament.name,
            "start_datetime": str(self.start_datetime_beautified),
            "end_datetime": str(self.end_datetime_beautified),
            "matches": serialized_matches}
        return serialized_round

    def __str__(self):
        return f'the {self.name_field} from {self.tournament}. ' \
               f'Started at {self.start_datetime_beautified}. ' \
               f'Ended at {self.end_datetime_beautified}'

    def __repr__(self):
        return self.__str__()

    def __post_init__(self):
        # converting epoch time start and end datetime to user-friendly datetime.
        self.start_datetime_beautified = datetime.datetime.fromtimestamp(self.start_datetime).replace(microsecond=0)
        self.end_datetime_beautified = datetime.datetime.fromtimestamp(self.end_datetime).replace(microsecond=0)


class Player:
    # this class won't be wrapped by dataclass because we don't know how to create class
    # variable with dataclasses.
    # Here again, how should the date_of_birth be stored ?
    # For each of those attrs, some formatting is necessary. Otherwise, it's unuseful info.

    def __init__(self, last_name, first_name, date_of_birth, sex, ranking,
                 opponents_faced=None, result_field=0):
        self.last_name: str = last_name
        self.first_name: str = first_name
        self.date_of_birth: datetime.date = date_of_birth
        self.sex: str = sex
        self.ranking: int = ranking
        self.opponents_faced: List[str] = opponents_faced
        self.result_field: float = result_field
        self.avoid_mutable_default_value_issue()
        self.correct_attributes_type()
        self.raise_error_for_incorrect_values()

    def add_opponent(self, value):
        self.opponents_faced.append(value)

    def avoid_mutable_default_value_issue(self):
        self.opponents_faced = []

    def correct_attributes_type(self):
        self.ranking = int(self.ranking)
        try:
            date_in_datetime_type = datetime.datetime.strptime(self.date_of_birth, "%Y/%m/%d")
        except ValueError:
            date_in_datetime_type = datetime.datetime.strptime(self.date_of_birth, "%Y-%m-%d")
        self.date_of_birth = date_in_datetime_type
        self.date_of_birth = self.date_of_birth.date()

    def raise_error_for_incorrect_values(self):
        if not (self.sex == "men" or self.sex == "women" or self.sex == "other" or
                self.sex == "MEN" or self.sex == "WOMEN" or self.sex == "OTHER"):
            raise ValueError("the sex of the player can be either men or women or other ")

    def serialized_player(self):
        serialized_player = {"last_name": self.last_name,
                             "first_name": self.first_name,
                             "date_of_birth": str(self.date_of_birth),
                             "sex": self.sex,
                             "ranking": str(self.ranking),
                             "opponents_faced": json.dumps(self.opponents_faced),
                             "result_field": str(self.result_field)}

        return serialized_player

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
        try:
            date_in_datetime_type = datetime.datetime.strptime(self.date, "%Y/%m/%d")
        except ValueError:
            date_in_datetime_type = datetime.datetime.strptime(self.date, "%Y-%m-%d")
        self.date = date_in_datetime_type
        self.date = self.date.date()

        self.players_number = int(self.players_number)

        self.number_of_rounds = int(self.number_of_rounds)

    def raise_error_for_incorrect_values(self):
        if not (self.time_control == "bullet" or self.time_control == "blitz" or self.time_control == "rapid" or
                self.time_control == "BULLET" or self.time_control == "BLITZ" or self.time_control == "RAPID"):
            raise ValueError("please, enter the name of one of the time control proposed")

        if not self.players_number % 2 == 0:
            raise ValueError("please, enter an even number of players. Otherwise, we cannot assure each player a match")

        if self.number_of_rounds > self.players_number:
            raise ValueError("in the swiss-system tournament, there shouldn't be more "
                  "rounds than players.")

    def serialize_rounds(self):
        serialized_rounds = {}
        for round in self.rounds.values():
            serialized_round = round.serialize_round()
            serialized_rounds[round.name_field] = serialized_round
        return serialized_rounds

    def serialize_tournament(self):
        serialized_rounds = self.serialize_rounds()
        print(f"this is serialized_rounds in Tournament: {serialized_rounds}")
        serialized_tournament = {
            "venue": self.venue,
            "date": str(self.date),
            "players number": str(self.players_number),
            "description": self.description,
            "time control": self.time_control,
            "number of rounds": str(self.number_of_rounds),
            "rounds": serialized_rounds
        }
        return serialized_tournament

    def __str__(self):
        return f'tournament {self.name} that took place in {self.venue}'

    def __repr__(self):
        return self.__str__()

    def __post_init__(self):
        self.correct_attributes_type()
        self.raise_error_for_incorrect_values()


@dataclass
class Match:
    player1: Player
    player2: Player
    result: str
    round: Round

    def convert_match_result_into_points(self):
        # We take the needed letter from the view and we return the results in the correct format
        if self.result == "W" or self.result == "w":
            points_player1 = 1
            points_player2 = 0
        elif self.result == "L" or self.result == "l":
            points_player1 = 0
            points_player2 = 1
        elif self.result == "D" or self.result == "d":
            points_player1 = 0.5
            points_player2 = 0.5
        else:
            raise TypeError('please enter "W", "L" or "D"')
        results = [(self.player1, points_player1), (self.player2, points_player2)]
        return results

    def serialize_match(self):
        serialized_match = {"player1": self.player1.last_name,
                            "player2": self.player2.last_name,
                            "result": self.result,
                            "round": self.round.name_field}
        return serialized_match

