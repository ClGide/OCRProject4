def insert_tournament_info():
    # with the input from this function, the controller will instantiate the tournament object
    tournament_name: str = input("Hi, we hope our program will help you store all the data you need on your "
                                 "chess tournaments. "
                                 "Please follow the instructions carefully, remembering that the program "
                                 "is case sensitive. Do not write unnecessary spaces.\n\n"
                                 "Please enter the tournament's name\n")
    tournament_venue: str = input("Please enter the tournament's venue\n")
    tournament_date: str = input("Enter the tournament's date. "
                                 "Please, respect the expected format yyyy/mm/dd\n")
    tournament_players_number: int = input("How many players are in the tournament\n")
    tournament_description: str = input("you can enter some remarks about the tournament right here\n")
    tournament_time_control: str = input("Choose between the three time control type\n1.bullet\n2.blitz\n3.rapid\n")
    tournament_round_numbers: str = input("How many rounds should they be in the tournament ?\n")
    return tournament_name, tournament_venue, tournament_date, tournament_players_number, tournament_description, tournament_time_control, tournament_round_numbers


def insert_player_info():
    # this functions immediately returns it's value in the model module.
    # The number of times it is used is also set in the model module.
    player_surname: str = input("Please enter the player's surname\n")
    player_first_name: str = input("Please enter the player's first name\n")
    player_birthday: str = input("Enter the player's date of birth. "
                                 "Please, respect the expected format yyyy/mm/dd\n")
    player_gender: str = input("Please enter the player's gender "
                               "(choose between 'men', 'women' or 'other')\n")
    player_rank: int = input("Please enter the player's rank\n")
    return player_surname, player_first_name, player_birthday, player_gender, player_rank


def insert_results(player1: str):
    # No computation should be done here. All we need to do is take result for each mach, store it and
    # transfer it in the controller.
    match_result = input(f"What was the result of the match ? Enter 'W' if {player1} winned, "
                         "'L' if he lost and 'D  if the match ended in a draw \n")
    return match_result


def modify_tournament_description():
    pass


def override_ranking():
    pass


def what_request():
    request = input("Do you need something from the database ? just enter the integer corresponding to your request:\n"
                    "1. a list with all the players from a tournament ranked alphabetically\n"
                    "2. a list with the ranking of all the players from a tournament\n"
                    "3. a list with the players from all the tournaments ranked alphabetically\n"
                    "4. a list with the ranking of all the players from all tournaments\n"
                    "5. a list with all the tournaments\n"
                    "6. a list of all the rounds in a tournament\n"
                    "7. a list of all the matches in a tournament\n"
                    "8. I don't need anything for the moment\n")
    return request


def requesting_tournament_name():
    which_tournament = input("which tournament are you refering to ?")
    return which_tournament


def requesting_table_to_save_first_round():
    manager_wants_to_save = input("Do you want to save some data ? Please enter the integer corresponding to your need:\n"
                                  "1. I need to save a table with all the tournament info\n"
                                  "2. I need to save a table with all the players info\n"
                                  "3. I need to save both tables\n"
                                  "4. I don't need to save anything for the moment\n")
    return manager_wants_to_save


def requesting_table_to_save_subsequent_round():
    manager_wants_to_save = input("Do you want to save some data ? Please enter the integer corresponding to your need:\n"
                                  "1. I need to save a table with all the players info\n"
                                  "2. I don't need to save anything for the moment\n")
    return manager_wants_to_save


def requesting_player_table_name():
    which_player = input("please, enter the player table name you are requesting")
    return which_player


# if I import it before, I'll run into circular importing
from controller import announce_pairing_for_first_round


def display_first_round_matches():
    pairing_announcement = announce_pairing_for_first_round()
    print(pairing_announcement)

