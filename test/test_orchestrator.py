import pytest
from game import Game
from orchestrator import Orchestrator, GameAlreadyExistError


class TestOrchestrator:
    def setup_method(self):
        self.orchestrator = Orchestrator()

    def test_new_game(self):
        chat_id = "123"
        self.orchestrator.new_game(chat_id)
        assert chat_id in self.orchestrator.games
        assert isinstance(self.orchestrator.games[chat_id], Game)

        with pytest.raises(GameAlreadyExistError):
            self.orchestrator.new_game(chat_id)

    def test_end_game(self):
        chat_id = "123"
        with pytest.raises(GameAlreadyExistError):
            self.orchestrator.end_game(chat_id)

        self.orchestrator.new_game(chat_id)
        self.orchestrator.end_game(chat_id)
        assert chat_id not in self.orchestrator.games
