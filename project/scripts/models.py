"""The classes representing the matches, rounds, players and tournaments.
"""

from __future__ import annotations

import datetime
import json
from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Tuple, Any


@dataclass
class Round:
    """Stores data of a specific round.

    Attributes:
        name_field: the name of the round.
        tournament: the tournament in which the round takes place.
        start_datetime: epoch style representation of the time the
            "round" is instantiated. In the representation of the
            object, the value is converted to human readable time.
        end_datetime: epoch style representation of the time the
            round ended. The value depend on start_datetime and
            the time control chosen by the user when the tournament was
            instantiated. In the representation of the
            object, the value is converted to human readable time.
        matches: contains the Match instances representing all the
            matches that happened during the round.
    """
    name_field: str
    tournament: Tournament
    start_datetime: float = 0
    end_datetime: float = 0
    matches: Optional[Dict[str, Match]] = None

    def serialize_matches(self) -> Union[str, Dict[str, Dict[str, str]]]:
        """converts the Match instances to a serializable format.

        Returns:
            If the matches attribute is not None, converts each Match
            instance into a dictionary : each key represents the attribute name
            while the value represents the attribute value. The func then nests
            those ready-to-be-serialized matches into a dictionary where the
            key represents the number of the match.

            If the matches attribute is None, returns an empty string.
        """
        try:
            serialized_matches = {}
            matches: List[Match] = list(self.matches.values())

            for i in range(len(matches)):
                serialized_matches[str(i + 1)] = matches[i].serialize_match()

            return serialized_matches

        except AttributeError:
            serialized_matches = ""
            return serialized_matches

    def serialize_round(
            self) -> Dict[str, Union[str, Dict[str, Dict[str, str]]]]:
        """converts the round to a serializable format.

        Returns:
            A dictionary where each key represents the attribute name
            while the value represents the attribute value.
            If the matches attribute is None, all the values
            in the dictionary are strings. Otherwise, the last value in
            the dictionary is a dictionary containing the data on all
            the matches that happened during the round.
        """
        serialized_matches = self.serialize_matches()

        serialized_round = {
            "tournament": self.tournament.name,
            "start_datetime": str(self.start_datetime_beautified),
            "end_datetime": str(self.end_datetime_beautified),
            "matches": serialized_matches}

        return serialized_round

    def __str__(self):
        return (f'the {self.name_field} from {self.tournament}. '
                f'Started at {self.start_datetime_beautified}. '
                f'Ended at {self.end_datetime_beautified}')

    def __repr__(self):
        return self.__str__()

    def __post_init__(self):
        """converting start and end epoch time to user-friendly datetime.
         """
        self.start_datetime_beautified = datetime.datetime.fromtimestamp(
            self.start_datetime).replace(microsecond=0)

        self.end_datetime_beautified = datetime.datetime.fromtimestamp(
            self.end_datetime).replace(microsecond=0)


class Player:
    """Stores data on a specific player.

    Attributes:
        last_name: player's last name.
        first_name: player's fist name.
        date_of_birth: player's date of birth.
        sex: player's sex.
        ranking: player's ranking. Unlike for the preceding
            attributes, the value of ranking will evolve
            during the tournament. Idem for the following
            two attributes.
        opponents_faced: last name of the adversaries met by
            the player during the tournament.
        result_field: the number of points earned by the player
            during the tournament.
    """
    def __init__(self, last_name, first_name, date_of_birth, sex, ranking,
                 opponents_faced=None, result_field=0):
        self.last_name: str = last_name
        self.first_name: str = first_name
        self.date_of_birth: Union[datetime.date, str] = date_of_birth
        self.sex: str = sex
        self.ranking: int = ranking
        self.opponents_faced: Optional[List[str]] = opponents_faced
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
            date_in_datetime_type = \
                datetime.datetime.strptime(self.date_of_birth, "%Y/%m/%d")
        except ValueError:
            date_in_datetime_type = \
                datetime.datetime.strptime(self.date_of_birth, "%Y-%m-%d")
        self.date_of_birth = date_in_datetime_type
        self.date_of_birth = self.date_of_birth.date()

    def raise_error_for_incorrect_values(self):
        if not (self.sex == "men"
                or self.sex == "women"
                or self.sex == "other"
                or self.sex == "MEN"
                or self.sex == "WOMEN"
                or self.sex == "OTHER"):
            raise ValueError("the sex of the player can be "
                             "either 'men' or 'women' or 'other'.")

    def serialize_player(self) -> Dict[str, str]:
        """Returns a serializable format of the object.
        """
        serialized_player = \
            {"last_name": self.last_name,
             "first_name": self.first_name,
             "date_of_birth": str(self.date_of_birth),
             "sex": self.sex,
             "ranking": str(self.ranking),
             "opponents_faced": json.dumps(self.opponents_faced),
             "result_field": str(self.result_field)}

        return serialized_player

    def __str__(self):
        return (f"Player({self.last_name}  "
                f"ranking: {self.ranking} | "
                f"result field: {self.result_field} | "
                f"opponents: {self.opponents_faced} ///)")

    def __repr__(self):
        return self.__str__()


@dataclass
class Tournament:
    """Stores all the data about the tournament.

    Attributes:
        name: The name of the tournament.
        venue: the name of the venue.
        date: the date the tournament took place.
        players_number: the number of competitors in the tournament.
        description: anything the manager wants to note about the tournament.
        time_control: bullet, blitz or rapid. Will be used to define the
            duration of the round.
         number_of_rounds: the number of rounds.
         rounds: store all the Round instances that took place in the
            tournament. Those instances store match instances.
        player_instances: stores player instances.
    """
    name: str
    venue: str
    date: Union[str, datetime]
    players_number: int
    description: str
    time_control: str
    number_of_rounds: int = 4
    rounds: Dict[str, Round] = None
    players_instances: List[Player] = None

    def correct_attributes_type(self):
        try:
            date_in_datetime_type = datetime.datetime.strptime(
                self.date, "%Y/%m/%d")
        except ValueError:
            date_in_datetime_type = datetime.datetime.strptime(
                self.date, "%Y-%m-%d")
        self.date = date_in_datetime_type
        self.date = self.date.date()

        self.players_number = int(self.players_number)

        self.number_of_rounds = int(self.number_of_rounds)

    def raise_error_for_incorrect_values(self):
        if not (self.time_control == "bullet"
                or self.time_control == "blitz"
                or self.time_control == "rapid"
                or self.time_control == "BULLET"
                or self.time_control == "BLITZ"
                or self.time_control == "RAPID"):
            raise ValueError("please, enter the name"
                             " of one of the time control proposed")

        if not self.players_number % 2 == 0:
            raise ValueError("please, enter an even number of players."
                             " Otherwise, we cannot assure each "
                             "player a match")

        if self.number_of_rounds > self.players_number:
            raise ValueError("in the swiss-system tournament,"
                             " there shouldn't be more "
                             "rounds than players.")

    def serialize_rounds(
        self
    ) -> Dict[str, Dict[str, Union[str, Dict[str, Dict[str, str]]]]]:
        """Returns a serializable format of all the rounds in the tournament.
        """
        serialized_rounds = {}

        for round in self.rounds.values():
            serialized_round = round.serialize_round()
            serialized_rounds[round.name_field] = serialized_round

        return serialized_rounds

    def serialize_tournament(
            self
    ) -> Dict[str, Union[str,
                         Dict[str, Dict[str,
                                        Union[str, Dict[str, Any]]]]]]:
        """Returns a serializable format of the data stored in the object.
        """
        serialized_rounds = self.serialize_rounds()

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
    """Stores all the data about a specific match.

    The first two attributes store the instances representing
    the two competitors. The result, a single char ("W", "L" or
    "D") needs to be understood from the perspective of player1.
    The last attribute is the instance in which the matches are
    stored.
    """

    player1: Player
    player2: Player
    result: str
    round: Union[Round, str]

    def convert_match_result_into_points(self) -> List[Tuple[Player, float]]:
        """Prepares the data needed to change the player object's
        attributes after the match.

        Returns:
            A list containing two tuples. Each tuple's first item
            is a player instance while the second is the number
            of points earned by that player in the match.
        """
        if self.result == "W" or self.result == "w":
            points_player1 = 1.0
            points_player2 = 0.0
        elif self.result == "L" or self.result == "l":
            points_player1 = 0.0
            points_player2 = 1.0
        elif self.result == "D" or self.result == "d":
            points_player1 = 0.5
            points_player2 = 0.5
        else:
            raise TypeError('please enter "W", "L" or "D"')
        results = [
                (self.player1, points_player1),
                (self.player2, points_player2)]

        return results

    def serialize_match(self) -> Dict[str, str]:
        """Returns a serializable format of the data stored in the object.
        """
        serialized_match = {"player1": self.player1.last_name,
                            "player2": self.player2.last_name,
                            "result": self.result,
                            "round": self.round.name_field}

        return serialized_match
