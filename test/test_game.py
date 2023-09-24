import pytest
from telegram import User
from game import Game, MIN_PLAYER_NUMBER, MAX_PLAYER_NUMBER
from player import Player
from common.exceptions import (
    CannotRemoveControllerError,
    NotEnoughPlayersError,
    TooManyPlayersError,
    PlayerAlreadyInGameError,
)

# Dummy data
user1 = User(id=1, first_name="Ateba", is_bot=False)
user2 = User(id=2, first_name="Bassogog", is_bot=False)
user3 = User(id=3, first_name="Chokote", is_bot=False)
user4 = User(id=3, first_name="Donfack", is_bot=False)
user5 = User(id=3, first_name="Essani", is_bot=False)
player1 = Player(user1)
player2 = Player(user2)
player3 = Player(user3)
player4 = Player(user4)
player5 = Player(user5)


def test_initialize_game():
    game = Game(chat_id=100, user=user1)
    assert game.chat_id == 100
    assert not game.started
    assert game.creator == user1


def test_add_player():
    game = Game(chat_id=100, user=user1)
    game.add_player(player1)
    assert len(game.players) == 1


def test_add_too_many_players():
    # set the max player number to 2
    game = Game(chat_id=100, user=user1, max_player_number=2)
    game.add_player(player1)
    game.add_player(player2)
    with pytest.raises(TooManyPlayersError):
        game.add_player(Player(user4))


def test_add_same_player_twice():
    game = Game(chat_id=100, user=user1)
    game.add_player(player1)
    with pytest.raises(PlayerAlreadyInGameError):
        game.add_player(player1)


def test_remove_player_ends_game_single_player_left():
    game = Game(chat_id=100, user=user1)
    game.add_player(player1)
    game.add_player(player2)
    game.remove_player(player1)
    assert not game.started  # Assuming end_game() resets the started flag


""" def test_remove_current_player_error():
    game = Game(chat_id=100, user=user1)
    game.add_player(player1)
    game.add_player(player2)
    game.start_game()
    with pytest.raises(CannotRemoveControllerError):
        game.remove_player(game.current_player) """


def test_remove_player_not_enough_players_error():
    game = Game(chat_id=100, user=user1)
    game.add_player(player1)
    with pytest.raises(NotEnoughPlayersError):
        game.remove_player(player1)


def test_start_game_not_enough_players():
    game = Game(chat_id=100, user=user1)
    game.add_player(player1)
    with pytest.raises(NotEnoughPlayersError):
        game.start_game()


def test_start_game_with_enough_players():
    game = Game(chat_id=100, user=user1)
    game.add_player(player1)
    game.add_player(player2)
    game.start_game()
    assert game.started
