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

import common.jobs as jobs
from common.callback_handler import (
    handle_inline_query,
    handle_query,
    process_inline_query_result,
)
from common.exceptions import (
    CannotRemoveControllerError,
    CannotTransferToBannedError,
    CannotTransferToBotError,
    CannotTransferToSelfError,
    CannotTransferToUnknownPlayerError,
    GameAlreadyExistError,
    NotEnoughNkapError,
    PlayerNotInGameError,
    PlayerRemovedBeforeGameStart,
)
from common.database import db

import common.interactions as interactions
from common.stats import show_stats, top_kora, top_nkap, top_points
from common.utils import log_admin, mention, n_format
from common.models import (
    add_achievement,
    add_user,
    compute_ban_unban,
    compute_ret_rem,
    compute_transfer_nkap,
    remove_achievement,
)

from orchestrator import Orchestrator

from config import (
    ACHIEVEMENTS,
    BOT_ID,
    SUPER_ADMIN_LIST,
    THREAD_IDS,
    TOKEN,
    DATABASE_URL,
)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)


logger.info("Starting orchestrator")
orchestrator = Orchestrator()

# ruff: noqa: E501 # pylint: disable=line-too-long disable=anomalous-backslash-in-string


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start command handler"""
    if update.message and update.message.from_user:
        user = update.message.from_user
        add_user(user)

    await interactions.INIT_USER(update)


async def kill_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """kills the game in the current chat"""
    if update.message and update.message.chat.type == "private":
        await interactions.PRIVATE_CHAT(update)
        return

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


async def force_kick_player(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """kills the game in the current chat"""
    if update.message and update.message.chat.type == "private":
        await interactions.PRIVATE_CHAT(update)
        return

    is_admin = False
    is_super_admin = False
    user = update.effective_user
    if update.effective_chat and user:
        chat_admins = await update.effective_chat.get_administrators()
        if user in (admin.user for admin in chat_admins):
            is_admin = True
        if str(user.id) in SUPER_ADMIN_LIST:
            is_super_admin = True

    if is_admin or is_super_admin:
        if (
            not update.message
            or not update.message.reply_to_message
            or not update.message.reply_to_message.from_user
        ):
            await interactions.CANNOT_DO_THIS(update)
            return
        context.bot_data[
            "user_to_kick_id"
        ] = update.message.reply_to_message.from_user.id
        await quit_game(update, context)


async def quit_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/fuir command handler"""
    if update.message and update.message.chat.type == "private":
        await interactions.PRIVATE_CHAT(update)
        return

    user = update.effective_user

    # incase the command was called by force_kick_player
    if context.bot_data.get("user_to_kick_id"):
        user = context.bot_data["user_to_kick_id"]

    if update.effective_chat and user:
        chat_id = update.effective_chat.id
        if chat_id in orchestrator.games:
            game = orchestrator.games[chat_id]

            if len(game.players) > 2 and game.started:
                await interactions.CANNOT_QUIT_GAME(update, "experimental")
                return

            try:
                game.kick_player(user.id)
                msg = await interactions.QUIT_GAME(update, user)
                if game.started:
                    await interactions.NEXT_PLAYER(update, game)
                else:
                    jobs.remove_job_if_exists(str(chat_id), context)
                    await interactions.END_GAME(context, chat_id, game)
                    orchestrator.end_game(chat_id, context)
            except PlayerRemovedBeforeGameStart:
                msg = await interactions.QUIT_GAME(update, user)
                if msg:
                    game.add_message_to_delete(msg.message_id)
            except PlayerNotInGameError:
                msg = await interactions.CANNOT_QUIT_GAME(update, "not_in_game")
                if msg:
                    game.add_message_to_delete(msg.message_id)
            except CannotRemoveControllerError:
                msg = await interactions.CANNOT_QUIT_GAME(update, "controller")
                if msg:
                    game.add_message_to_delete(msg.message_id)

        else:
            await interactions.CANNOT_QUIT_GAME(update, "no_game")
            return


async def learn(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """/learn command handler"""
    await interactions.LEARN(update)


async def start_new_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """asks the orchestrator to initialize a new game in the current chat"""
    if update.message and update.message.chat.type == "private":
        await interactions.PRIVATE_CHAT(update)
        return

    nkap = 0
    if context.args and len(context.args) > 0:
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
                update.message.chat.id,
                update.effective_chat.title or "Groupe non nommé",
                user,
                update,
                context,
                nkap,
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
            logger.warning("GAME_ALREADY_EXIST in %i", update.message.chat.id)


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
    chat = update.effective_chat

    if not chat:
        return

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user

        if context.args and len(context.args) > 0:
            amount = int(context.args[0].replace(" ", ""))
            if amount < 0:
                await interactions.CANNOT_TRANSFER_NKAP(update, "neg")
                return
            try:
                if reciever.id == BOT_ID:
                    raise CannotTransferToBotError()
                if sender.id == reciever.id:
                    raise CannotTransferToSelfError()

                compute_transfer_nkap(sender.id, reciever.id, amount)

                await log_admin(
                    f"💸 \#TRANSFERT de **{amount}**:\n\n"
                    f"↗️ {mention(sender.first_name, f'tg://user?id={sender.id}', True)}"
                    f"  `{sender.id}`\n"
                    f"↘️ {mention(reciever.first_name, f'tg://user?id={reciever.id}', True)}"
                    f"  `{reciever.id}`\n\n"
                    f"➡️ {mention(chat.title, update.message.link, True)}",
                    context,
                    THREAD_IDS["TRANSFERT"],
                )

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
    chat = update.effective_chat

    if not chat:
        return

    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    reciever_id = None
    reciever = None
    amount = 0
    has_id_arg = False

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user
        reciever_id = reciever.id

    if context.args and len(context.args) > 1:
        has_id_arg = True
        reciever_id = int(context.args[1].replace(" ", ""))

    if context.args and len(context.args) > 0:
        amount = int(context.args[0].replace(" ", ""))

    else:
        await interactions.CANNOT_TRANSFER_NKAP(update, "admin")
        return

    try:
        compute_ret_rem(reciever_id, amount, False)
        await interactions.DID_REM(update, amount)

        logger.info(
            "REMBOURSEMENT of %i to player %i by admin %i in chat %i",
            amount,
            reciever_id,
            user.id,
            chat.id,
        )
        if reciever and not has_id_arg:
            await log_admin(
                f"🪙 \#REMBOURSEMENT de **{amount}**"
                f" à {mention(reciever.first_name, f'tg://user?id={reciever.id}', True)}"
                f"  \(`{reciever.id}`\) "
                f"dans {mention(chat.title, update.message.link, True)}",
                context,
                THREAD_IDS["RETREM"],
            )
        else:
            await log_admin(
                f"🪙 \#REMBOURSEMENT de **{amount}**\n à `{reciever_id}` "
                f"dans {mention(chat.title, update.message.link, True)}",
                context,
                THREAD_IDS["RETREM"],
            )

    except Exception as e:
        await interactions.CANNOT_DO_THIS(update)
        logger.warning(
            "ATTEMPT_REMBOURSEMENT of %i by %i in %i players",
            reciever_id,
            chat.id,
            user.id,
            exc_info=e,
        )


async def ret_nkap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """credit a user account /rem <nkap> or /rem <nkap> <user_id> - ONLY SUPER ADMIN"""
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    chat = update.effective_chat

    if not chat:
        return

    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    reciever_id = None
    reciever = None
    has_id_arg = False
    amount = 0

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user
        reciever_id = reciever.id

    if context.args and len(context.args) > 1:
        has_id_arg = True
        reciever_id = int(context.args[1].replace(" ", ""))

    if context.args and len(context.args) > 0:
        amount = int(context.args[0].replace(" ", ""))
    else:
        await interactions.CANNOT_TRANSFER_NKAP(update, "admin")
        return

    try:
        compute_ret_rem(reciever_id, amount, True)
        await interactions.DID_RET(update, amount)

        logger.info(
            "RETOUR of %i to player %i by admin %i in chat %i",
            amount,
            reciever_id,
            user.id,
            chat.id,
        )
        logger.info(
            "RETOUR of %i to player %i by admin %i in chat %i",
            amount,
            reciever_id,
            user.id,
            chat.id,
        )

        if reciever and not has_id_arg:
            await log_admin(
                f"🪙 \#RETOUR de **{amount}**"
                f" à {mention(reciever.first_name, f'tg://user?id={reciever.id}', True)}"
                f"  \(`{reciever.id}`\) "
                f"dans {mention(chat.title, update.message.link, True)}",
                context,
                THREAD_IDS["RETREM"],
            )
        else:
            await log_admin(
                f"🪙 \#RETOUR de **{amount}**\n à `{reciever_id}` "
                f"dans {mention(chat.title, update.message.link, True)}",
                context,
                THREAD_IDS["RETREM"],
            )
    except Exception as e:
        await interactions.CANNOT_DO_THIS(update)
        logger.warning(
            "ATTEMPT_RETOUR of %i by %i in %i players",
            reciever_id,
            chat.id,
            user.id,
            exc_info=e,
        )


async def block_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ban a user account /senta <user_id> or reply - ONLY SUPER ADMIN"""
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    chat = update.effective_chat

    if not chat:
        return

    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    reciever: User | int = 0

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user
    if context.args and len(context.args) > 0:
        reciever = int(context.args[0].replace(" ", ""))

    try:
        compute_ban_unban(reciever, True)
        await interactions.BLOCK_USER(update, reciever)

        if not isinstance(reciever, int):
            logger.info(
                "BLOCK of %i by admin %i in chat %i",
                reciever.id,
                user.id,
                chat.id,
            )
            await log_admin(
                f"🔨 \#BLOCK de à {mention(reciever.first_name, f'tg://user?id={reciever.id}', True)}"
                f"  \(`{reciever.id}`\) "
                f"dans {mention(chat.title, update.message.link, True)}",
                context,
                THREAD_IDS["BLOCKS"],
            )
        else:
            logger.info(
                "BLOCK of %i by admin %i in chat %i",
                reciever,
                user.id,
                chat.id,
            )
            await log_admin(
                f"🔨 \#BLOCK de `{reciever}` "
                f"dans {mention(chat.title, update.message.link, True)}",
                context,
                THREAD_IDS["BLOCKS"],
            )

    except Exception as e:
        await interactions.CANNOT_DO_THIS(update)
        logger.warning(
            "ATTEMPT_BLOCK of %i by %i in chat %i",
            reciever,
            chat.id,
            user.id,
            exc_info=e,
        )


async def unblock_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """unban a user account /senta <user_id> or reply - ONLY SUPER ADMIN"""
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    chat = update.effective_chat

    if not chat:
        return

    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    reciever: User | int = 0

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user

    if context.args and len(context.args) > 0:
        reciever = int(context.args[0].replace(" ", ""))

    try:
        compute_ban_unban(reciever, False)
        await interactions.UNBLOCK_USER(update, reciever)

        if not isinstance(reciever, int):
            logger.info(
                "UNBLOCK of %i by admin %i in chat %i",
                reciever.id,
                user.id,
                chat.id,
            )
            await log_admin(
                f"🔨 \#UNBLOCK de à {mention(reciever.first_name, f'tg://user?id={reciever.id}', True)}"
                f"  \(`{reciever.id}`\)\n"
                f"dans {mention(chat.title, update.message.link, True)}",
                context,
                THREAD_IDS["BLOCKS"],
            )
        else:
            logger.info(
                "UNBLOCK of %i by admin %i in chat %i",
                reciever,
                user.id,
                chat.id,
            )
            await log_admin(
                f"🔨 \#UNBLOCK de `{reciever}` "
                f"dans {mention(chat.title, update.message.link, True)}",
                context,
                THREAD_IDS["BLOCKS"],
            )

    except Exception as e:
        await interactions.CANNOT_DO_THIS(update)
        logger.warning(
            "ATTEMPT_UNBLOCK of %i by %i in chat %i",
            reciever,
            chat.id,
            user.id,
            exc_info=e,
        )


async def force_achievement(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user
        if context.args and len(context.args) > 0:
            achievement = str(context.args[0].replace(" ", ""))
            # check if this code is a valid achievement
            if achievement in ACHIEVEMENTS:
                add_achievement(reciever.id, achievement)
                await update.message.reply_text(
                    f"C'est bon, c'est fait, il a reçu `{achievement}`"
                )
            else:
                await update.message.reply_text("Je ne connais pas le badge là")
        else:
            await interactions.CANNOT_DO_THIS(update)
            return
    else:
        await interactions.CANNOT_DO_THIS(update)
        return


async def force_achievement_rem(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        reciever = update.message.reply_to_message.from_user
        if context.args and len(context.args) > 0:
            achievement = str(context.args[0].replace(" ", ""))
            # check if this code is a valid achievement
            if achievement in ACHIEVEMENTS:
                remove_achievement(reciever.id, achievement)
                await update.message.reply_text(f"On lui a enlevé `{achievement}`")
            else:
                await update.message.reply_text("Je ne connais pas le badge là")
        else:
            await interactions.CANNOT_DO_THIS(update)
            return
    else:
        await interactions.CANNOT_DO_THIS(update)
        return


async def refresh_nkap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    if str(user.id) not in SUPER_ADMIN_LIST:
        await interactions.YOU_ARE_NOT_SUPER_ADMIN(update)
        return

    if not context.args or len(context.args) == 0:
        await interactions.CANNOT_DO_THIS(update)
        return

    try:
        user = update.message.from_user
        amount = int(context.args[0].replace(" ", ""))
        db.execute(
            """UPDATE userdb
                    SET nkap=$amount
                    WHERE verified=true
                    """,
            {"amount": amount},
        )
        await update.message.reply_text(
            f"C'est bon, on a refresh tout le monde à {n_format(amount)}"
        )
        logger.info("REFRESH from %i OF %i", user.id, amount)
        await log_admin(
            f"🔨 \#REFRESH de à {mention(user.first_name, f'tg://user?id={user.id}', True)}"
            f"  \(`{user.id}`\)\n"
            f"a {n_format(amount)}",
            context,
            THREAD_IDS["BLOCKS"],
        )
    except (ValueError, IndexError):
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
    logger.critical("An issue occured when launching the app", exc_info=excp)
    raise ValueError("An issue occured when launching the app") from excp

# Bot command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("learn", learn))

# Game handlers
app.add_handler(CommandHandler("play", start_new_game))
app.add_handler(CommandHandler("tuer", kill_game))
app.add_handler(CommandHandler("fuir", quit_game))
app.add_handler(CommandHandler("kick", force_kick_player))

# Stats handlers
app.add_handler(CommandHandler("transfert", transfer_nkap))
app.add_handler(CommandHandler("stats", show_stats))
app.add_handler(CommandHandler("top_nkap", top_nkap))
app.add_handler(CommandHandler("top_points", top_points))
app.add_handler(CommandHandler("top_kora", top_kora))

# Admin handlers
app.add_handler(CommandHandler("rem", rem_nkap))
app.add_handler(CommandHandler("ret", ret_nkap))
app.add_handler(CommandHandler("block", block_user))
app.add_handler(CommandHandler("unblock", unblock_user))
app.add_handler(CommandHandler("refresh", refresh_nkap))

# FORCE commands - only for super admins - TO USE WITH EXTRA CAUTION
# todo: add handlers for these
app.add_handler(CommandHandler("FORCE_achievement", force_achievement))
app.add_handler(CommandHandler("FORCE_REMOVE_achievement", force_achievement_rem))
app.add_handler(CommandHandler("FORCE_nkap_reset", transfer_nkap))

# Callback query handler
app.add_handler(CallbackQueryHandler(callback_query))

# Inline results handling
app.add_handler(InlineQueryHandler(reply_inline_query))
app.add_handler(ChosenInlineResultHandler(process_result, block=False))

app.run_polling(allowed_updates=Update.ALL_TYPES)
