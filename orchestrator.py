from game import Game
from common.exceptions import GameAlreadyExistError


class Orchestrator:
    """
    ## The Grand O
    - Manages **EVERY** game initiated on Telegram.
    - Communicates with players globally (warnings, upcoming games, ban status, money drops).
    - Acts as a central point for systems to communicate about game events and state changes.
    For instance, the Orchestrator may notify the game manager when a player exits a game.
    - Provides high-level insights on the bot's activity.
    - Can be persistent, but not at the db level.
    It only monitors the current state of every game being played.
    - Logs these insights for monitoring purposes or specialized logging.
    """

    def __init__(self):
        # dict of games, key = chat_id, value = Game object
        self.games: dict[int, Game] = {}

    def new_game(self, chat_id: int):
        """initializes a new game in a chat"""

        # do not start another if there's already one going on
        if chat_id in self.games:
            raise GameAlreadyExistError()

        self.games[chat_id] = Game(chat_id)

    def end_game(self, chat_id: int):
        """ends a game in a chat"""

        if chat_id not in self.games:
            raise GameAlreadyExistError()

        del self.games[chat_id]
