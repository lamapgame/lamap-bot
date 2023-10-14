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
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode

from common.callback_handler import (
    handle_inline_query,
    handle_query,
    process_inline_query_result,
)
from common.exceptions import GameAlreadyExistError

import common.interactions as interactions
from common.utils import mention
from orchestrator import Orchestrator
from validator import Validator
from config import TOKEN


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)


# start the orchestrator at bot load
orchestrator = Orchestrator()


@Validator.check_message_is_group
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await interactions.INIT_USER(update)


async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await interactions.LEARN(update)


async def start_new_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """asks the orchestrator to initialize a new game in the current chat"""
    if (
        update.message
        and update.message.from_user
        and update.effective_chat
        and context.job_queue
    ):
        user = update.message.from_user
        try:
            game = orchestrator.new_game(update.message.chat.id, user, update, context)
            msg = await interactions.NEW_GAME(update, game)
            chat_id = update.message.chat.id
            await context.bot.pin_chat_message(
                chat_id,
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


async def process_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await process_inline_query_result(orchestrator, update, context)


async def reply_inline_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await handle_inline_query(orchestrator, update, context)


async def grab_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ...


# launch bot
try:
    if not TOKEN:
        raise Exception("No token provided")
    app = (
        ApplicationBuilder().defaults(Defaults(ParseMode.MARKDOWN)).token(TOKEN).build()
    )
except RuntimeError as excp:
    raise Exception("No token provided") from excp

# Bot command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("learn", learn))

# Game handlers
app.add_handler(CommandHandler("play", start_new_game))

# Callback query handler
app.add_handler(CallbackQueryHandler(callback_query))

# Inline results handling
app.add_handler(InlineQueryHandler(reply_inline_query))
app.add_handler(ChosenInlineResultHandler(process_result, block=False))

app.run_polling(allowed_updates=Update.ALL_TYPES)
