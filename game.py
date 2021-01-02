import logging
from datetime import datetime
from config import ADMIN_LIST, OPEN_LOBBY, MAX_PLAYERS, WAITING_TIME
from deck import Deck

import global_variables


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
    game_round = 1
    game_info = list()
    game_players = list()
    nkap = False
    bet = 0

    winnings = 0  # what the user wins
    owner = ADMIN_LIST
    waiting_time = WAITING_TIME
    max_players = MAX_PLAYERS
    open = OPEN_LOBBY

    # mode = "DEFAULT_GAMEMODE"

    def __init__(self, chat):
        self.chat = chat
        self.last_card = None
        owner = ADMIN_LIST
        self.job = global_variables.LMjobQueue
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
        self.job.stop()
        self.job.start()
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

    def start(self):
        self.deck.fill_cards()
        self.started = True
        self.job.run_once(self.end_turn_by_afk, WAITING_TIME)

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
