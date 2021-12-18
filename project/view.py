def tournament_info():
    # with the input from this function, the controller will instantiate the tournament object
    tournament_name: str = input("Please enter the tournament's name\n")
    tournament_venue: str = input("Please enter the tournament's venue\n")
    tournament_date: str = input("Please enter the tournament's date\n")
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
    player_birthday: str = input("Please enter the player's date of birth\n")
    player_gender: str = input("Please enter the player's gender\n")
    player_rank: int = input("Please enter the player's rank\n")
    return player_surname, player_first_name, player_birthday, player_gender, player_rank


def insert_results(player1:str):
    # No computation should be done here. All we need to do is take result for each mach, store it and
    # transfer it in the controller.
    match_result = input(f"What was the result of the match ? Enter 'W' if {player1} winned, "
                   "'L' if he lost and 'D  if the match ended in a draw \n")
    return match_result

def modify_tournament_description():
    pass

