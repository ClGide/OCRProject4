"""Displays data on matches as they happen in the tournament.
"""

from controller_1 import (announce_pairing_for_subsequent_round,
                          announce_ranking,
                          announce_pairing_for_first_round)


def display_first_round_matches(tournament):
    announce_pairing_for_first_round(tournament)


def display_subsequent_round_matches(tournament):
    announce_pairing_for_subsequent_round(tournament)


def display_ranking(tournament):
    announce_ranking(tournament)
