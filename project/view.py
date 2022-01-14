from typing import Tuple


def collect_tournament_info() -> Tuple[str, str, str, str, str, str, str]:
    # with the input from this function, the controller will instantiate the tournament object
    tournament_name: str = input("Hi, we hope our program will help you store all the data you need on your "
                                 "chess tournaments. "
                                 "Please follow the instructions carefully, remembering that the program "
                                 "is case sensitive. Do not type unnecessary spaces.\n\n"
                                 "Please enter the tournament's name\n")
    tournament_venue: str = input("Please enter the tournament's venue\n")
    tournament_date: str = input("Enter the tournament's date. "
                                 "Please, respect the expected format yyyy/mm/dd\n")
    tournament_players_number: str = input("How many players are in the tournament\n")
    tournament_description: str = input("you can enter some remarks about the tournament right here\n")
    tournament_time_control: str = input("Choose between the three time control type\n1.bullet\n2.blitz\n3.rapid\n")
    tournament_round_numbers: str = input("How many rounds should they be in the tournament ?\n")

    return tournament_name, tournament_venue, tournament_date, tournament_players_number, \
        tournament_description, tournament_time_control, tournament_round_numbers


def collect_results(player1: str) -> str:
    # No computation should be done here. All we need to do is take result for each mach, store it and
    # transfer it in the controller.
    match_result = input(f"What was the result of the match ? Enter 'W' if {player1} won, "
                         "'L' if he lost and 'D  if the match ended in a draw \n")
    return match_result


def collect_player_info() -> Tuple[str, str, str, str, str]:
    # this functions immediately returns it's value in the model module.
    # The number of times it is used is also set in the model module.
    player_surname: str = input("Please enter the player's surname\n")
    player_first_name: str = input("Please enter the player's first name\n")
    player_birthday: str = input("Enter the player's date of birth. "
                                 "Please, respect the expected format yyyy/mm/dd\n")
    player_gender: str = input("Please enter the player's gender "
                               "(choose between 'men', 'women' or 'other')\n")
    player_rank: str = input("Please enter the player's rank\n")

    return player_surname, player_first_name, player_birthday, player_gender, player_rank


def override_tournament_description():
    new_description: str = input("Do you want to override the tournament's description ?\n"
                                 "If you don't need anything, just click ENTER\n"
                                 "Otherwise, enter the new description\n")
    return new_description


def override_player_ranking():
    which_player: str = input("Do you want to override one player's ranking ?\n"
                              "If you don't need anything, just click ENTER\n"
                              "Otherwise, enter the player's LAST NAME\n")
    return which_player


def complete_override_player_ranking():
    new_rank: str = input("What's the new ranking of the player\n")
    return new_rank


def what_table_to_save() -> str:
    manager_wants_to_save = input(
        "Do you want to save some data ? Please enter the number corresponding to your need:\n"
        "1. I need to save a table with all the tournament info\n"
        "2. I need to save a table with all the players info\n"
        "3. I need to save both tables\n"
        "4. I don't need to save anything for the moment\n")
    return manager_wants_to_save


def what_data_to_read() -> str:
    request = input("Do you need something from the database ? just enter the number corresponding to your request:\n"
                    "1. a list with all the players from a tournament ranked alphabetically\n"
                    "2. a list with the ranking of all the players from a tournament\n"
                    "3. a list with the players from all the tournaments ranked alphabetically\n"
                    "4. a list with the ranking of all the players from all tournaments\n"
                    "5. a list with all the tournaments\n"
                    "6. a list of all the rounds in a tournament\n"
                    "7. a list of all the matches in a tournament\n"
                    "8. I don't need anything for the moment\n")
    return request


def what_tournament_name():
    which_tournament = input("which tournament are you referring to ?")
    return which_tournament
