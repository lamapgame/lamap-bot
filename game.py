from datetime import datetime

from deck import Deck
from player import Player


class Game:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.started_date = datetime.now()
        self.players: list[Player] = []
        # TODO: implement deck of cards (see deck.py) ->
        # dylantientcheu/lamap-bot/deck.py and dylantientcheu/lamap-bot/card.py
        self.deck = Deck()

        # add various game options here
        # (number of players, koras, or more configuration options)
        self.max_player_number = 4
        self.has_quick_wins = True
        self.has_koras = True
        self.has_dbl_koras = True
