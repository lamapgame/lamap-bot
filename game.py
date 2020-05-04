import logging
from datetime import datetime
from config import ADMIN_LIST, OPEN_LOBBY, MAX_PLAYERS
from deck import Deck
import card as c


class Game(object):
    """represents one game"""
    current_player = None
    starter = None
    started = False
    player_won = None
    owner = ADMIN_LIST
    players_list = list()
    max_players = MAX_PLAYERS
    open = OPEN_LOBBY

    #mode = "DEFAULT_GAMEMODE"

    def __init__(self, chat):
        self.chat = chat
        self.last_card = None
        owner = ADMIN_LIST

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
        """
        Plays a card and triggers its effects. 
        Should be called only from Player.play 
        or on game start to play the first card
        """
        self.logger.info("playing card:" + repr(card))
        self.last_card = card

    def start(self):
        self.started = True
