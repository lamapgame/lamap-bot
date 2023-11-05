import pytest
from game import Game
from deck import Card
from player import Player
from common.exceptions import (
    NotEnoughPlayersError,
    PlayerNotInGameError,
    TooManyPlayersError,
    PlayerAlreadyInGameError,
)
from test.mock_objects import user1, user4, player1, player2


def test_initialize_game():
    game = Game(chat_id=100, user=user1)
    assert game.chat_id == 100
    assert not game.started
    assert game.creator == user1


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


sample_card = Card("h", 10)


@pytest.fixture
def new_game():
    return Game(chat_id=12345, user=user1)


@pytest.fixture
def new_player():
    return Player(user1)


@pytest.fixture
def game_with_two_players(new_game):
    new_game.add_player(player2)
    another_player = player1
    new_game.add_player(another_player)
    return new_game


def test_play_card(game_with_two_players):
    ...


def test_next_round(game_with_two_players):
    ...


def test_is_playable_card(game_with_two_players):
    ...


def test_get_player(game_with_two_players, new_player):
    # Get a valid player
    retrieved_player = game_with_two_players.get_player(new_player.id)
    assert retrieved_player == new_player

    # Try to get a player that's not in the game
    with pytest.raises(PlayerNotInGameError):
        game_with_two_players.get_player(9999)  # some random ID not in the game


def test_remove_current_player(game_with_two_players):
    ...


def test_add_message_to_delete(new_game):
    # Add a message and ensure it's stored correctly
    new_game.add_message_to_delete(101)
    assert 101 in new_game.messages_to_delete


def test_game_end_conditions(game_with_two_players):
    ...
