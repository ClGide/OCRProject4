from controller_1 import announce_pairing_for_subsequent_round, announce_ranking, announce_pairing_for_first_round


def display_first_round_matches(tournament):
    pairing_announcement = announce_pairing_for_first_round(tournament)
    print(pairing_announcement)


def display_subsequent_round_matches(tournament):
    pairing_announcement = announce_pairing_for_subsequent_round(tournament)
    print(pairing_announcement)


def display_ranking(tournament):
    ranking_announcement = announce_ranking(tournament)
    print(ranking_announcement)

