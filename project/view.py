def tournament_info():
    # with the input from this function, the controller will instantiate the tournament object
    pass


def insert_player_info():
    # this functions immediately returns it's value in the model module.
    # The number of times it is used is also set in the model module.
    player_surname: str = input(f"Please enter the player's surname")
    player_first_name: str = input(f"Please enter the player's first name")
    player_birthday: str = input(f"Please enter the player's date of birth")
    player_gender = str = input(f"Please enter the player's gender")
    player_rank = int = input(f"Please enter the player's rank")
    return player_surname, player_first_name, player_birthday, player_gender, player_rank


def define_time_control(tournament):
    time_control = input(f"what time-control type should the {tournament} implement ? Enter"
                 f"'rapid', 'blitz' or 'bullet")


def insert_results(player1):
    # No computation should be done here. All we need to do is take result for each mach, store it and
    # transfer it in the controller.
    match_result = input(f"What was the result of the match ? Enter 'W' if {player1} winned, "
                   "'L' if he lost and 'D  if the match ended in a draw")
