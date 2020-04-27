import logging
from datetime import datetime

from deck import Deck


class Game(object):
    """represents one game"""
    current_player = None
    starter = None
    mode = DEFAULT_GAMEMODE
    owner = ADMIN_LIST
    open = OPEN_LOBBY

    def __init__(self):
        super().__init__()
        self.chat = chat
        self.last_card = None

        self.deck = Deck()
        self.logger = logging.getLogger(__name__)

    @property
    def players(self):
        """returns a list of all players in game"""
        players = list()
        if not self.current_player:
            return players
        current_player = self.current_player
        itplayer = current_player.next
        players.append(current_player)
        while itplayer and itplayer is not current_player:
            players.append(itplayer)
            itplayer = itplayer.next
        return players

        def play_card(self, card):
            self.last_card

    def start(self):
        self.deck.shuffle()

        self.started = True
