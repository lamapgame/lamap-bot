from datetime import datetime
from random import shuffle
from typing import Literal, NamedTuple

from telegram import User
from common.exceptions import (
    CannotRemoveControllerError,
    NotEnoughPlayersError,
    PlayerIsBanned,
    PlayerIsPoor,
    PlayerNotInGameError,
    PlayerRemovedBeforeGameStart,
    TooManyPlayersError,
    PlayerAlreadyInGameError,
)
from common.models import compute_game_stats, get_stats

from deck import Card, Deck
from player import Player


MIN_PLAYER_NUMBER = 2
MAX_PLAYER_NUMBER = 4

ReasonType = Literal["NORMAL", "KORA", "DBL_KORA", "AFK", "SPECIAL", "QUIT", "KILL"]


class Play(NamedTuple):
    """Play typing"""

    player: Player | None
    move: Card


class RoundInfo(NamedTuple):
    """Round information typing"""

    round: int
    plays: list[Play]
    controller: Player | None
    controlling_card: Card | None


class Game:
    """An instance of the game"""

    def __init__(
        self,
        chat_id: int,
        user: User,
        max_player_number: int = MAX_PLAYER_NUMBER,
        has_quick_wins: bool = True,
        has_koras: bool = True,
        has_dbl_koras: bool = True,
        time_to_play: int = 60,
        nkap: int = 0,
    ):
        self.chat_id = chat_id
        self.started_date = None
        self.players: list[Player] = []
        self.deck = Deck()
        self.started = False
        self.creator = user
        self.current_player = None
        self.nkap = nkap
        self.round = 1
        self.play_history: list[Play] = []
        self.round_history: list[RoundInfo] = []
        self.controlling_player = None
        self.controlling_card = None
        self.prev_controlling_card = None
        self.killer: User | None = None

        # end of game computation
        self.winners: list[Player] = []
        self.losers: list[Player] = []
        self.quitters: list[Player] = []
        self.end_reason: ReasonType = "NORMAL"
        self.amount_won = 0

        # messages to delete when the game starts
        self.messages_to_delete: list[int] = []

        # game options
        self.max_player_number = max_player_number
        self.has_quick_wins = has_quick_wins
        self.has_koras = has_koras
        self.has_dbl_koras = has_dbl_koras
        self.time_to_play = time_to_play
        self.cards_design: Literal["DEFAULT", "GALACTIC", "LUXURY"] = "DEFAULT"

    @property
    def current_player_index(self) -> int:
        if self.current_player is None:
            raise ValueError("No current player")
        return self.players.index(self.current_player)

    @property
    def number_of_players(self) -> int:
        return len(self.players)

    def add_player(self, player: Player) -> None:
        user, stats = get_stats(player.user)
        if not user.verified:
            raise PlayerIsBanned()

        if stats.nkap < self.nkap:
            raise PlayerIsPoor()

        # check if the player is already in game
        if player.id in [p.id for p in self.players]:
            raise PlayerAlreadyInGameError()

        # check if the game is full
        if len(self.players) < self.max_player_number:
            self.players.append(player)
            self.deck.cut_cards(player)
        else:
            raise TooManyPlayersError()

    def get_player(self, player_id: int) -> Player:
        for player in self.players:
            if player.id == player_id:
                return player
        raise PlayerNotInGameError()

    def get_next_player(self) -> Player:
        if self.current_player is None:
            raise ValueError("No current player")
        next_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[next_player_index]

    def kick_player(self, player_id: int) -> None:
        player = self.get_player(player_id)

        # if the player controls the game, they cannot be kicked
        if self.controlling_player and self.controlling_player == player:
            raise CannotRemoveControllerError()

        # if the game isn't started, remove the player thats it
        if not self.started:
            self.players.remove(player)
            raise PlayerRemovedBeforeGameStart()
        else:
            # if the game is started...
            self.players.remove(player)

            # if this is the first round, remove the player and
            # make them not koratable
            if self.round == 1:
                player.is_koratable = False
                self.quitters.append(player)
            else:
                self.quitters.append(player)

            # if the player is the current player, move to the next player
            # if self.current_player and self.current_player == player:

        # ends the game if there are not enough players left
        if len(self.players) < MIN_PLAYER_NUMBER and self.started:
            self.end_game("QUIT")
        else:
            self.next_round()

    def end_game(
        self, reason: ReasonType = "NORMAL"
    ) -> tuple[list[Player], list[Player], ReasonType]:
        """Compute the score and end the game by setting the winners and losers"""
        self.started = False
        self.end_reason = reason

        if reason == "KILL":
            return [], [], reason

        # if the game ends by special card
        if reason == "SPECIAL":
            if (
                self.play_history
                and self.play_history[-1].move.suit == "x"
                and self.play_history[-1].player
            ):
                winner = self.play_history[-1].player
                self.winners = [winner]
                self.losers = [p for p in self.players if p.id != winner.id]

        # if the game ends by afk
        if reason == "AFK":
            if self.current_player is None:
                raise ValueError("No current player: cannot end game properly")

            self.losers = [self.current_player]
            self.winners = [p for p in self.players if p.id != self.current_player.id]

        # if the game ends by player quitting
        if reason == "QUIT":
            self.losers = self.quitters
            # winners are the players who didn't quit
            self.winners = [p for p in self.players if p.id not in self.quitters]

        # in case the game ends normally
        if reason == "NORMAL":
            if not self.controlling_player or not self.controlling_card:
                return [], [], "NORMAL"

            # the winner is the player who controls the last round
            self.winners.append(self.controlling_player)

            if self.controlling_card.value == 3:
                reason = "KORA"
                # if round 4's controlling card was 3, it is double kora
                if (
                    self.round > 3
                    and self.round_history[3].controlling_card
                    and self.round_history[3].controlling_card.value == 3
                    and self.round_history[3].controller == self.controlling_player
                ):
                    reason = "DBL_KORA"

            # if the game ends by kora or dbl kora
            # the reason is set to kora or dbl kora
            self.end_reason = reason

            self.losers = [
                p for p in self.players if p.id != self.controlling_player.id
            ]

        # calculate the score and distribute the points and money
        compute_game_stats(self)
        return self.winners, self.losers + self.quitters, reason

    def add_message_to_delete(self, message_id: int) -> None:
        self.messages_to_delete.append(message_id)

    def start_game(self):
        if len(self.players) < MIN_PLAYER_NUMBER:
            raise NotEnoughPlayersError()

        self.started = True
        # a deck is shuffled by default
        shuffle(self.players)  # randomize list of players
        self.current_player = self.players[0]  # set the first player
        self.started_date = datetime.now()
        self.round = 1

    def play_card(self, player: Player, card: Card) -> tuple[bool, bool]:
        """
        Plays the specified card from the player,
        ! returns a boolean tuple (card_played, card_correctly_played)
        ! card_played is True if the card was played, False otherwise
        ! card_correctly_played is True only
        ! if the card meets conditions to play the round
        False otherwise
        """
        rest_of_cards = [c for c in player.hand_of_cards if c.id != card.id]

        play = Play(player, card)
        card_played, card_correctly_played = False, False

        is_first_card = False  # first card of a round

        # make sure the player is the current player
        if self.current_player and self.current_player.id == player.id:
            # make sure the card is in the player's hand
            if card in player.hand_of_cards:
                # for the first round make the current player controller
                if self.controlling_card is None:
                    self.controlling_player = player
                    self.controlling_card = card
                    card_played, card_correctly_played = True, True
                    is_first_card = True

                # if the card is of special type (x) it is always playable
                if card.suit == "x":
                    self.controlling_player = player
                    self.controlling_card = card
                    card_played, card_correctly_played = True, True

                # if this is the first card, the next control flow
                # will be skipped
                if not is_first_card:
                    # the player takes control if the condition is met
                    # otherwise plays but doesnt take control
                    if card.suit == self.controlling_card.suit:
                        if card.value > self.controlling_card.value:
                            self.controlling_card = card
                            self.controlling_player = player

                        card_played, card_correctly_played = True, True

                    # if the player has the controlling suit, only it should be playable
                    # otherwise they can play anything
                    elif self.controlling_card.suit in [c.suit for c in rest_of_cards]:
                        card_played, card_correctly_played = True, False
                    else:
                        card_played, card_correctly_played = True, True

        # if the player is not the current player, they can play
        # but won't correctly play
        else:
            card_played, card_correctly_played = True, False

            # if it is a special card, it is always playable
            if card.suit == "x":
                card_correctly_played = True

        # remove the card from the player's hand
        # and add it to the play history if it was played correctly
        if card_played and card_correctly_played:
            player.hand_of_cards.remove(card)
            self.play_history.append(play)
            self.next_round()

        return card_played, card_correctly_played

    def next_round(self):
        """Check if the round is over and move to the next round"""
        self.prev_controlling_card = self.controlling_card

        # if the last card played was a special card, the round is over
        if self.play_history and self.play_history[-1].move.suit == "x":
            self.end_game("SPECIAL")
            return

        # if all players played, move to the next
        if len(self.play_history) == len(self.players):
            self.current_player = self.controlling_player
            self.round_history.append(
                RoundInfo(
                    self.round,
                    self.play_history,
                    self.controlling_player,
                    self.controlling_card,
                )
            )
            self.play_history = []
            self.prev_controlling_card = self.controlling_card
            self.controlling_card = None
            if self.round == 5:
                self.controlling_card = self.prev_controlling_card
                self.end_game()
                return

            self.round += 1
            return

        self.current_player = self.get_next_player()

    def is_playable_card(self, card: Card, cards: list[Card]) -> bool:
        """
        Checks if the card is playable
        """
        rest_of_cards = [c for c in cards if c.id != card.id]
        if (
            self.round == 1
            or self.controlling_card is None
            or self.controlling_player is None
        ):
            return True
        else:
            # if card is of special type (x) it is always playable
            if card.suit == "x":
                return True
            # if the player has the controlling suit it should not be playable
            if card.suit in [c.suit for c in rest_of_cards]:
                return False

        return False
