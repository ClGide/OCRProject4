from models import *
from controller import *

def tournament_infos():
    # with the input from this function, the controller will instantiate the tournament object
    pass


def insert_player_names(tournament):
    # with the input from this function, the controller will add the players to the tournament object
    player1 = input(f"Please enter the player names according to their ranking \n"
                    f"1.")
    player2 = input("2.")
    player3 = input("3.")
    player4 = input("4.")
    player5 = input("5.")
    player6 = input("6.")
    player7 = input("7.")
    player8 = input("8.")

def define_time_control(tournament):
    time_control = input(f"what time-control type should the {tournament} implement ? Enter"
                 f"'rapid', 'blitz' or 'bullet")

def rankings_before_tournament(tournament):
    pass


def insert_results(player1, player2):
    # No computation should be done here. All we need to do is take result for each mach, store it and
    # transfer it in the controller.
    match_result = input(f"What was the result of the match ? Enter 'W' if {player1} winned, "
                   "'L' if he lost and 'D  if the match ended in a draw")
