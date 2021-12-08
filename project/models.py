from dataclasses import dataclass


@dataclass
class Round:
    # the two date times should be clearly epoch date
    name_field: str
    tournament: str
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
    rounds: Round
    players: int
    description: str
    time_control: str
    number_of_rounds: int = 4


@dataclass
class Player:
    # Here again, how should the date_of_birth be stored ?
    # For each of those attrs, some formatting is necessary. Otherwise, it's unuseful info.
    last_name: str
    first_name: str
    date_of_birth: str
    sex: str
    ranking: int
    result_field: int = 0

    def __str__(self):
        return f"Player({self.last_name} ranking: {self.ranking} result field: {self.result_field})"

    def __repr__(self):
        return self.__str__()
