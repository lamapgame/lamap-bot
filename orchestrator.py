from telegram import User
from game import Game
from common.exceptions import GameAlreadyExistError


class Orchestrator:
    """
    ## The Grand O:

    - Manages all Telegram games.
    - Communicates globally with players:
        warnings, upcoming games, bans, money drops.
    - Central hub for game event communication.
    - Offers insights on bot activity.
    - Monitors current game states; not database-persistent.
    - Logs insights for monitoring and specialized logging.
    """

    def __init__(self):
        # dict of games, key = chat_id, value = Game object
        self.games: dict[int, Game] = {}

    def new_game(
        self,
        chat_id: int,
        game_creator: User,
        max_player_number: int = 4,
        has_quick_wins: bool = True,
        has_koras: bool = True,
        has_dbl_koras: bool = True,
        time_to_play: int = 60,
    ) -> Game:
        """initializes a new game in a chat"""

        # do not start another if there's already one going on
        if chat_id in self.games:
            raise GameAlreadyExistError()

        self.games[chat_id] = Game(
            chat_id,
            game_creator,
            max_player_number,
            has_quick_wins,
            has_koras,
            has_dbl_koras,
            time_to_play,
        )
        return self.games[chat_id]

    def end_game(self, chat_id: int):
        """ends a game in a chat"""

        if chat_id not in self.games:
            raise GameAlreadyExistError()

        del self.games[chat_id]
