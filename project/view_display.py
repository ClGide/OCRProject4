from controller_3 import announce_pairing_for_subsequent_round, announce_ranking, announce_pairing_for_first_round


def display_first_round_matches():
    pairing_announcement = announce_pairing_for_first_round()
    print(pairing_announcement)


def display_subsequent_round_matches():
    pairing_announcement = announce_pairing_for_subsequent_round()
    print(pairing_announcement)


def display_ranking():
    ranking_announcement = announce_ranking()
    print(ranking_announcement)

