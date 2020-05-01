import logging
from datetime import datetime

import card as c
import deck
from errors import DeckEmptyError
from config import WAITING_TIME


class Player(object):
    """
    This class represents a player.
    It is basically a doubly-linked ring list with the option to reverse the
    direction. On initialization, it will connect itself to a game and its
    other players by placing itself behind the current player.
    """

    def __init__(self, game, user):
        self.cards = list()
        self.game = game
        self.user = user
        self.logger = logging.getLogger(__name__)

        # Check if this player is the first player in this game.
        """ if game.current_player:
						self.next = game.current_player
						self.prev = game.current_player.prev
						game.current_player.prev.next = self
						game.current_player.prev = self
				else:
						self._next = self
						self._prev = self
						game.current_player = self """

        self.turn_started = datetime.now()
        self.waiting_time = WAITING_TIME

    def __repr__(self):
        return repr(self.user)

    def __str__(self):
        return str(self.user)

    def draw_hand(self):
        """Draws a card from this deck"""
        try:
            hand = list()
            for _ in range(5):
                hand.append(self.game.deck.cards.pop())
                self.cards_dealt += 5
            return hand
        except IndexError:
            raise DeckEmptyError()

    def leave(self):
        self.logger.info(self.user + "left the game")
