import controller
from unittest import TestCase
from unittest.mock import patch


"""
# Each time there is some input, I only need to be sure the info requested in the VIEW is used 
# to instantiate a TOURNAMENT, ROUND or PLAYER without problems. The size of the input vary according 
# to how many players are in the tournament, but the format stays the same. 
# All statements, even if they do not take the tournament instance as an argument, directly or  
# indirectly rely on it.


storing_player_instances_in_tournament = CreatingPlayerStoringInTournament(tournament)

>tournament_name = french presidents
>tournament_venue = Elysee
>tournament's date = 2022/01/04
>players_number = 4
>descriptions = nothing to write
>number_of_rounds = bullet
>rounds = 3

>player_last_name = Macron
>player_first_name = Emmanuel 
>player_date_of_birth = 1977/12/21
>player_sex = men
>player_ranking = 1

>player_last_name = Hollande
>player_first_name = Francois 
>player_date_of_birth = 1954/08/12
>player_sex = men
>player_ranking = 2

>player_last_name = Sarkozy
>player_first_name = Nicolas 
>player_date_of_birth = 1955/01/28
>player_sex = men
>player_ranking = 3

>player_last_name = Chirac
>player_first_name = Jacques 
>player_date_of_birth = 1932/11/29
>player_sex = men
>player_ranking = 4
  
announce_pairing_for_first_round()
storing_round_instances_in_tournament = CreatingRoundStoringInTournament(tournament)
time_control()
storing_match_instances_in_tournament = CreatingMatchStoringInRoundOne(1)

>"W"
>"W"

matches_from_last_round = tournament.rounds["Round 1"].dict_of_matches
update_all_players_attrs_after_round(matches_from_last_round)
for i in range(1, tournament.number_of_rounds):
    possibly_saving_data = SaveDataInDB(tournament)

    >"2" 

    announce_pairing_for_subsequent_round()
    time_control(tournament)
    storing_more_match_instances_in_tournament = CreatingMatchStoringInSubsequentRounds(i + 1)
    
    >"D"
    >"L"
        
    matches_from_last_round = tournament.rounds[f"Round {i + 1}"].dict_of_matches
    update_all_players_attrs_after_round(matches_from_last_round)
possibly_saving_data = SaveDataInDB(tournament)

> "3"

"""