import datetime
import itertools
import json
import time
import calendar
from operator import attrgetter
from typing import Dict, List

import tinydb.table
from tinydb import TinyDB, Query

from models import Player, Round, Tournament, Match
from view import insert_player_info, insert_tournament_info, insert_results, what_request, requesting_tournament_name, \
    requesting_table_to_save_first_round, requesting_player_table_name, requesting_table_to_save_subsequent_round


class CreatingPlayerStoringInTournament:
    """
    The number of players per tournament is inputted by the manager at the start. It is stored
    as an attribute of the tournament instance. We use that number to request the info needed to
    instantiate all the players. The func insert_player_info() is in the VIEW.
    """

    def __init__(self, tournament: Tournament):
        self.tournament = tournament
        self.players_number = tournament.players_number
        self.create_and_store_player_instances()

    def requesting_players_info(self):
        players = []
        for _ in range(self.players_number):
            player = insert_player_info()
            players.append(player)
        return players

    def create_and_store_player_instances(self):
        """Q: this func does two things, should I split it or is it short enough ?"""

        players_info = self.requesting_players_info()

        player_instances = []
        for player_info in players_info:
            player_instance = Player(*player_info)
            player_instances.append(player_instance)

        tournament.list_of_players_instances = player_instances


""" 
Below comes a useful decorator aiming at beautifying the info sent to the VIEW.

Q : Dunder method overriding at instance level is not very readable. And there is a more readable workaround 
to beautify the info sent to the VIEW. I could extract a separate list of player names by 
looping through the list of player instances. However, those names will just be strings, acting upon them 
won't have any effect on the player instances. That means that I'll have to loop through both lists (the one 
with the names and the one with the instances) each time I want to act upon/compute something with 
those instances and send the resulting info to the VIEW. I don't know if that would be clearer.  
 """


def shorten_player_representation(players: List[Player]):
    overriding_method = {'__str__': lambda self: self.__getattribute__('last_name')}
    for player in players:
        player.__class__ = type('class_with_shorter_representation_inheriting_from_Player',
                                (Player,),
                                overriding_method)
        yield player


def lengthen_player_representation(players: List[Player]):
    for player in players:
        player.__class__ = Player
        yield player


def beautify_player_representation(func):
    def wrapper():
        # shortening the representation of each player in order to make it suitable for the view.
        shortened_representation_players = []
        for player in shorten_player_representation(tournament.list_of_players_instances):
            shortened_representation_players.append(player)

        func()

        # restore the object representation for further uses.
        restored_representation_players = []
        for player in lengthen_player_representation(tournament.list_of_players_instances):
            restored_representation_players.append(player)

    return wrapper


def pairing_for_first_round(players: List[Player]):
    half = len(players) // 2
    first_group = players[:half]
    second_group = players[half:]

    pairing = []
    for first_group_player, second_group_player in zip(first_group, second_group):
        pairing.append((first_group_player, second_group_player))
    return pairing


"""
Q: MVC > reusability ? 
For the function to be reusable, I should give the list of players as an argument. However, 
the return value needs to be displayed in the VIEW. And I want to import as little things
as possible (here, the list of players) from the MODEL to the VIEW (risk of circular imports). 
Therefore, I think the best is to get the list of players from the global scope. 
In this way, when I call the function from the VIEW, I don't have to give it any argument. Another 
advantage of this choice is that it keeps the VIEW dumb.  
"""


@beautify_player_representation
def announce_pairing_for_first_round():
    # should this go directly in the view ? probably not, because there is some method overriding.
    # for a 16 player tournament, pairs[0] should meet pairs[8], pairs[1] should meet pairs[9] and so on.
    pairs = pairing_for_first_round(tournament.list_of_players_instances)

    pairing_announcement = ["For the first round"]
    for pair in pairs:
        pairing_announcement.append(f'{pair[0]} will meet {pair[1]}')

    return pairing_announcement


""" 
The following is a flow proposal : 
1) program announces the matches for the first round.
* here some time control takes place* 
2) matches took place and the manager inserted the result (in the VIEW).
3) program instantiates the matches and the corresponding round. 
3) the program pairs the player with the swiss algorithm for subsequent rounds.

We also need to give each round a start and end datetime that will be set depending on two criteria. 
First, the number of expected rounds AND second, the time_control property of the corresponding Tournament instance.
EXTRA: For more realism, we can even program a 1-min break between rounds.

The round should be instantiated just before we request the match results. 
It's dict_of_matches default arg will be given a non-None value afterwards. 
the Match instances should be instantiated just after the manager wrote the results.  
"""


class CreatingRoundStoringInTournament:
    def __init__(self, tournament):
        self.tournament = tournament
        self.number_of_rounds = self.tournament.number_of_rounds
        self.store_rounds()

    def instantiate_round(self, round_number: int):
        # round_number is an attribute of the Round instance we create, not the total number of rounds
        # in the tournament. The variable holding the later is self.number_of_rounds.

        """Q: the inconvenience of dynamically creating an obj is that we recreate the
        obj each time you need it. Given that we store rounds in the Tournament instance,
        and maybe in other locations, I hope this recreation doesn't create bugs."""

        round_name = f"Round {round_number}"
        # the rounds will last 20 min if time control is set to rapid, 5 min if time control is
        # set to blitz, 3 min if time control is set to bullet.
        round_start_datetime = time.time()
        if self.tournament.time_control == "bullet" or self.tournament.time_control == "BULLET":
            round_end_datetime = round_start_datetime + 180
        elif self.tournament.time_control == "blitz" or self.tournament.time_control == "BLITZ":
            round_end_datetime = round_start_datetime + 300
        elif self.tournament.time_control == "rapid" or self.tournament.time_control == "RAPID":
            round_end_datetime = round_start_datetime + 12000
        else:
            raise ValueError("something went wrong with the instantiation of the tournament, "
                             "namely it's time-control attribute")
        round_instance = Round(round_name, self.tournament, round_start_datetime, round_end_datetime)

        return round_name, round_instance

    def store_rounds(self):
        round_instances = {}
        for i in range(self.number_of_rounds):
            # appending the round instance to the dict round_instances
            round_name, round_instance = self.instantiate_round(i + 1)
            if round_instance not in round_instances.values():
                round_instances[round_name] = round_instance

            # catching eventual errors in the process
            else:
                raise ValueError("this round have already been instantiated and stored")
            if len(round_instances) > tournament.number_of_rounds:
                raise IndexError("there are more rounds than originally declared")
        # storing the dict containing the rounds in the tournament instance
        tournament.rounds = round_instances


class CreatingMatchStoringInRoundOne:
    """
    After using the pairing_for_first_round func to announce the matches to the manager, we are
    reusing it to ask for the results of those matches. We use those results and other info already
    inputted by the manager to instantiate the matches and store them in the tournament object.
    the func insert_results() is in the VIEW.
    """

    def __init__(self, round_number: int):
        self.round_number = round_number
        self.instantiate_and_store_matches_in_round()

    @staticmethod
    def request_match_results():
        players_pairs = pairing_for_first_round(tournament.list_of_players_instances)

        results = []
        for i in range(len(players_pairs)):
            player1 = players_pairs[i][0]
            match_result = insert_results(player1.last_name)
            results.append(match_result)

        return results

    def collect_matches_info(self):
        player_pairs_for_first_round = pairing_for_first_round(tournament.list_of_players_instances)

        match_results = self.request_match_results()

        match_round = tournament.rounds[f"Round {self.round_number}"]

        match_instances_attributes = []
        for i in range(len(player_pairs_for_first_round)):
            match_players_1 = player_pairs_for_first_round[i][0]
            match_players_2 = player_pairs_for_first_round[i][1]
            match_result = match_results[i]
            match_instances_attributes.append((match_players_1, match_players_2, match_result, match_round))

        return match_instances_attributes

    def instantiate_and_store_matches_in_round(self):
        """Q: should this func be refactored (does two things), but it also seems to be a short func"""
        matches_attributes = self.collect_matches_info()
        matches_instances = {}

        for i in range(len(matches_attributes)):
            match_name = f'match{i + 1}'
            match_instance = Match(*matches_attributes[i])
            matches_instances[match_name] = match_instance

        tournament.rounds[f"Round {self.round_number}"].dict_of_matches = matches_instances


class CreatingMatchStoringInSubsequentRounds:

    def __init__(self, round_number: int):
        self.round_number = round_number
        self.instantiate_and_store_matches_in_round()

    @staticmethod
    def request_match_results():
        # the function returns a tuple of length 2, we only need the first item, the player pairs.
        ranked_players = avoid_player_meeting_twice(tournament.list_of_players_instances)

        results = []
        for i in range(0, len(ranked_players), 2):
            # pl1 meets pl2, pl3 meets pl4 and so on in subsequent rounds. Therefore, pl1 from match1 is
            # at index 0, pl1 from match 2 is at index 2 and so on.
            player1 = ranked_players[i]
            match_result = insert_results(player1.last_name)
            results.append(match_result)

        return results

    def collect_matches_info(self):
        ranked_players = avoid_player_meeting_twice(tournament.list_of_players_instances)

        match_results = self.request_match_results()

        match_round = tournament.rounds[f"Round {self.round_number}"]

        match_instances_attributes = []

        iterable_player_pairs = range(0, len(ranked_players), 2)
        # for each two players there is one match, so if there are 10 players in the tournament, we have 5 matches.
        iterable_match_result = range(len(ranked_players) // 2)

        for i, j in itertools.zip_longest(iterable_player_pairs, iterable_match_result):
            match_players_1 = ranked_players[i]
            match_players_2 = ranked_players[i + 1]
            match_result = match_results[j]
            match_instances_attributes.append((match_players_1, match_players_2, match_result, match_round))

        return match_instances_attributes

    def instantiate_and_store_matches_in_round(self):
        """Q: should this func be refactored (does two things), but it also seems to be a short func"""
        matches_attributes = self.collect_matches_info()
        matches_instances = {}

        for i in range(len(matches_attributes)):
            match_name = f'match{i + 1}'
            match_instance = Match(*matches_attributes[i])
            matches_instances[match_name] = match_instance

        tournament.rounds[f"Round {self.round_number}"].dict_of_matches = matches_instances


"""
below we update all the players attributes in accordance to the result of the round that just happened.
Even if I use procedural style, I think it is clear enough to not be rewritten into OOP style. 
"""


def check_match_result(player1: Player, player2: Player, match: Match):
    # We take the results in the right format from the request_match_results match method.
    results = match.convert_match_result_into_points()

    # We should give the right players the right results
    player1_from_results = results[0][0]
    player2_from_results = results[1][0]
    if player1_from_results != player1 or player2_from_results != player2:
        raise TypeError("the players you entered do not match the players from the match")

    return results


def change_players_result_field(player1: Player, player2: Player, match: Match):
    results = check_match_result(player1, player2, match)

    # Updating the result_field attr of the player
    player1_result = results[0][1]
    player2_result = results[1][1]
    player1.result_field += player1_result
    player2.result_field += player2_result


def update_player_faced_opponents_attr(match: Match):
    player1 = match.player1
    player1_opponent = match.player2
    player2 = match.player2
    player2_opponent = match.player1

    # for more readability, we will only add the player's last name to the record
    player1_opponent = player1_opponent.last_name
    player2_opponent = player2_opponent.last_name

    # updating the player's attribute opponents_faced
    player1.add_opponent(player1_opponent)
    player2.add_opponent(player2_opponent)


def update_all_players_attrs_after_round(matches: Dict[str, Match]):
    for match in matches.values():
        player1 = match.player1
        player2 = match.player2
        change_players_result_field(player1, player2, match)
        update_player_faced_opponents_attr(match)


"""
the below operations reorder the ranks to transition from one round to the other. 
"""


def rank_players_for_subsequent_round(players_ranked_in_previous_round: List[Player]):
    # I need to figure out a more elegant way to sort by points in decreasing order
    # then, ONLY IF players have an equal number of points, by rank in ascending order.
    # Right now, the sorting is done in two steps. First, I'm negating the rank of each player,
    # then I'm sorting by points and rank in decreasing order

    for player in players_ranked_in_previous_round:
        player.ranking = -player.__getattribute__("ranking")

    players_sorted_by_points_then_rank = sorted(players_ranked_in_previous_round,
                                                key=attrgetter("result_field", 'ranking'),
                                                reverse=True)

    # Restoring the rank of each player for further uses.
    for player in players_ranked_in_previous_round:
        player.ranking = -player.__getattribute__("ranking")

    # Updating players' rank attribute in accordance to the ranking we just done.
    # remember that index starts at 0 but rankings starts at 1.
    for player in players_sorted_by_points_then_rank:
        player.ranking = players_sorted_by_points_then_rank.index(player) + 1

    return players_sorted_by_points_then_rank


def avoid_player_meeting_twice(players_ranked_in_previous_round: list):
    players_ranked_for_subsequent_round = rank_players_for_subsequent_round(players_ranked_in_previous_round)
    p = players_ranked_for_subsequent_round

    # rearranging the list in order to avoid duplicate. The logic is the following. If two players are
    # about to meet, we need to swap one of the players w/ another one located two indexes further in the list.
    for _ in range(len(p)):
        for i in range(len(p)):
            if i == 0:
                continue
            if p[i - 1].last_name in p[i].opponents_faced:
                print("there were some rearrangements in order to avoid duplicate")
                p[i], p[(i + 2) % (len(p))] = p[(i + 2) % (len(p))], p[i]

    paired_players = p
    return paired_players


@beautify_player_representation
def announce_pairing_for_subsequent_round():
    paired_players = avoid_player_meeting_twice(tournament.list_of_players_instances)
    p = paired_players

    pairing_announcement = [f'{p[0]} will meet {p[1]}']

    for i in range(len(p)):
        if i == 0 or i == 1 or i == 2:
            continue
        if i >= 3 and (i % 2) != 0:
            pairing_announcement.append(f'{p[i - 1]} will meet {p[i]}')

    return pairing_announcement


"""Now that the matches from round 1 took place, the following should happen: 
1) manager inserts the results 
2) program creates the corresponding Match instances and Round instance
3) program ranks the players and announces the matches 
"""

# manager inputs the results.
# creating another set of matches will be a fun endeavour.
# Because the return value is ONE object, there seems to necessarily be ONE func.
# that func needs to keep track of the number of the round AND
# of all the matches already created so it doesn't override a previous Match instance.


""" All good for the second round too. Let's create a func that announces the current rank. 
"""


@beautify_player_representation
def announce_ranking():
    ranking_announcement = []
    p = rank_players_for_subsequent_round(tournament.list_of_players_instances)
    for i in range(len(p)):
        ranking_announcement.append(f'{p[i]} is number {i + 1}')
    print(ranking_announcement)
    return ranking_announcement


def time_control(tournament):
    # this function simulates the time each round takes depending on the time control chose
    # by the manager when instantiating the tournament.
    if tournament.time_control == "bullet" or tournament.time_control == "BULLET":
        return time.sleep(10)
    elif tournament.time_control == "blitz" or tournament.time_control == "BLITZ":
        return time.sleep(300)
    elif tournament.time_control == "rapid" or tournament.time_control == "RAPID":
        return time.sleep(12000)
    else:
        raise ValueError("something went wrong with the instantiation of the tournament, "
                         "namely it's time-control attribute")


db = TinyDB('db.json', indent=4, separators=(',', ': '))


class SaveDataInDB:
    def __init__(self, tournament: Tournament):
        self.what_table_to_save_first_round = requesting_table_to_save_first_round()
        self.what_table_to_save_subsequent_round = requesting_table_to_save_subsequent_round()
        self.tournament = tournament

        if not SUBSEQUENT_ROUNDS:
            if self.what_table_to_save_subsequent_round == "1":
                self.what_table_to_save_subsequent_round()
            elif self.what_table_to_save_subsequent_round == "2":
                self.what_table_to_save_subsequent_round()
            else:
                raise ValueError("if you need something, please only enter the integer corresponding "
                                 "to your need")

        else:
            if self.what_table_to_save_first_round == "1":
                self.save_the_tournament(self.tournament.name)
            elif self.what_table_to_save_first_round == "2":
                self.save_players_from_tournament()
            elif self.what_table_to_save_first_round == "3":
                self.save_the_tournament(self.tournament.name)
                self.save_players_from_tournament()
            elif self.what_table_to_save_first_round == "4":
                pass
            else:
                raise ValueError("if you need something, please only enter the integer corresponding "
                                 "to your need")

    def save_players_from_tournament(self):
        serialized_players = []
        for player in self.tournament.list_of_players_instances:
            serialized_player = player.serialized_player()
            serialized_players.append(serialized_player)

        player_table_name = f"players_competing_in_{self.tournament.name}"
        players_table = db.table(player_table_name)
        players_table.truncate()
        players_table.insert_multiple(serialized_players)

    def save_the_tournament(self, tournament_table_name: str):
        serialized_tournament = self.tournament.serialize_tournament()
        tournament_table = db.table(tournament_table_name)
        tournament_table.truncate()
        tournament_table.insert(serialized_tournament)


class RequestsMenu:
    def __init__(self, tournament: Tournament):
        self.tournament = tournament
        self.User = Query()
        self.request = what_request()
        self.which_tournament = self.check_and_complete_the_request()
        self.search_in_database()

    def check_and_complete_the_request(self):
        if self.request not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            raise ValueError("please, enter only the integer corresponding to your request")

        if self.request in ["1", "2", "6", "7"]:
            which_tournament = requesting_tournament_name()
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

    def find_the_player_table(self):
        # Q: The if-else statement is probably useless, I could do the query anyway. However, I am
        # wondering if it is faster to make the query only if necessary. What's your opinion ?
        if self.which_tournament == self.tournament.name:
            player_table_name = f"players_competing_in_{self.tournament.name}"
            serialized_players = db.table(player_table_name)

        elif self.which_tournament != self.tournament.name:
            database = self.open_database()
            player_table_name = f"players_competing_in_{self.which_tournament}"
            serialized_players = [table for table_name, table in database.items()
                                  if table_name == player_table_name]
            if not serialized_players:
                raise KeyError("the player table you're searching wasn't found. Please, check your spelling")

        return serialized_players

    def deserialize_players(self):
        serialized_players = self.find_the_player_table()

        try:
            list_of_deserialized_players = []

            for serialized_player in serialized_players:
                last_name = serialized_player['last_name']
                first_name = serialized_player['first_name']
                date_of_birth = serialized_player['date_of_birth'].replace("-", "/")
                sex = serialized_player['sex']
                ranking = int(serialized_player['ranking'])
                opponents_faced = []
                result_field = float(serialized_player["result_field"])

                player = Player(last_name, first_name, date_of_birth, sex, ranking, opponents_faced, result_field)

                opponents_faced = json.loads(serialized_player['opponents_faced'])
                # why not append the entire list directly ? Because an empty list would be appended
                for opponent in opponents_faced:
                    player.opponents_faced.append(opponent)
                list_of_deserialized_players.append(player)

                return list_of_deserialized_players

        except KeyError:
            list_of_deserialized_players = []

            # serialized_players is a list containing one dictionary
            # containing doc_id(key):player_attributes(value) pairs
            for serialized_players_dict in serialized_players:
                for doc_id, player_attributes in serialized_players_dict.items():
                    player_attributes["result_field"] = float(player_attributes["result_field"])
                    player = Player(**player_attributes)
                    list_of_deserialized_players.append(player)

            return list_of_deserialized_players

    def find_the_tournament_table(self):
        if self.which_tournament == self.tournament.name:
            serialized_tournament = db.table(self.tournament.name)

        elif self.which_tournament != self.tournament.name:
            database = self.open_database()
            serialized_tournament = [table for table_name, table in database.items() if table_name == self.which_tournament]
            if not serialized_tournament:
                raise KeyError("the player table you're searching wasn't found. Please, check your spelling")

        return serialized_tournament

    def deserialize_tournament(self):
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
        print(f"this is deserialized_tournament as returned by deserialize_tournament: {deserialized_tournament}")
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
        list_of_deserialized_players = self.deserialize_players()
        sorted_deserialized_players = sorted(list_of_deserialized_players, key=lambda x: x.last_name)
        print(
            f"this is the return value of players_in_a_tournament_ranked_alphabetically: {sorted_deserialized_players}")
        return sorted_deserialized_players

    def collect_players_from_all_tournaments(self):
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
        all_players = self.collect_players_from_all_tournaments()

        for player in all_players:
            player.ranking = -player.__getattribute__("ranking")
        all_players_ranked = sorted(all_players,
                                    key=attrgetter("result_field", 'ranking'),
                                    reverse=True)
        for player in all_players:
            player.ranking = -player.__getattribute__("ranking")

        return all_players_ranked

    def all_tournaments_players_ranked_alphabetically(self):
        all_players = self.collect_players_from_all_tournaments()

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


if __name__ == "__main__":
    """ 
    For each new tournament, the script will be run again. Therefore, we know we only need one tournament instance. 
    We get the info from the VIEW.
    """
    SUBSEQUENT_ROUNDS = False

    # instantiating the tournament
    tournament = Tournament(*insert_tournament_info())

    storing_player_instances_in_tournament = CreatingPlayerStoringInTournament(tournament)

    # setting up the first round
    announce_pairing_for_first_round()
    storing_round_instances_in_tournament = CreatingRoundStoringInTournament(tournament)

    # the first round is taking place
    time_control(tournament)

    # the first round happened
    storing_match_instances_in_tournament = CreatingMatchStoringInRoundOne(1)
    matches_from_last_round = tournament.rounds["Round 1"].dict_of_matches
    update_all_players_attrs_after_round(matches_from_last_round)

    possibly_saving_data = SaveDataInDB(tournament)

    for i in range(1, tournament.number_of_rounds):
        # the algorithm used for the first round and for the subsequent rounds are different. Therefore,
        # the first round matches are instantiated out of the loop. The range built-in function starts at
        # zero but the first round is round1, that's why the arg passed to the CreatingMatchStoringInRoundOne
        # class is i+1

        announce_pairing_for_subsequent_round()
        time_control(tournament)

        storing_more_match_instances_in_tournament = CreatingMatchStoringInSubsequentRounds(i + 1)
        matches_from_last_round = tournament.rounds[f"Round {i + 1}"].dict_of_matches
        update_all_players_attrs_after_round(matches_from_last_round)

        possibly_saving_data = SaveDataInDB(tournament)

    print(f"the idea is to be sure that the players attributes are updated correctly\n"
          f"this is player1:{tournament.list_of_players_instances[0]}\n"
          f"this is player2:{tournament.list_of_players_instances[1]}\n"
          f"this is player3:{tournament.list_of_players_instances[2]}\n"
          f"this is player4:{tournament.list_of_players_instances[3]}")

    announce_ranking()

    making_a_request = RequestsMenu(tournament)


