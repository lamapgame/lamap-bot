import pytest
from telegram import User
from game import Game
from orchestrator import Orchestrator
from common.exceptions import GameAlreadyExistError

# Dummy user for testing
user = User(id=123, first_name="Test", is_bot=False)


def test_initialize_new_game():
    o = Orchestrator()
    game = o.new_game(chat_id=123456, game_creator=user)
    assert isinstance(game, Game)
    assert 123456 in o.games


def test_cannot_initialize_multiple_games_in_same_chat():
    o = Orchestrator()
    o.new_game(chat_id=123456, game_creator=user)

    with pytest.raises(GameAlreadyExistError):
        o.new_game(chat_id=123456, game_creator=user)


def test_cannot_end_nonexistent_game():
    o = Orchestrator()
    with pytest.raises(GameAlreadyExistError):
        o.end_game(chat_id=123456)


def test_end_game():
    o = Orchestrator()
    o.new_game(chat_id=123456, game_creator=user)
    assert 123456 in o.games
    o.end_game(chat_id=123456)
    assert 123456 not in o.games
