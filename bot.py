"""
Bot's entry point.
It declares the bot's handlers and starts the bot.
"""

import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ChosenInlineResultHandler,
    InlineQueryHandler,
    Defaults,
)
from telegram.constants import ParseMode

from common.callback_handler import (
    handle_inline_query,
    handle_query,
    process_inline_query_result,
)
from common.exceptions import GameAlreadyExistError
from common.database import db

import common.interactions as interactions
from common.stats import show_stats
from common.utils import mention
from common.models import add_user

from orchestrator import Orchestrator

from config import TOKEN, DATABASE_URL


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)


# start the orchestrator at bot load
orchestrator = Orchestrator()


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start command handler"""
    if update.message and update.message.from_user:
        user = update.message.from_user
        add_user(user)

    await interactions.INIT_USER(update)


async def learn(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """/learn command handler"""
    await interactions.LEARN(update)


async def start_new_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """asks the orchestrator to initialize a new game in the current chat"""

    nkap = 0
    if context.args and context.args[0]:
        nkap = int(context.args[0])

    if nkap < 0:
        await interactions.CANNOT_START_GAME(update, "neg")
        return

    if (
        update.message
        and update.message.from_user
        and update.effective_chat
        and context.job_queue
    ):
        user = update.message.from_user
        try:
            game = orchestrator.new_game(
                update.message.chat.id, user, update, context, nkap
            )
            msg = await interactions.NEW_GAME(update, game)
            chat_id = update.message.chat.id
            try:
                await context.bot.pin_chat_message(
                    chat_id,
                    msg.message_id,
                    True,
                )
            except Exception:
                # log: can not pin
                pass

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
    """collects a callback query"""
    await handle_query(orchestrator, update, context)


async def process_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """process the result from an inline query"""
    await process_inline_query_result(orchestrator, update, context)


async def reply_inline_query(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """process a reply to an inline query"""
    await handle_inline_query(orchestrator, update)


# launch bot
try:
    if not TOKEN:
        raise ValueError("No token provided")
    if not DATABASE_URL:
        raise ValueError("No database url provided")
    app = (
        ApplicationBuilder().defaults(Defaults(ParseMode.MARKDOWN)).token(TOKEN).build()
    )
    db.bind("postgres", DATABASE_URL)
    db.generate_mapping(create_tables=True)
except RuntimeError as excp:
    raise ValueError("An issue occured when launching the app") from excp

# Bot command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("learn", learn))

# Game handlers
app.add_handler(CommandHandler("play", start_new_game))

# Stats handlers
app.add_handler(CommandHandler("stats", show_stats))

# Callback query handler
app.add_handler(CallbackQueryHandler(callback_query))

# Inline results handling
app.add_handler(InlineQueryHandler(reply_inline_query))
app.add_handler(ChosenInlineResultHandler(process_result, block=False))

app.run_polling(allowed_updates=Update.ALL_TYPES)
