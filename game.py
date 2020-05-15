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
    control_card = None
    control_player = None
    player_won = None
    first_player = None
    play_round = 0  # game has 5 rounds: each player plays 5 times
    owner = ADMIN_LIST
    max_players = MAX_PLAYERS
    open = OPEN_LOBBY

    # mode = "DEFAULT_GAMEMODE"

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

    def turn(self, card):
        """ Change a turn and change the player """
        # self.logger.debug(f"Next player {self.current_player.next.user.name}")
        if self.current_player.user.id == self.first_player.user.id:
            self.play_round += 1
            if self.play_round > 1:
                self.current_player = self.control_player
                self.control_card = None

        else:
            self.current_player = self.current_player.next
            self.current_player.turn_started = datetime.now()

    def play_card(self, card):
        """
        Plays a card and triggers its effects.
        Should be called only from Player.play
        or on game start to play the first card
        """
        if self.current_player.user.id == self.first_player.user.id and self.play_round > 1:
            self.control_card = None

        if self.control_card is None:
            self.control_player = self.current_player
            self.control_card = card

        else:
            if takes_control(self.control_card, card):
                self.control_player = self.current_player
                self.control_card = card

        # self.logger.info("playing card:" + repr(card))
        self.turn(card)

    def start(self):
        self.started = True


def takes_control(previous, current):
    """ Determine if a card takes control """
    pv = int(previous.value)
    cv = int(current.value)
    if previous.suit is current.suit:
        if cv > pv:
            return True
        else:
            return False
    else:
        return False
