from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from common.exceptions import GameAlreadyExistError

import common.interactions as interactions
from config import TOKEN
from common.utils import send_reply_message
from orchestrator import Orchestrator


# start the orchestrator at bot load
orchestrator = Orchestrator()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user:
        await send_reply_message(update, f"Hello {update.effective_user.first_name}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await interactions.INIT_USER(update)


async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await interactions.LEARN(update)


async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """asks the orchestrator to initialize a new game in the current chat"""
    if update.message:
        try:
            orchestrator.new_game(update.message.chat.id)
        except GameAlreadyExistError:
            await send_reply_message(
                update, "Une partie est déjà en cours dans ce groupe."
            )


try:
    if not TOKEN:
        raise Exception("No token provided")
    app = ApplicationBuilder().token(TOKEN).build()
except RuntimeError as excp:
    raise Exception("No token provided") from excp

# Bot command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("learn", learn))
app.add_handler(CommandHandler("hello", hello))

# Game handlers
app.add_handler(CommandHandler("play", start_game))

app.run_polling()
