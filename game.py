import logging
from datetime import datetime
from config import ADMIN_LIST, OPEN_LOBBY, MAX_PLAYERS, WAITING_TIME
from deck import Deck

import global_variables


class Game(object):
    """represents one game"""

    waiting_time = WAITING_TIME
    max_players = MAX_PLAYERS
    open = OPEN_LOBBY

    # mode = "DEFAULT_GAMEMODE"

    def __init__(self, chat):
        self.current_player = None
        self.starter = None
        self.started = False
        self.control_card = None
        self.control_player = None
        self.player_won = None
        self.first_player = None
        self.play_round = 0  # game has 5 rounds: each player plays 5 times
        self.game_round = 1
        self.game_info = list()
        self.game_players = list()
        self.nkap = False
        self.bet = 0
        self.winnings = 0  # what the user wins
        self.owner = ADMIN_LIST
        self.chat = chat
        self.last_card = None
        self.owner = ADMIN_LIST
        # self.job = global_variables.LMjobQueue
        self.deck = Deck()
        self.logger = logging.getLogger(__name__)

    @property
    def players(self):
        """returns a list of all players in game"""
        return self.game_players

    @property
    def current_player_index(self):
        ref = list(filter(lambda n: n.id ==
                          self.current_player.id, self.players))
        index = self.players.index(ref[0])
        return index

    @property
    def control_player_index(self):
        ref = list(filter(lambda n: n.id ==
                          self.control_player.id, self.players))
        index = self.players.index(ref[0])
        return index

    @property
    def next_player(self):
        next = self.players[(self.current_player_index + 1) %
                            len(self.players)]
        return next

    def turn(self):
        """ Change a turn and change the player """
        self.current_player = self.next_player
        self.current_player.turn_started = datetime.now()
        ''' self.job.stop()
        self.job.start() '''
        self.play_round += 1

    def turn_to_controler(self):
        """ Change the turn to the game_controler """
        self.current_player = self.players[self.control_player_index]

    def play_card(self, card):
        """
        Plays a card and triggers its effects.
        Should be called only from Player.play
        or on game start to play the first card
        """
        if self.control_card is None:
            self.control_player = self.current_player
            self.control_card = card

        elif takes_control(self.control_card, card):
            self.control_player = self.current_player
            self.control_card = card

        self.last_card = card
        self.turn()

    def get_user_in_game(self, user):
        ref = list(filter(lambda n: n.id == user.id, self.players))
        return ref[0]

    def start(self):
        self.deck.fill_cards()
        self.started = True
        # self.job.run_once(self.end_turn_by_afk, WAITING_TIME)

    def end_turn_by_afk(self, context):
        """ kill the turn and make the player afk """
        return


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
