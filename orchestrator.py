import logging
from telegram import Update, User
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from common import interactions, jobs
from common.exceptions import GameAlreadyExistError, NotEnoughPlayersError

from config import GAME_START_TIMEOUT
from game import Game

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        self.games: dict[int, Game] = dict()

    def new_game(
        self,
        chat_id: int,
        title: str,
        game_creator: User,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        nkap: int = 0,
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
            title,
            game_creator,
            max_player_number,
            has_quick_wins,
            has_koras,
            has_dbl_koras,
            time_to_play,
            nkap,
        )

        if context.job_queue:
            passed_data = {
                "chat_id": chat_id,
                "game": self.games[chat_id],
                "update": update,
                "orchestrator": self,
            }
            # start warning timer
            context.job_queue.run_once(  # type: ignore
                interactions.WARN_GAME_START,
                int(GAME_START_TIMEOUT / 2),
                passed_data,
                name=str(chat_id),
            )
            # start game timer
            context.job_queue.run_once(  # type: ignore
                self.start_game_on_timeout,
                GAME_START_TIMEOUT,
                passed_data,
                name=str(chat_id),
            )

        logger.info("GAME_STARTED in chat %s", chat_id)
        return self.games[chat_id]

    def end_game(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
        """ends a game in a chat"""

        if chat_id not in self.games:
            raise GameAlreadyExistError()

        jobs.remove_job_if_exists(str(chat_id), context)
        logger.info("GAME_ENDED in chat %s", chat_id)
        del self.games[chat_id]

    async def start_game_on_timeout(self, context: ContextTypes.DEFAULT_TYPE):
        """starts the game when start time is elapsed"""
        job = context.job
        if job:
            chat_id = job.data["chat_id"]  # type: ignore
            game = context.job.data["game"]  # type: ignore
            update = context.job.data["update"]  # type: ignore
            orchestrator = context.job.data["orchestrator"]  # type: ignore

            try:
                game.start_game()
                await self.delete_game_messages(chat_id, context)
                jobs.remove_job_if_exists(str(chat_id), context)
                await interactions.FIRST_CARD(
                    update, context, chat_id, game, orchestrator
                )
            except NotEnoughPlayersError:
                await interactions.NOT_ENOUGH_PLAYERS(chat_id, context=context)
                await self.delete_game_messages(chat_id, context)
                self.end_game(chat_id, context)
                logger.info("CANNOT_START in chat %s", chat_id)

    async def end_game_from_afk(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        """ends a game from afk"""
        job = context.job

        if job:
            chat_id: int = job.data["chat_id"]  # type: ignore
            game: Game = job.data["game"]  # type: ignore
            orchestrator: Orchestrator = job.data["orchestrator"]  # type: ignore

            game.end_game("AFK")
            jobs.remove_job_if_exists(str(chat_id), context)
            await interactions.END_GAME(context, chat_id, game)
            orchestrator.end_game(chat_id, context)

    async def delete_game_messages(
        self, chat_id: int, context: ContextTypes.DEFAULT_TYPE
    ):
        """deletes all messages from a game"""
        if chat_id in self.games:
            game = self.games[chat_id]
            for message_id in game.messages_to_delete:
                try:
                    await context.bot.delete_message(chat_id, message_id)
                except TelegramError:
                    # bot might not be admin or the message is already deleted
                    logger.warning("CANNOT_DELETE in chat %s", chat_id)
