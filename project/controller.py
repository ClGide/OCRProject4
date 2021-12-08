from models import *
from operator import attrgetter

"""We are figuring out the basic logic for an eight person tournament"""


@dataclass
class Match:
    player1: Player
    player2: Player
    result: str
    round: str

    def return_result(self):
        # We take the needed letter from the view and we return the results in the correct format
        if self.result == "W":
            score1 = 1
            score2 = 0
        elif self.result == "L":
            score1 = 0
            score2 = 1
        elif self.result == "D":
            score1 = 0.5
            score2 = 0.5
        else:
            print('please enter "W", "L" or "D"')
            raise TypeError
        results = [(self.player1, score1), (self.player2, score2)]
        return results


"""
In the first round nr 1 plays w/ nr 5, Nr 2 w/ nr 6 and so on. In the second round, rankings are updated and then
nr1 plays w/nr2, nr3 plays w/ nr4 and so on. 
For the first round, we rank players by their rankings. 
The Player instances and the list ranking them should be created by a function
after the manager input the player info. 
We will mimic a 16 player tournament, 3 rounds. We need to make sure that players do not meet each other twice. 
Why a 16 players tournament? 
Because with less players, the chance of double meeting are too small.
"""

macron = Player("Macron", "Emmanuel", "1977", "men", 1)
erdogan = Player("Erdogan", "Recep", "1954", "men", 2)
johnson = Player("Johnson", "Boris", "1964", "men", 3)
scholz = Player("Scholz", "Olaf", "1958", "men", 4)
biden = Player("Biden", "Joe", "1942", "men", 5)
jinping = Player("Jinping", "Xi", "1953", "men", 6)
radev = Player("Radev", "Roumen", "1963", "men", 7)
iohannis = Player("Iohannis", "Klaus", "1959", "men", 8)
modi = Player("Narendra", "Modi", "1950", "men", 9)
putin = Player("Putin", "Vladimir", "1952", "men", 10)
draghi = Player("Draghi", "Mario", "1947", "men", 11)
orban = Player("Orban", "Viktor", "1963", "men", 12)
kurz = Player("Kurz", "Seabstian", "1986", "men", 13)
sanchez = Player("Sanchez", "Pedro", "1972", "men", 14)
ardern = Player("Ardern", "Jacinda", "1980", "women", 15)
marin = Player("Marin", "Sanna", "1986", "women", 16)

players_ranked_for_first_round = [macron, erdogan, johnson, scholz, biden, jinping, radev, iohannis,
                                  modi, putin, draghi, orban, kurz, sanchez, ardern, marin]


def pairing_for_first_round(list_of_players):
    # is it possible that the tournament has an even number of players ?
    half = len(list_of_players) // 2
    first_group = list_of_players[:half]
    second_group = list_of_players[half:]
    pairing = []
    for first_group_player, second_group_player in zip(first_group, second_group):
        pairing.append((first_group_player, second_group_player))
    return pairing


""" DISCLAIMER : I know there are easier workarounds to do what follows, 
but given the fact I spend 2 hours understanding how dunder method overriding at instance level works, 
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


def announce_pairing_for_first_round(list_of_players):
    # should this go directly in the view ? probably not, because there is some method overriding.
    # shortening the representation of each player in order to make it suitable for the view.
    shortened_representation_players = []
    for player in shorten_player_representation(list_of_players):
        shortened_representation_players.append(player)

    # pairs[0] should meet pairs[1], pairs[2] should meet pairs[3] and so on.
    pairs = pairing_for_first_round(list_of_players)

    # restore the object representation for further uses.
    restored_representation_players = []
    for player in lenghten_player_representation(list_of_players):
        restored_representation_players.append(player)


announce_pairing_for_first_round(players_ranked_for_first_round)

""" The following is a flow proposal : 
1) program instantiates a round with the matches. 
2) matches took place and the manager inserted the result (in the view).
3) the program pairs the player with the swiss algorithm.
We also need to implement a start and end datetime. 
"""

# the match instances and the corresponding round should be instantiated just after the manager wrote the results
match1 = Match(macron, modi, "W", 'round1')
match2 = Match(erdogan, putin, "W", 'round1')
match3 = Match(johnson, draghi, "D", 'round1')
match4 = Match(scholz, orban, "L", 'round1')
match5 = Match(biden, kurz, "D", 'round1')
match6 = Match(jinping, sanchez, "L", 'round1')
match7 = Match(radev, ardern, "D", 'round1')
match8 = Match(iohannis, marin, "L", 'round1')
matches_round1 = [match1, match2, match3, match4, match5, match6, match7, match8]

round1 = Round("round1", "international politics", matches_round1)


def give_players_points(player1: Player, player2: Player, match: Match):
    # We take the results in the right format from the return_results match method.
    # We then change the players result_field in accordance to those results.
    results = match.return_result()

    # Just a little check up - we should give the right players the right results
    player1_from_results = results[0][0]
    player2_from_results = results[1][0]
    if player1_from_results != player1 or player2_from_results != player2:
        print("the players you entered do not match the players from the match")
        raise TypeError

    player1_result = results[0][1]
    player2_result = results[1][1]
    player1.result_field += player1_result
    player2.result_field += player2_result


def give_all_players_in_round_points(matches: list):
    for match in matches:
        give_players_points(match.return_result()[0][0], match.return_result()[1][0], match)


give_all_players_in_round_points(matches_round1)


def rank_players_for_subsequent_round(players_ranked_in_previous_round):
    # I need to figure out a more elegant way to sort by points in decreasing order
    # then, ONLY IF players have an equal number of points, by rank in ascending order.
    for player in players_ranked_in_previous_round:
        player.ranking = -player.__getattribute__("ranking")

    players_sorted_by_points_then_rank = sorted(players_ranked_in_previous_round,
                                                key=attrgetter("result_field", 'ranking'),
                                                reverse=True)

    for player in players_ranked_in_previous_round:
        player.ranking = -player.__getattribute__("ranking")

    return players_sorted_by_points_then_rank


def announce_pairing_for_subsequent_round(players_ranked_in_previous_round):
    # this also should go in the view ?
    p = players_ranked_in_previous_round
    return f'{p[0]} will meet {p[1]}' \
           f'{p[2]} will meet {p[3]}' \
           f'{p[4]} will meet {p[5]}' \
           f'{p[6]} will meet {p[7]}'
