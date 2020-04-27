from random import shuffle
import logging

import card as c
from card import Card
from errors import DeckEmptyError

# LaMap's 31 playing cards
LAMAP_CARDS = [
    'h_3', 'h_4', 'h_5', 'h_6', 'h_7', 'h_8', 'h_9', 'h_10', 'c_3', 'c_4', 'c_5', 'c_6',
    'c_7', 'c_8', 'c_9', 'c_10', 'd_3', 'd_4', 'd_5', 'd_6', 'd_7', 'd_8',
    'd_9', 'd_10', 's_3', 's_4', 's_5', 's_6', 's_7', 's_8', 's_9'
]


class Deck(object):
    """This class represents a deck of card"""

    def __init__(self):
        self.cards = LAMAP_CARDS
        self.graveyard = list()
        self.cards_dealt = 0
        self.logger = logging.getLogger(__name__)

        self.logger.info(self.cards)

    def shuffle(self):
        """Shuffles the deck"""
        self.logger.info("Shuffling Deck")
        shuffle(self.cards)
        return self.cards

    def draw(self):
        """Draws a card from this deck"""
        try:
            hand = list()
            for _ in range(5):
                hand.append(self.cards.pop())
            self.logger.info("Hand:", hand)
            return hand
        except IndexError:
            raise DeckEmptyError()
