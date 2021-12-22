from operator import attrgetter
from typing import Dict, List

from models import Player, Round, Tournament, Match
from view import insert_player_info, tournament_info, insert_results


class CreatingPlayerStoringInTournament:
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
2) matches took place and the manager inserted the result (in the view).
3) program instantiates the matches and the corresponding round. 
3) the program pairs the player with the swiss algorithm for subsequent rounds.

TODO: We also need to give each round a start and end datetime that will be set depending on two criteria. 
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

        """Q: the inconvenience of dynamically creating an obj is that you recreate the
        obj each time you need it. Given that we store rounds in the Tournament instance,
        and maybe in other locations, I hope this recreation doesn't create bugs."""

        round_name = f"round{round_number}"
        round_instance = Round(round_name, self.tournament)
        return round_name, round_instance

    def store_rounds(self):
        round_instances = {}
        for i in range(self.number_of_rounds):
            # appending the round instance to the dict round_instances
            round_name, round_instance = self.instantiate_round(i+1)
            if round_instance not in round_instances.values():
                round_instances[round_name] = round_instance

            # catching eventual errors in the process
            else:
                print("this round have already been instantiated and stored")
                raise ValueError
            if len(round_instances) > tournament.number_of_rounds:
                print("there are more rounds than originally declared")
                raise IndexError

        # storing the rounds in the tournament instance
        tournament.rounds = round_instances


class CreatingMatchStoringInRound:
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

        match_round = tournament.rounds[f"round{self.round_number}"]

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

        tournament.rounds[f"round{self.round_number}"].dict_of_matches = matches_instances


"""
below we update all the players attributes in accordance to the result of the round that just happened.
Even I use procedural style, I think is clear enough to not be transferred into OOP style. 
"""


def check_match_result(player1: Player, player2: Player, match: Match):
    # We take the results in the right format from the request_match_results match method.
    results = match.convert_match_result_into_points()

    # We should give the right players the right results
    player1_from_results = results[0][0]
    player2_from_results = results[1][0]
    if player1_from_results != player1 or player2_from_results != player2:
        print("the players you entered do not match the players from the match")
        raise TypeError

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

    # Updating players' rank attribute in accordance to the ranking we just done
    for player in players_sorted_by_points_then_rank:
        player.ranking = players_sorted_by_points_then_rank.index(player) + 1

    return players_sorted_by_points_then_rank


def avoid_player_meeting_twice(players_ranked_in_previous_round: list):
    players_ranked_for_subsequent_round = rank_players_for_subsequent_round(players_ranked_in_previous_round)
    p = players_ranked_for_subsequent_round
    unavoidable_duplicate = False

    # rearranging the list in order to avoid duplicate. The logic is the following. If two players are
    # about to meet, we need to swap one of the players w/ another one located two indexes further in the list.
    for _ in range(len(p)):
        for i in range(len(p)):
            if i == 0:
                continue
            if p[i - 1].last_name in p[i].opponents_faced:
                p[i], p[(i + 2) % (len(p))] = p[(i + 2) % (len(p))], p[i]

    # checking the sorted list for unavoidable match duplicate
    for i in range(len(p)):
        if i == 0:
            continue
        if p[i - 1].last_name in p[i].opponents_faced:
            unavoidable_duplicate = True
            break
    paired_players = p
    return paired_players, unavoidable_duplicate


@beautify_player_representation
def announce_pairing_for_subsequent_round():
    paired_players, unavoidable_duplicate = avoid_player_meeting_twice(tournament.list_of_players_instances)
    p = paired_players

    pairing_announcement = [f'{p[0]} will meet {p[1]}']

    for i in range(len(p)):
        if i == 0 or i == 1 or i == 2:
            continue
        if i >= 3 and (i % 2) != 0:
            pairing_announcement.append(f'{p[i-1]} will meet {p[i]}')

    if unavoidable_duplicate is True:
        pairing_announcement.append("given the number of matches and players in tournament, "
                                    "it is unavoidable that players meet twice")

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


if __name__ == "__main__":
    """ 
    For each new tournament, the script will be run again. Therefore, we know we only need one tournament instance. 
    We get the info from the VIEW.
    """

    tournament = Tournament(*tournament_info())

    storing_player_instances_in_tournament = CreatingPlayerStoringInTournament(tournament)

    announce_pairing_for_first_round()

    storing_round_instances_in_tournament = CreatingRoundStoringInTournament(tournament)

    storing_match_instances_in_tournament = CreatingMatchStoringInRound(1)

    matches_from_last_round = tournament.rounds["round1"].dict_of_matches
    update_all_players_attrs_after_round(matches_from_last_round)

    print(f"the idea is to be sure that the players attributes are updated correctly\n"
          f"this is player1:{tournament.list_of_players_instances[0]}"
          f"this is player2:{tournament.list_of_players_instances[1]}"
          f"this is player3:{tournament.list_of_players_instances[2]}"
          f"this is player4:{tournament.list_of_players_instances[3]}")

    announce_pairing_for_subsequent_round()

    announce_ranking()
