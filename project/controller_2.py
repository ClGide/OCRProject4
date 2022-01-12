import datetime
import json
from operator import attrgetter
from typing import Dict, List, Union

from tinydb import TinyDB, Query

from models import Player, Round, Tournament, Match
from view import what_data_to_read, what_tournament_name, \
    what_table_to_save

db = TinyDB('db.json', indent=4, separators=(',', ': '))


class SaveDataInDB:
    def __init__(self, tournament: Tournament):
        self.what_table_to_save = what_table_to_save()
        self.tournament = tournament

        if self.what_table_to_save == "1":
            self.save_the_tournament(self.tournament.name)
        elif self.what_table_to_save == "2":
            self.save_players_from_tournament()
        elif self.what_table_to_save == "3":
            self.save_the_tournament(self.tournament.name)
            self.save_players_from_tournament()
        elif self.what_table_to_save == "4":
            pass
        else:
            raise ValueError("if you need something, please only enter the number corresponding "
                             "to your need")

    def save_players_from_tournament(self):
        serialized_players: List[Dict[str, str]] = []
        for player in self.tournament.list_of_players_instances:
            serialized_player: Dict[str, str] = player.serialize_player()
            serialized_players.append(serialized_player)

        player_table_name = f"players_competing_in_{self.tournament.name}"
        players_table = db.table(player_table_name)
        players_table.truncate()
        players_table.insert_multiple(serialized_players)

    def save_the_tournament(self, tournament_table_name: str):
        serialized_tournament: Dict[str, Union[str, Dict[str, Dict[str, Union[str, Dict[str, Dict[str, str]]]]]]] = \
            self.tournament.serialize_tournament()

        tournament_table = db.table(tournament_table_name)
        tournament_table.truncate()
        tournament_table.insert(serialized_tournament)


class RequestsMenu:
    def __init__(self, tournament: Tournament):
        self.tournament = tournament
        self.User = Query()
        self.request: str = what_data_to_read()
        self.which_tournament: str = self.check_and_complete_the_request()
        self.search_in_database()

    def check_and_complete_the_request(self) -> str:
        if self.request not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            raise ValueError("please, enter only the number corresponding to your request")

        if self.request in ["1", "2", "6", "7"]:
            which_tournament = what_tournament_name()
            return which_tournament

    def search_in_database(self):
        if self.request == "1":
            self.players_in_a_tournament_ranked_alphabetically()
        elif self.request == "2":
            self.players_ranking_from_a_tournament()
        elif self.request == "3":
            self.all_tournaments_players_ranked_alphabetically()
        elif self.request == "4":
            self.all_tournaments_players_ranking()
        elif self.request == "5":
            self.all_tournaments()
        elif self.request == "6":
            self.all_rounds_in_a_tournament()
        elif self.request == "7":
            self.all_matches_in_a_tournament()

    @staticmethod
    def open_database():
        f = open("db.json")
        database = json.load(f)
        f.close()
        return database

    def find_the_player_table(self) -> List[Dict[str, Dict[str, Union[str, list, float]]]]:
        database = self.open_database()

        player_table_name = f"players_competing_in_{self.which_tournament}"
        serialized_players = [table for table_name, table in database.items()
                              if table_name == player_table_name]
        if not serialized_players:
            raise KeyError("the player table you're searching wasn't found. Please, check your spelling")

        return serialized_players

    def deserialize_players(self) -> List[Player]:
        serialized_players: List[Dict[str, Dict[str, Union[str, list, float]]]] = self.find_the_player_table()
        # serialized_players is a list containing one dictionary
        # containing doc_id(key):player_attributes(value) pairs
        list_of_deserialized_players = []
        for serialized_players_dict in serialized_players:
            for doc_id, player_attributes in serialized_players_dict.items():
                player_attributes["result_field"] = float(player_attributes["result_field"])
                player = Player(**player_attributes)

                opponents_faced = json.loads(player_attributes['opponents_faced'])
                # why not append the entire list directly ? Because an empty list would be appended
                for opponent in opponents_faced:
                    player.opponents_faced.append(opponent)
                list_of_deserialized_players.append(player)

        return list_of_deserialized_players

    def find_the_tournament_table(self) -> \
            List[Dict[str, Union[str, int, Dict[str, Union[str, Dict[str, str]]]]]]:
        database = self.open_database()

        serialized_tournament = [table for table_name, table in database.items() if table_name == self.which_tournament]
        if not serialized_tournament:
            raise KeyError("the player table you're searching wasn't found. Please, check your spelling")

        return serialized_tournament

    def deserialize_tournament(self) -> Tournament:
        serialized_tournament = self.find_the_tournament_table()
        tournament_name = serialized_tournament.name
        # the Table class in TinyDB doesn't implement the __getitem__ method so I need to typecast the table.
        serialized_tournament = list(serialized_tournament)[0]
        tournament_venue = serialized_tournament["venue"]
        tournament_date = serialized_tournament["date"]
        tournament_players_number = serialized_tournament["players number"]
        tournament_description = serialized_tournament["description"]
        tournament_time_control = serialized_tournament["time control"]
        tournament_number_of_rounds = serialized_tournament["number of rounds"]

        tournament_rounds_serialized = serialized_tournament["rounds"]
        tournament_rounds = {}
        for round_name, serialized_round in tournament_rounds_serialized.items():
            deserialized_round = self.deserialize_round(serialized_round)
            tournament_rounds[round_name] = deserialized_round

        deserialized_tournament = Tournament(tournament_name, tournament_venue, tournament_date,
                                             tournament_players_number, tournament_description, tournament_time_control,
                                             tournament_number_of_rounds, tournament_rounds)
        return deserialized_tournament

    def deserialize_round(self, serialized_round):
        round_name_field = serialized_round
        round_tournament = serialized_round["tournament"]

        round_s_datetime = serialized_round["start_datetime"]
        epoch_s_datetime = datetime.datetime.fromisoformat(round_s_datetime).timestamp()

        round_e_datetime = serialized_round["end_datetime"]
        epoch_e_datetime = datetime.datetime.fromisoformat(round_e_datetime).timestamp()

        serialized_matches = serialized_round["matches"]
        round_matches = {}
        for match_number, serialized_match in serialized_matches.items():
            deserialized_match = self.deserialize_matches(serialized_match)
            round_matches[f"match{match_number}"] = deserialized_match
        deserialized_round = Round(round_name_field, round_tournament, epoch_s_datetime,
                                   epoch_e_datetime, round_matches)
        print(f"this is deserialized_round: {deserialized_round}")
        return deserialized_round

    @staticmethod
    def deserialize_matches(serialized_match):
        match_player1 = serialized_match["player1"]
        match_player_2 = serialized_match["player2"]
        match_result = serialized_match["result"]
        match_round = serialized_match["round"]
        deserialized_match = Match(match_player1, match_player_2, match_result, match_round)
        print(f"this is deserialized_match: {deserialized_match}")
        return deserialized_match

    def players_ranking_from_a_tournament(self):
        list_of_deserialized_players = self.deserialize_players()
        sorted_deserialized_players = sorted(list_of_deserialized_players, key=lambda x: x.ranking)
        print(f"this is the return value of players_ranking_from_a_tournament {sorted_deserialized_players}")
        return sorted_deserialized_players

    def players_in_a_tournament_ranked_alphabetically(self):
        list_of_deserialized_players: List[Player] = self.deserialize_players()
        sorted_deserialized_players = sorted(list_of_deserialized_players, key=lambda x: x.last_name)
        print(
            f"this is the return value of players_in_a_tournament_ranked_alphabetically: {sorted_deserialized_players}")
        return sorted_deserialized_players

    def gather_players_from_all_tournaments(self) -> List[Player]:
        # The idea is that all tournaments tables' first key is "venue" while
        # player's first key is "last_name"
        database = self.open_database()

        all_players = []
        for table in database.values():
            for nested_table in table.values():
                if list(nested_table.keys())[0] == "last_name":
                    player_table = nested_table
                    player_table["result_field"] = float(player_table["result_field"])
                    player = Player(**player_table)
                    all_players.append(player)

        return all_players

    def all_tournaments_players_ranking(self):
        # QUESTION: What takes precedence, the DRY principle or the less dependencies principle ?
        all_players = self.gather_players_from_all_tournaments()

        for player in all_players:
            player.ranking = -player.__getattribute__("ranking")
        all_players_ranked = sorted(all_players,
                                    key=attrgetter("result_field", 'ranking'),
                                    reverse=True)
        for player in all_players:
            player.ranking = -player.__getattribute__("ranking")

        return all_players_ranked

    def all_tournaments_players_ranked_alphabetically(self) -> List[Player]:
        all_players: List[Player] = self.gather_players_from_all_tournaments()

        all_players_ranked = sorted(all_players, key=attrgetter("last_name"))

        return all_players_ranked

    def all_tournaments(self):
        database = self.open_database()

        all_tournaments = []
        for table in database.values():
            for nested_table in table.values():
                if list(nested_table.keys())[0] == "venue":
                    tournament_table = nested_table
                    all_tournaments.append(tournament_table)

        return all_tournaments

    def all_matches_in_a_tournament(self):
        deserialized_tournament = self.deserialize_tournament()

        all_matches_in_a_tournament = []
        for round in deserialized_tournament.rounds.values():
            for match in round.dict_of_matches.values():
                all_matches_in_a_tournament.append(match)
        print(f"this is the return value of all_matches_in_a_tournament: {all_matches_in_a_tournament} ")
        return all_matches_in_a_tournament

    def all_rounds_in_a_tournament(self):
        deserialized_tournament = self.deserialize_tournament()
        all_rounds_in_a_tournament = []
        for round in deserialized_tournament.rounds.values():
            all_rounds_in_a_tournament.append(round)
        print(f"this is the return value of all_matches_in_a_tournament: {all_rounds_in_a_tournament} ")
        return all_rounds_in_a_tournament
