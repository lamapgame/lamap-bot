import pytest
from orchestrator import Orchestrator
from common.exceptions import GameAlreadyExistError
from test.mock_objects import mocked_message_update, mocked_context, mocked_user


def test_orchestrator_initialization():
    orchestrator = Orchestrator()
    assert isinstance(orchestrator.games, dict)
    assert not orchestrator.games  # Ensure games dictionary is empty


def test_new_game():
    orchestrator = Orchestrator()
    chat_id = 12345
    game_creator = mocked_user

    game = orchestrator.new_game(
        chat_id, game_creator, mocked_message_update, mocked_context
    )
    assert chat_id in orchestrator.games

    # Test trying to create another game for the same chat
    with pytest.raises(GameAlreadyExistError):
        orchestrator.new_game(
            chat_id, game_creator, mocked_message_update, mocked_context
        )


def test_end_game():
    orchestrator = Orchestrator()
    chat_id = 12345
    game_creator = mocked_user

    game = orchestrator.new_game(
        chat_id, game_creator, mocked_message_update, mocked_context
    )
    assert chat_id in orchestrator.games

    orchestrator.end_game(chat_id, mocked_context)
    assert chat_id not in orchestrator.games

    # Test trying to end a game that doesn't exist
    with pytest.raises(GameAlreadyExistError):
        orchestrator.end_game(chat_id, mocked_context)
