from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from common.models import get_user
from common.utils import mention, n_format


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows a user's stats"""
    user = update.effective_user
    chat = update.effective_chat
    message = update.message
    if not user or not message or not chat:
        return

    try:
        (_u, s, a) = get_user(user)

        stats_txt = (
            f"`{n_format(s.nkap):<4}`   {mention(user.first_name, f'tg://user?id={user.id}')}\n\n"
            f"`{s.games_played:<4}`   {'Jouées'}\n"
            f"`{s.wins:<4}`   {'Gagnées'}\n"
            f"`{s.losses:<4}`   {'Perdues'}\n"
            f"`{s.wins_kora:<4}`   {'Koras'}\n\n"
            f"`{s.points:<4}`   {'Points'}"
        )

        keyboard = [
            [
                InlineKeyboardButton("🖐🏽", callback_data="join_game"),
                InlineKeyboardButton("💰", callback_data="start_game"),
                InlineKeyboardButton("👑", callback_data="start_game"),
                InlineKeyboardButton("👑", callback_data="start_game"),
            ],
            [
                InlineKeyboardButton("🖐🏽", callback_data="join_game"),
                InlineKeyboardButton("💰", callback_data="start_game"),
                InlineKeyboardButton("👑", callback_data="start_game"),
                InlineKeyboardButton("👑", callback_data="start_game"),
            ],
            [
                InlineKeyboardButton("🖐🏽", callback_data="join_game"),
                InlineKeyboardButton("💰", callback_data="start_game"),
                InlineKeyboardButton("👑", callback_data="start_game"),
                InlineKeyboardButton("👑", callback_data="start_game"),
            ],
        ]

        await message.reply_text(stats_txt, reply_markup=InlineKeyboardMarkup(keyboard))
    except ValueError as e:
        print(e)
        await message.reply_text(
            "Je ne te know pas encore, fais /start j'ouvre ton registre"
        )
