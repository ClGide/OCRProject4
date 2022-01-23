"""Displays data on matches as they happen in the tournament.
"""

from c_1_pairing_first_round import announce_pairing_for_first_round
from c_2_pairing_subsequent_rounds import (
    announce_pairing_for_subsequent_round,
    announce_ranking)


def display_first_round_matches(tournament):
    announce_pairing_for_first_round(tournament)


def display_subsequent_round_matches(tournament):
    announce_pairing_for_subsequent_round(tournament)


def display_ranking(tournament):
    announce_ranking(tournament)
