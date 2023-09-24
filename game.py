from datetime import datetime
from random import shuffle

from telegram import User
from common.exceptions import (
    CannotRemoveControllerError,
    NotEnoughPlayersError,
    TooManyPlayersError,
    PlayerAlreadyInGameError,
)

from deck import Deck
from player import Player


MIN_PLAYER_NUMBER = 2
MAX_PLAYER_NUMBER = 4


class Game:
    def __init__(
        self,
        chat_id: int,
        user: User,
        max_player_number: int = MAX_PLAYER_NUMBER,
        has_quick_wins: bool = True,
        has_koras: bool = True,
        has_dbl_koras: bool = True,
        time_to_play: int = 60,
    ):
        self.chat_id = chat_id
        self.started_date = None
        self.players: list[Player] = []
        self.deck = Deck()
        self.started = False
        self.creator = user
        self.current_player = None
        self.bet = 0
        self.round = 0

        # messages to delete when the game starts
        self.messages_to_delete: list[int] = []

        # game options
        self.max_player_number = max_player_number
        self.has_quick_wins = has_quick_wins
        self.has_koras = has_koras
        self.has_dbl_koras = has_dbl_koras
        self.time_to_play = time_to_play

    def add_player(self, player: Player) -> None:
        # todo: [db] check if the player is banned
        # todo: [db] check if the player has enough currency

        # check if the player is already in game
        if player.id in [p.id for p in self.players]:
            raise PlayerAlreadyInGameError()

        # check if the game is full
        if len(self.players) < self.max_player_number:
            self.players.append(player)
        else:
            raise TooManyPlayersError()

    def remove_player(self, player: Player) -> None:
        self.players.remove(player)
        if self.current_player == player:
            raise CannotRemoveControllerError()
        if len(self.players) == 1:
            self.end_game()
            return
        if len(self.players) < MIN_PLAYER_NUMBER:
            raise NotEnoughPlayersError()

    def end_game(self) -> None:
        self.started = False
        pass

    def add_message_to_delete(self, message_id: int) -> None:
        self.messages_to_delete.append(message_id)

    def start_game(self):
        if len(self.players) < MIN_PLAYER_NUMBER:
            raise NotEnoughPlayersError()

        self.started = True
        self.deck.shuffle_cards()  # shuffle cards
        shuffle(self.players)  # randomize list of players
        self.current_player = self.players[0]  # set the first player
        self.started_date = datetime.now()
        self.round = 1
