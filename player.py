import logging
from datetime import datetime

import card as c
import deck
from errors import DeckEmptyError
from config import WAITING_TIME


class Player(object):
    """
    This class represents a player.
    It is basically a simple list. On initialization, it will connect itself to a game and its
    other players by placing itself behind the current player.
    """

    def __init__(self, game, user):
        self.cards = list()
        self.game = game
        self.user = user
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
        c_card = self.game.control_card
        cards = self.cards

        for card in cards:
            if self._card_playable(c.from_str(card), c_card):
                playable.append(card)

        # if there's no single card matching the last card,
        # then make all of them playable
        if not playable:
            self.logger.debug("No matching card!")
            for card in cards:
                playable.append(card)

        return playable

    def _card_playable(self, card, c_card):
        ''' Check if a card can be played '''
        is_playable = True
        # if there's a control card, then if he should play that
        if c_card is not None:
            # if they do not have the same suit, they cannot be playable
            if card.suit is not c_card.suit:
                self.logger.debug("No match")
                is_playable = False

        return is_playable

    def leave(self):
        self.logger.debug(self.user + "left the game")
