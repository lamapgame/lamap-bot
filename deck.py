from random import shuffle
import logging

import card as c
from card import Card
from errors import DeckEmptyError

# LaMap's 31 playing cards
LAMAP_CARDS = shuffle([
    'h_3', 'h_4', 'h_5', 'h_6', 'h_7', 'h_8', 'h_9', 'h_10', 'c_3', 'c_4', 'c_5', 'c_6',
    'c_7', 'c_8', 'c_9', 'c_10', 'd_3', 'd_4', 'd_5', 'd_6', 'd_7', 'd_8',
    'd_9', 'd_10', 's_3', 's_4', 's_5', 's_6', 's_7', 's_8', 's_9'
])  # shuffle cards directly


class Deck(object):
    """This class represents a shuffled deck of card"""

    def __init__(self):
        self.cards = LAMAP_CARDS  # create game cards
        self.graveyard = list()
        self.cards_dealt = 0
        self.logger = logging.getLogger(__name__)
