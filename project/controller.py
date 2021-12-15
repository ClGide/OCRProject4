from dataclasses import dataclass
from operator import attrgetter

from models import Player, Round, Tournament
from view import insert_player_info

"""We are figuring out the basic logic for an 16 person tournament"""

@dataclass
class Match:
    player1: Player
    player2: Player
    result: str
    round: str

    def return_result(self):
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


""" There seems to be a conflict between MVC and OOP. The thing is that the MODEL shouldn't define any process. 
Therefore, the classes in the MODEL should define no method. However, we need to act upon the 
instances of those classes. To do so, I see two possibilities (ofc, they may be others I ignore).
The first one is to define some func in the global scope that acts upon the instance attributes. But this is not very OOP.
I should modify instance properties only through the interface defined by the class. 
The second one is to bind some function to the class in the CONTROLLER. I think it is the best approach although the 
downside is that the properties and the behaviours of a class will be defined in two different files. I will define all
those behaviours down here so I can easily find them.   
"""

def add_opponent(self, value):
    self.opponents_faced.append(value)

Player.add_opponent = add_opponent


"""
In the first round, for a 16 player tournament, nr 1 plays w/ nr 9, nr 2 w/ nr 10 and so on. 
In the second round, rankings are updated and then nr1 plays w/nr2, nr3 plays w/ nr4 and so on. 
For the first round, we rank players by their rankings. 
The Player instances and the list ranking them should be created by a function
after the manager input the player info. 
We will mimic a 16 players tournament, 3 rounds. We need to make sure that players do not meet each other twice. 
Why a 16 players tournament? 
Because with less players, the chance of player meeting twice are too small.
"""



"""he only argument of the three following functions should be given when the program starts. We should take it 
from the tournament instance. """

def collect_player_info_from_view(number_of_players: int):
    """
    The insert_player_info() from the view module returns a tuple.
    From that tuple, we are making two lists. The first one contains player names. In the dictionary we will build
    with the create_player_instances function, those names are going to be the keys.
    The second list contains a tuple with the player info. Those info are going to be used to create Player instances
    with the create_player_instances function. Those Player instances are going to be the values of the dict returned
    by that function.
    """
    player_names: str = []
    player_attrs: tuple = []
    for _ in range(number_of_players):
        attrs = insert_player_info()
        name = attrs[0].lower()
        player_attrs.append(attrs)
        player_names.append(name)
    return player_names, player_attrs

def format_player_info(number_of_players: int):
# The previous func returns a tuple containing two lists. We zip those two lists into a dictionnary.
    player_names, player_attrs = collect_player_info_from_view(number_of_players)
    if len(player_names) == len(player_attrs):
        # I see no config in which the two lists won't be of equal length, but is better to catch errors soon.
        player_names_and_attrs_info = dict(zip(player_names, player_attrs))
    return player_names_and_attrs_info


def create_player_instances(number_of_players: int):
    names_and_attrs = format_player_info(number_of_players)
    dict_with_player_instances = {}
    for name, attrs in names_and_attrs.items():
        dict_with_player_instances[name] = Player(*attrs)
    return dict_with_player_instances


""" We need to write everything that follows with the input format in mind. 
"""


all_players = {
"macron" : Player("Macron", "Emmanuel", "1977", "men", 1),
"erdogan" : Player("Erdogan", "Recep", "1954", "men", 2),
"johnson" : Player("Johnson", "Boris", "1964", "men", 3),
"scholz" : Player("Scholz", "Olaf", "1958", "men", 4),
"biden" : Player("Biden", "Joe", "1942", "men", 5),
"jinping" : Player("Jinping", "Xi", "1953", "men", 6),
"radev" : Player("Radev", "Roumen", "1963", "men", 7),
"iohannis" : Player("Iohannis", "Klaus", "1959", "men", 8),
"modi" : Player("Modi", "Narendra", "1950", "men", 9),
"putin" : Player("Putin", "Vladimir", "1952", "men", 10),
"draghi" : Player("Draghi", "Mario", "1947", "men", 11),
"orban" : Player("Orban", "Viktor", "1963", "men", 12),
"kurz" : Player("Kurz", "Sebastian", "1986", "men", 13),
"sanchez" : Player("Sanchez", "Pedro", "1972", "men", 14),
"ardern" : Player("Ardern", "Jacinda", "1980", "women", 15),
"marin" : Player("Marin", "Sanna", "1986", "women", 16),
}

all_players_in_list_format = list(all_players.values())


def pairing_for_first_round():
    # is it possible that the tournament has an odd number of players ?
    players = all_players_in_list_format
    half = len(players) // 2
    first_group = players[:half]
    second_group = players[half:]
    pairing = []
    for first_group_player, second_group_player in zip(first_group, second_group):
        pairing.append((first_group_player, second_group_player))
    return pairing

pairing_for_first_round()

""" DISCLAIMER : I know there are easier workarounds to do what follows, 
but given the fact I spent 2 hours understanding how dunder method overriding at instance level works, 
I want to use it. I may change the code before the presentation though.  
"""


def shorten_player_representation(players: Player):
    overriding_method = {'__str__': lambda self: self.__getattribute__('last_name')}
    for player in players:
        player.__class__ = type('class_with_shorter_representation_inheriting_from_Player',
                                (Player,),
                                overriding_method)
        yield player


def lenghten_player_representation(players: Player):
    for player in players:
        player.__class__ = Player
        yield player


def beautify_player_representation(func):
    def wrapper(players:Player):
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


@beautify_player_representation
def announce_pairing_for_first_round(list_of_players):
    # should this go directly in the view ? probably not, because there is some method overriding.
    # for a 16 player tournament, pairs[0] should meet pairs[8], pairs[1] should meet pairs[9] and so on.
    pairs = pairing_for_first_round(list_of_players)
    pairing_announcement = []
    for pair in pairs:
        pairing_announcement.append(f'{pair[0]} will meet {pair[1]}')
    return pairing_announcement


#announce_pairing_for_first_round(all_players_in_list_format)

""" The following is a flow proposal : 
1) program announces the matches for the first round.
2) matches took place and the manager inserted the result (in the view).
3) program instantiates the matches and the corresponding round. 
3) the program pairs the player with the swiss algorithm for subsequent rounds.
We also need to give each round a start and end datetime that will be set depending on two criteria : the 
number of expected rounds AND the time_control property of the corresponding Tournament instance. Should we 
foresee a break time between rounds ? and if yes, of what time ?  
"""

# the Match instances and the corresponding round should be instantiated just after the manager wrote the results

p = all_players
match1 = Match(p["macron"], p["modi"], "W", 'round1')
match2 = Match(p["erdogan"], p["putin"], "W", 'round1')
match3 = Match(p["johnson"], p["draghi"], "D", 'round1')
match4 = Match(p["scholz"], p["orban"], "L", 'round1')
match5 = Match(p["biden"], p["kurz"], "D", 'round1')
match6 = Match(p["jinping"], p["sanchez"], "L", 'round1')
match7 = Match(p["radev"], p["ardern"], "D", 'round1')
match8 = Match(p["iohannis"], p["marin"], "L", 'round1')
matches_round1 = [match1, match2, match3, match4, match5, match6, match7, match8]

round1 = Round("round1", "international politics", matches_round1)


def get_opponents_and_match_result(player1: Player, player2: Player, match: Match):
    # We take the results in the right format from the return_results match method.
    results = match.return_result()

    # We should give the right players the right results
    player1_from_results = results[0][0]
    player2_from_results = results[1][0]
    if player1_from_results != player1 or player2_from_results != player2:
        print("the players you entered do not match the players from the match")
        raise TypeError

    return results


def change_players_result_field(player1: Player, player2: Player, match: Match):
    results = get_opponents_and_match_result(player1, player2, match)

    # Updating the result_field attr of the player
    player1_result = results[0][1]
    player2_result = results[1][1]
    player1.result_field += player1_result
    player2.result_field += player2_result


def update_player_faced_opponents_record(player1: Player, player2: Player, match: Match):
    results = get_opponents_and_match_result(player1, player2, match)

    # Updating the opponents_faced attr of the player
    player1_opponent = results[1][0]
    player2_opponent = results[0][0]

    # for more readability, we will only add the player's last name to the record
    player1_opponent = player1_opponent.last_name
    player2_opponent = player2_opponent.last_name

    player1.add(player1_opponent)
    player2.add(player2_opponent)


def update_all_players_in_round_points_and_record(matches: list):
    for match in matches:
        change_players_result_field(match.return_result()[0][0], match.return_result()[1][0], match)
        update_player_faced_opponents_record(match.return_result()[0][0], match.return_result()[1][0], match)


update_all_players_in_round_points_and_record(matches_round1)


def rank_players_for_subsequent_round(players_ranked_in_previous_round: list):
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

    return players_sorted_by_points_then_rank


def avoid_player_meeting_twice(players_ranked_in_previous_round: list):
    players_ranked_for_subsequent_round = rank_players_for_subsequent_round(players_ranked_in_previous_round)
    p = players_ranked_for_subsequent_round
    unavoidable_duplicata = False

    # sorting the list in order to avoid duplicata
    for _ in range(len(p)):
        for i in range(len(p)):
            if i == 0: continue
            if p[i - 1].last_name in p[i].opponents_faced:
                p[i], p[(i + 2) % (len(p))] = p[(i + 2) % (len(p))], p[i]

    # checking the sorted list for unavoidable match duplicata
    for i in range(len(p)):
        if i == 0: continue
        if p[i - 1].last_name in p[i].opponents_faced:
            unavoidable_duplicata = True
            break
    paired_players = p
    return paired_players, unavoidable_duplicata


@beautify_player_representation
def announce_pairing_for_subsequent_round(players_ranked_in_previous_round):
    paired_players, unavoidable_duplicata = avoid_player_meeting_twice(players_ranked_in_previous_round)
    p = paired_players

    pairing_announcement = []
    pairing_announcement.append(f'{p[0]} will meet {p[1]}')
    for i in range(len(p)):
        if i == 0 or i == 1 or i == 2:
            continue
        if i >= 3 and (i%2) != 0:
            pairing_announcement.append(f'{p[i-1]} will meet {p[i]}')
    if unavoidable_duplicata == True:
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

match9 = Match(p["macron"], p["erdogan"], "L", 'round2')
match10 = Match(p["orban"], p["sanchez"], "W", 'round2')
match11 = Match(p["marin"], p["johnson"], "D", 'round2')
match12 = Match(p["biden"], p["radev"], "D", 'round2')
match13 = Match(p["draghi"], p["kurz"], "D", 'round2')
match14 = Match(p["ardern"], p["scholz"], "W", 'round2')
match15 = Match(p["jinping"], p["iohannis"], "W", 'round2')
match16 = Match(p["modi"], p["putin"], "W", 'round2')
matches_round2 = [match9, match10, match11, match12, match13, match14, match15, match16]

round2 = Round("round2", "international politics", matches_round2)

update_all_players_in_round_points_and_record(matches_round2)

avoid_player_meeting_twice(all_players_in_list_format)



""" All good for the second round too. Let's create a func that announces the current rank. 
"""

@beautify_player_representation
def announce_ranking(players:Player):
    ranking_annoucement = []
    p = rank_players_for_subsequent_round(players)
    for i in range(len(p)):
        ranking_annoucement.append(f'{p[i]} is number {i+1}')
    print(ranking_annoucement)
    return ranking_annoucement


print(avoid_player_meeting_twice(all_players_in_list_format))
announce_ranking(all_players_in_list_format)
