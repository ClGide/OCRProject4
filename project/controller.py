from operator import attrgetter
from typing import Dict, List

from models import Player, Round, Tournament, Match
from view import insert_player_info, tournament_info, insert_results

"""We are figuring out the basic logic for an 16 person tournament"""

# Assuming for each new tournament, a new script will be run,
# we only need one tournament instance per script. The attributes are requested in the WIEW module.
tournament = Tournament(*tournament_info())

# the input is necessarily a string. Let's convert the attrs we want as integers.
tournament.players_number = int(tournament.players_number)
tournament.number_of_rounds = int(tournament.number_of_rounds)

""" There seems to be a conflict between MVC and OOP. The thing is that the MODEL shouldn't define any process. 
Therefore, the classes in the MODEL should define no method. However, we need to act upon the 
instances of those classes. To do so, I see two possibilities (ofc, they may be others I ignore).
The first one is to define some func in the global scope that acts upon the instance attributes. 
But this is not very OOP. I should modify instance properties only through the interface defined by the class. 
The second one is to bind some function to the class in the CONTROLLER. I think it is the best approach although the 
downside is that the properties and the behaviours of a class will be defined in two different files. 
I will define all those behaviours down here so I can easily find them.   
"""


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


Match.convert_match_result_into_points = convert_match_result_into_points


def add_opponent(self, value):
    self.opponents_faced.append(value)


Player.add_opponent = add_opponent


""" 
Below comes a useful decorator aiming at beautifying the info send to the VIEW.
DISCLAIMER : I know there are easier workarounds to do what follows, 
but given the fact I spent 2 hours understanding how dunder method overriding at instance level works, 
I want to use it. I may change the code before the presentation though.  
"""


def shorten_player_representation(players: List[Player]):
    overriding_method = {'__str__': lambda self: self.__getattribute__('last_name')}
    for player in players:
        player.__class__ = type('class_with_shorter_representation_inheriting_from_Player',
                                (Player,),
                                overriding_method)
        yield player


def lenghten_player_representation(players: List[Player]):
    for player in players:
        player.__class__ = Player
        yield player


def beautify_player_representation(func):
    def wrapper(players: List[Player]):
        # shortening the representation of each player in order to make it suitable for the view.
        shortened_representation_players = []
        for player in shorten_player_representation(players):
            shortened_representation_players.append(player)

        func(players)

        # restore the object representation for further uses.
        restored_representation_players = []
        for player in lenghten_player_representation(players):
            restored_representation_players.append(player)

    return wrapper


"""
Here comes the requesting, storing of players in dict then list format
"""


def request_players_info(number_of_players: int):
    players = []
    for _ in range(number_of_players):
        player = insert_player_info()
        players.append(player)
    return players


def store_player_instances(number_of_players: int):
    players_info = request_players_info(number_of_players)

    player_names = []
    for player_info in players_info:
        player_name = player_info[0]
        player_names.append(player_name)

    player_instances = []
    for player_info in players_info:
        player_instance = Player(*player_info)
        player_instances.append(player_instance)

    all_players_in_dict_format = {}
    for name, instance in zip(player_names, player_instances):
        all_players_in_dict_format[name] = instance

    return all_players_in_dict_format


def store_player_instances_in_list(number_of_players: int):
    all_players_in_dict_format = store_player_instances(number_of_players)

    all_players_in_list_format = []
    for player_instance in all_players_in_dict_format.values():
        all_players_in_list_format.append(player_instance)

    return all_players_in_list_format


"""
Below comes the pairing and annoucing of the matches for the first round 
"""

#all_players_in_list_format = store_player_instances_in_list(tournament.players_number)


def pairing_for_first_round(players: List[Player]):
    half = len(players) // 2
    first_group = players[:half]
    second_group = players[half:]

    pairing = []
    for first_group_player, second_group_player in zip(first_group, second_group):
        pairing.append((first_group_player, second_group_player))
    print(len(pairing))
    return pairing


@beautify_player_representation
def announce_pairing_for_first_round(players: List[Player]):
    # should this go directly in the view ? probably not, because there is some method overriding.
    # for a 16 player tournament, pairs[0] should meet pairs[8], pairs[1] should meet pairs[9] and so on.
    pairs = pairing_for_first_round(players)

    pairing_announcement = ["For the first round"]
    for pair in pairs:
        pairing_announcement.append(f'{pair[0]} will meet {pair[1]}')

    return pairing_announcement


#announce_pairing_for_first_round(all_players_in_list_format)


""" 
The following is a flow proposal : 
1) program announces the matches for the first round.
2) matches took place and the manager inserted the result (in the view).
3) program instantiates the matches and the corresponding round. 
3) the program pairs the player with the swiss algorithm for subsequent rounds.

TODO: We also need to give each round a start and end datetime that will be set depending on two criteria. 
First, the number of expected rounds AND second, the time_control property of the corresponding Tournament instance.
Should we foresee a break time between rounds ? and if yes, how long should that break be ?  
"""

""" The round should be instantiated just before we request the match results. 
It's list_of_matches default arg will be given a non-None value afterwards. 
the Match instances should be instantiated just after the manager wrote the results.  
"""


def instantiate_round(round_number: int):
    # the inconvenience of dynamically creating an obj is that you recreate the
    # obj each time you need it. Given that we store rounds in the Tournament instance,
    # and maybe in other locations, I hope this recreation doesn't create bugs.
    round_name = f"round{round_number}"
    round_instance = Round(round_name, tournament)
    return round_name, round_instance


def store_rounds(round_number: int):
    round_name, round_instance = instantiate_round(round_number)
    round_instances = {}
    if round_instance not in round_instances.values():
        round_instances[round_name] = round_instance
    if len(round_instances) > tournament.number_of_rounds:
        print("there are more rounds than originally declared")
        raise IndexError

    return round_instances


round1_name, round1_instance = instantiate_round(tournament.number_of_rounds)


def request_match_results(players: List[Player]):
    players_pairs = pairing_for_first_round(players)

    results = []
    for i in range(len(players_pairs)):
        player1 = players_pairs[i][0]
        match_result = insert_results(player1.last_name)
        results.append(match_result)

    return results


def collect_first_round_matches_attributes(players: List[Player]):
    number_of_matches = int(tournament.players_number) // 2
    player_pairs_for_first_round = pairing_for_first_round(players)

    if len(player_pairs_for_first_round) != number_of_matches:
        print("the number of players in the tournament doesn't match the number of matches choosen"
              " this script assumes all players have a match every round")
        raise IndexError

    match_results = request_match_results(players)
    match_round = instantiate_round(1)

    match_instances_attributes = []
    for i in range(number_of_matches):
        match_players_1 = player_pairs_for_first_round[i][0]
        match_players_2 = player_pairs_for_first_round[i][1]
        match_result = match_results[i]
        match_instances_attributes.append((match_players_1, match_players_2, match_result, match_round))

    return match_instances_attributes


def instantiate_and_store_first_round_matches_in_dict(players: List[Player]):
    # this function should probably be refactored (does two things), but it also seems to be a short func
    matches_attributes = collect_first_round_matches_attributes(players)
    first_round_matches = {}

    for i in range(len(matches_attributes)):
        match_name = f'match{i + 1}'
        match_instance = Match(*matches_attributes[i])
        first_round_matches.update({match_name: match_instance})

    return first_round_matches


#matches_first_round = instantiate_and_store_first_round_matches_in_dict(all_players_in_list_format)

"""
Below we append the matches that just happened to their corresponding round. We also append
the round to her corresponding tournament. Note that the two operations must happen in this order. 
"""


def append_matches_to_round(matches: Dict[str, Match], round: Round):
    for match in matches.values():
        if round == match.round:
            round.list_of_matches.append(match)
        else:
            print(f"the {match} didn't happen in this round")
            raise ValueError


#append_matches_to_round(matches_first_round, round1_instance)

def append_round_to_tournament(tournament: Tournament, round: Round):
    if tournament == round.tournament:
        tournament.rounds.append(round)
    else:
        print(f"this {round} didn't happen in this tournament")
        raise ValueError


#append_round_to_tournament(tournament, round1_instance)


"""
below we update all the players attributes in accordance to the result of the end that just happened.
"""


def check_match_result(player1: Player, player2: Player, match: Match):
    # We take the results in the right format from the request_match_results match method.
    results = match.convert_match_result_into_points

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


def update_player_faced_opponents_attr(player1: Player, player2: Player, match: Match):
    results = check_match_result(player1, player2, match)

    # Updating the opponents_faced attr of the player
    player1_opponent = results[1][0]
    player2_opponent = results[0][0]

    # for more readability, we will only add the player's last name to the record
    player1_opponent = player1_opponent.last_name
    player2_opponent = player2_opponent.last_name

    player1.add(player1_opponent)
    player2.add(player2_opponent)


def update_all_players_attrs_after_round(matches: list):
    for match in matches:
        player1 = match.convert_match_result_into_points()[0][0]
        player2 = match.convert_match_result_into_points()[1][0]
        change_players_result_field(player1, player2, match)
        update_player_faced_opponents_attr(player1, player2, match)


#update_all_players_attrs_after_round(matches_first_round)


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
    unavoidable_duplicata = False

    # rearranging the list in order to avoid duplicata. The logic is the following. If two players are
    # about to meet, we need to swap one of the players w/ another one located two indexes further in the list.
    for _ in range(len(p)):
        for i in range(len(p)):
            if i == 0:
                continue
            if p[i - 1].last_name in p[i].opponents_faced:
                p[i], p[(i + 2) % (len(p))] = p[(i + 2) % (len(p))], p[i]

    # checking the sorted list for unavoidable match duplicata
    for i in range(len(p)):
        if i == 0:
            continue
        if p[i - 1].last_name in p[i].opponents_faced:
            unavoidable_duplicata = True
            break
    paired_players = p
    return paired_players, unavoidable_duplicata


@beautify_player_representation
def announce_pairing_for_subsequent_round(players_ranked_in_previous_round):
    paired_players, unavoidable_duplicata = avoid_player_meeting_twice(players_ranked_in_previous_round)
    p = paired_players

    pairing_announcement = [f'{p[0]} will meet {p[1]}']

    for i in range(len(p)):
        if i == 0 or i == 1 or i == 2:
            continue
        if i >= 3 and (i % 2) != 0:
            pairing_announcement.append(f'{p[i-1]} will meet {p[i]}')

    if unavoidable_duplicata is True:
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


#update_all_players_attrs_after_round(matches_round2)

#avoid_player_meeting_twice(all_players_in_list_format)


""" All good for the second round too. Let's create a func that announces the current rank. 
"""


@beautify_player_representation
def announce_ranking(players: List[Player]):
    ranking_annoucement = []
    p = rank_players_for_subsequent_round(players)
    for i in range(len(p)):
        ranking_annoucement.append(f'{p[i]} is number {i+1}')
    print(ranking_annoucement)
    return ranking_annoucement

#rank_players_for_subsequent_round(all_players_in_list_format)
