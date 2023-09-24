from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
from telegram.constants import ParseMode

from common.callback_handler import handle_query
from common.exceptions import GameAlreadyExistError

import common.interactions as interactions
from common.utils import mention
from orchestrator import Orchestrator
from validator import Validator
from config import TOKEN


# start the orchestrator at bot load
orchestrator = Orchestrator()


@Validator.check_message_is_group
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await interactions.INIT_USER(update)


async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await interactions.LEARN(update)


async def start_new_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """asks the orchestrator to initialize a new game in the current chat"""
    if update.message and update.message.from_user and update.effective_chat:
        user = update.message.from_user
        try:
            game = orchestrator.new_game(
                update.message.chat.id, update.message.from_user
            )
            msg = await interactions.NEW_GAME(update, game)
            await context.bot.pin_chat_message(
                update.effective_chat.id,
                msg.message_id,
                True,
            )
            game.add_message_to_delete(msg.message_id)

        except GameAlreadyExistError:
            await context.bot.send_message(
                user.id,
                (
                    "Il y a déjà une partie en cours dans"
                    f" {mention(update.effective_chat.title, update.message.link)}"
                ),
                ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )


async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_query(orchestrator, update, context)


# launch bot
try:
    if not TOKEN:
        raise Exception("No token provided")
    app = ApplicationBuilder().token(TOKEN).build()
    print("Bot started in dev mode")  # todo: replace with logger
except RuntimeError as excp:
    raise Exception("No token provided") from excp

# Bot command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("learn", learn))

# Game handlers
app.add_handler(CommandHandler("play", start_new_game))

# Callback query handler
app.add_handler(CallbackQueryHandler(callback_query))

app.run_polling()
