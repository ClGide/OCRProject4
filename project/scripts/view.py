"""Requests the information from the user.

This module could be divided into three parts each defining three functions.

In the first part, the data used to instantiate the tournament, the players,
the rounds and the matches is collected. Those classes are defined in
models.py. Their instances are dynamically created by methods defined in
c_3_player_instantiation.py, c_4_round_instantiation.py and
c_5_match_instantiation.py

In the second part, functions enabling the user to
override a player's ranking or a tournament's description are defined.
Those functions are called in c_8_modify_attributes.py.

In the third part, functions enabling the manager to save or retrieve
data from the database are defined. The functions are used in c_6_save_data.py
and c_7_retrieve_data.py.
"""

from typing import Tuple


def collect_tournament_info() -> Tuple[str, str, str, str, str, str, str]:
    """collects the data necessary to instantiate a tournament object.

    The functions that checks the values inputted by the user are
    defined in models.py.

    Returns: a tuple of values that can be given as one argument(preceded
        by the unpacking '*') to Tournament.
    """

    tournament_name: str = (
        input("Hi, we hope our program will help you store "
              "all the data you need on your chess tournaments.\n"
              "Please follow the instructions carefully, remembering that the"
              " program is case sensitive."
              " Do not type unnecessary spaces.\n"
              "Also, two tournaments cannot"
              " be saved with the same name in the database.\n"
              "If, for example,"
              " a tournament named 'cheese' is already in the database, "
              "and you name the present"
              " tournament 'cheese',\n"
              "when you'll save it the previous 'cheese'"
              " tournament will be deleted.\n\n"
              "Please enter the tournament's name\n"))
    tournament_venue: str = input("Please enter the tournament's venue\n")
    tournament_date: str = input("Enter the tournament's date. "
                                 "Please, respect the expected format"
                                 " yyyy/mm/dd\n")
    tournament_players_number: str = input("How many players are in "
                                           "the tournament\n")
    tournament_description: str = input("you can enter some remarks about the"
                                        " tournament right here\n")
    tournament_time_control: str = input("Choose between the"
                                         " three time control types"
                                         "\n1.bullet (3 min/round)"
                                         "\n2.blitz (5 min/round)"
                                         "\n3.rapid (20 min/round)\n")
    tournament_round_numbers: str = input("How many rounds will be in "
                                          "the tournament ?\n")

    return (tournament_name, tournament_venue,
            tournament_date, tournament_players_number,
            tournament_description, tournament_time_control,
            tournament_round_numbers)


def collect_results(player1: str) -> str:
    """Collects the result of a match from the user.

    Args:
        player1: the player's last name who won, made
            a draw or lost.

    Returns: a single char describing the result.
    """
    match_result = input(f"What was the result of the match ?"
                         f" Enter 'W' if {player1} won, "
                         "'L' if he lost and 'D  if the match"
                         " ended in a draw \n")
    return match_result


def collect_player_info() -> Tuple[str, str, str, str, str]:
    """collects the data necessary to instantiate a Player object.

    The functions that checks the values inputted by the user are
    defined in models.py.

    Returns: a tuple of values that can be given as one argument(preceded
        by the unpacking '*') to Player.
    """
    player_surname: str = input("Please enter the player's surname\n")
    player_first_name: str = input("Please enter the player's first name\n")
    player_birthday: str = input("Enter the player's date of birth. "
                                 "Please, respect the expected format"
                                 " yyyy/mm/dd\n")
    player_gender: str = input("Please enter the player's gender "
                               "(choose between 'men', 'women' or 'other')\n")
    player_rank: str = input("Please enter the player's rank\n")

    return (player_surname, player_first_name, player_birthday,
            player_gender, player_rank)


def override_tournament_description() -> str:
    """Overrides the tournament's description while it takes place.

    Returns:
        If a non-empty string is inputted, the string becomes the new
        tournament description.
    """
    new_description: str = (
        input("Do you want to override the tournament's description ?\n"
              "If you don't need anything, just click ENTER\n"
              "Otherwise, enter the new description\n"
              "Remember that in order to store the changes in the DB,"
              " you need to save the tournament table\n"))
    return new_description


def override_player_ranking() -> str:
    """Returns the name of the player which ranking will be overridden.

    Enables the user to override the player's ranking
    while the tournament takes place. If the user enter a valid player
    LAST name, the complete_override_player_ranking is
    called from c_8_modify_attributes.py.
    """
    which_player: str = input("Do you want to override"
                              " one player's ranking ?\n"
                              "If you don't need anything, just click ENTER\n"
                              "Otherwise, enter the player's LAST NAME\n"
                              "Remember that in order to store"
                              " the changes in the DB, "
                              "you need to save the player table\n")
    return which_player


def complete_override_player_ranking() -> str:
    """Returns the new ranking of a player.

    Enables the user to override the player's ranking
    while the tournament takes place. The player's which ranking
    is overridden was inputted before in override_player_ranking().
    """
    new_rank: str = input("What's the new ranking of the player\n"
                          "Please, only enter the number\n")
    return new_rank


def what_table_to_save() -> str:
    """Enables the user to specify what table needs to be saved.

    Returns:
        a char corresponding to the table the user wants to save in DB.
    """
    manager_wants_to_save = input(
        "Do you want to save some data ? "
        "Please enter the number corresponding to your need:\n"
        "1. I need to save a table with all the tournament info\n"
        "2. I need to save a table with all the players info\n"
        "3. I need to save both tables\n"
        "4. I don't need to save anything for the moment\n")
    return manager_wants_to_save


def what_data_to_read() -> str:
    """Enables the user to specify what table needs to be retrieved.

    Returns:
        a single char corresponding to the table the user wants to retrieve
        from the DB.
    """
    request = input("Do you need something from the database ?"
                    " just enter the number corresponding to your request:\n"
                    "1. a list with all the players from a tournament"
                    " ranked alphabetically\n"
                    "2. a list with the ranking of all the players"
                    " from a tournament\n"
                    "3. a list with the players from all the tournaments"
                    " ranked alphabetically\n"
                    "4. a list with the ranking of all the players"
                    " from all tournaments\n"
                    "5. a list with all the tournaments\n"
                    "6. a list of all the rounds in a tournament\n"
                    "7. a list of all the matches in a tournament\n"
                    "8. I don't need anything for the moment\n")
    return request


def what_tournament_name():
    """Completes the request specified before in what_data_to_read().
    """
    which_tournament = input("which tournament are you referring to ?")
    return which_tournament
