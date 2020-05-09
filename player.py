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
        self.controls_game = False
        self.logger = logging.getLogger(__name__)

        # Check if this player is the first player in this game.
        if game.current_player:
            self.next = game.current_player
            self.prev = game.current_player.prev
            game.current_player.prev.next = self
            game.current_player.prev = self
        else:
            self._next = self
            self._prev = self
            game.current_player = self

        self.turn_started = datetime.now()
        self.waiting_time = WAITING_TIME

    def __repr__(self):
        return repr(self.user)

    def __str__(self):
        return str(self.user)

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, player):
        self._next = player

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, player):
        self._prev = player

    def play(self, card):
        self.cards.remove(card)
        self.game.play_card(card)

    def draw_hand(self):
        """Draws a card from this deck"""
        game_deck = self.game.deck
        try:
            for _ in range(5):
                self.cards.append(game_deck.cards.pop())
            game_deck.cards_dealt += 5
        except IndexError:
            raise DeckEmptyError()

    def playable_cards(self):
        """Returns a list of the cards this player can play right now"""

        playable = list()
        last = self.game.last_card

        self.logger.debug("Last card was " + str(last))

        cards = self.cards

        # You may only play a +4 if you have no cards of the correct suit
        self.bluffing = False
        for card in cards:
            if self._card_playable(card):
                self.logger.debug("Matching!")
                playable.append(card)

        return playable

    def _card_playable(self, card):
        ''' Check if a card can be played '''
        return True

    def leave(self):
        self.logger.info(self.user + "left the game")
