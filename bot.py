"""
Bot's entry point.
It declares the bot's handlers and starts the bot.
"""

import logging

from telegram import Update, User
from telegram.error import TelegramError
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
from common.exceptions import (
    CannotTransferToBannedError,
    CannotTransferToBotError,
    CannotTransferToSelfError,
    CannotTransferToUnknownPlayerError,
    GameAlreadyExistError,
    NotEnoughNkapError,
)
from common.database import db

import common.interactions as interactions
from common.stats import show_stats
from common.utils import mention
from common.models import (
    add_user,
    compute_ban_unban,
    compute_ret_rem,
    compute_transfer_nkap,
)

from orchestrator import Orchestrator

from config import BOT_ID, SUPER_ADMIN_LIST, TOKEN, DATABASE_URL


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


async def kill_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """kills the game in the current chat"""

    is_admin = False
    is_super_admin = False
    user = update.effective_user

    if update.effective_chat and user:
        chat_id = update.effective_chat.id

        if chat_id in orchestrator.games:
            chat_admins = await update.effective_chat.get_administrators()
            if user in (admin.user for admin in chat_admins):
                is_admin = True
            if str(user.id) in SUPER_ADMIN_LIST:
                is_super_admin = True

            game = orchestrator.games[chat_id]
            if is_admin or is_super_admin:
                await orchestrator.delete_game_messages(chat_id, context)
                game.end_game("KILL")
                game.killer = user
                await interactions.END_GAME(context, chat_id, game)
                orchestrator.end_game(chat_id, context)
            else:
                await interactions.NOT_ADMIN(update)
        else:
            await interactions.CANNOT_KILL_GAME(update)


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
            except TelegramError:
                # the bot lacks rights to pin in group
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


async def transfer_nkap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """transfer nkap to another user /transfer <nkap>"""
    if not update.message or not update.message.from_user:
        return

    reciever = None
    sender = update.message.from_user
    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user

        if context.args and context.args[0]:
            amount = int(context.args[0].replace(" ", ""))
            if amount < 0:
                await interactions.CANNOT_TRANSFER_NKAP(update, "neg")
                return
            try:
                if reciever.id == BOT_ID:
                    raise CannotTransferToBotError()

                compute_transfer_nkap(sender.id, reciever.id, amount)
                await interactions.TRANSFER_NKAP(
                    update, amount, sender.first_name, reciever.first_name
                )
            except CannotTransferToBannedError:
                await interactions.CANNOT_TRANSFER_NKAP(update, "banned")
            except CannotTransferToBotError:
                await interactions.CANNOT_TRANSFER_NKAP(update, "bot")
            except CannotTransferToSelfError:
                await interactions.CANNOT_TRANSFER_NKAP(update, "self")
            except NotEnoughNkapError:
                await interactions.CANNOT_TRANSFER_NKAP(update, "not_enough")
            except CannotTransferToUnknownPlayerError:
                await interactions.CANNOT_TRANSFER_NKAP(update, "unknown")
        else:
            await interactions.CANNOT_TRANSFER_NKAP(update, "no_nkap_specified")
    else:
        await interactions.CANNOT_TRANSFER_NKAP(update, "no_reply")


# ADMIN COMMANDS
async def rem_nkap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """transfer nkap to another user /rem <nkap> or /rem <nkap> <user_id>"""
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    reciever_id = None
    amount = 0
    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever_id = update.message.reply_to_message.from_user.id
    elif context.args and context.args[1]:
        reciever_id = int(context.args[1].replace(" ", ""))

    if context.args and context.args[0]:
        amount = int(context.args[0].replace(" ", ""))

    else:
        await interactions.CANNOT_TRANSFER_NKAP(update, "admin")
        return

    try:
        compute_ret_rem(reciever_id, amount, False)
        await interactions.DID_REM(update, amount)
    except Exception:
        await interactions.CANNOT_DO_THIS(update)


async def ret_nkap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """credit a user account /rem <nkap> or /rem <nkap> <user_id> - ONLY SUPER ADMIN"""
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    reciever_id = None
    amount = 0
    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever_id = update.message.reply_to_message.from_user.id
    elif context.args and context.args[1]:
        reciever_id = int(context.args[1].replace(" ", ""))

    if context.args and context.args[0]:
        amount = int(context.args[0].replace(" ", ""))
    else:
        await interactions.CANNOT_TRANSFER_NKAP(update, "admin")
        return

    try:
        compute_ret_rem(reciever_id, amount, True)
        await interactions.DID_RET(update, amount)
    except Exception:
        await interactions.CANNOT_DO_THIS(update)


async def block_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ban a user account /senta <user_id> or reply - ONLY SUPER ADMIN"""
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    reciever: User | int = 0

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user
    if context.args and context.args[0]:
        reciever = int(context.args[0].replace(" ", ""))

    try:
        compute_ban_unban(reciever, True)
        await interactions.BLOCK_USER(update, reciever)
    except Exception:
        await interactions.CANNOT_DO_THIS(update)


async def unblock_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """unban a user account /senta <user_id> or reply - ONLY SUPER ADMIN"""
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    reciever: User | int = 0

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user

    if context.args and context.args[0]:
        reciever = int(context.args[0].replace(" ", ""))

    try:
        compute_ban_unban(reciever, False)
        await interactions.UNBLOCK_USER(update, reciever)
    except Exception:
        await interactions.CANNOT_DO_THIS(update)


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
app.add_handler(CommandHandler("tuer", kill_game))

# Stats handlers
app.add_handler(CommandHandler("transfert", transfer_nkap))
app.add_handler(CommandHandler("stats", show_stats))

# Admin handlers
app.add_handler(CommandHandler("rem", rem_nkap))
app.add_handler(CommandHandler("ret", ret_nkap))
app.add_handler(CommandHandler("senta", block_user))
app.add_handler(CommandHandler("unsenta", unblock_user))
# FORCE commands - only for super admins - TO USE WITH EXTRA CAUTION
# todo: add handlers for these
app.add_handler(CommandHandler("FORCE_nkap_reset", transfer_nkap))
app.add_handler(CommandHandler("FORCE_stats_reset", transfer_nkap))

# Callback query handler
app.add_handler(CallbackQueryHandler(callback_query))

# Inline results handling
app.add_handler(InlineQueryHandler(reply_inline_query))
app.add_handler(ChosenInlineResultHandler(process_result, block=False))

app.run_polling(allowed_updates=Update.ALL_TYPES)
