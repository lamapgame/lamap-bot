from pony.orm import db_session

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from common.exceptions import UserIsBanned

from common.models import (
    get_top_double_kora,
    get_top_kora,
    get_top_nkap,
    get_top_points,
    get_user,
)
from common.utils import mention, n_format
from config import ACHIEVEMENTS


@db_session
async def top_nkap(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the top 15 richest players"""
    message = update.message
    if not message:
        return

    try:
        top = get_top_nkap()
        top_txt = ""
        for i, gs in enumerate(top):
            top_txt += f"`{i+1:<2}` *{gs.user.name}*  `{n_format(gs.nkap)}`\n"
        await message.reply_text(top_txt)
    except ValueError:
        await message.reply_text("Une erreur est survenue")


@db_session
async def top_points(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the top 15 by points"""
    message = update.message
    if not message:
        return

    try:
        top = get_top_points()
        top_txt = ""
        for i, gs in enumerate(top):
            top_txt += f"`{i+1:<2}` *{gs.user.name}*  `{gs.points}`\n"
        await message.reply_text(top_txt)
    except ValueError:
        await message.reply_text("Une erreur est survenue")


@db_session
async def top_kora(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """shows the top 15 koras and double koras"""
    message = update.message
    if not message:
        return

    try:
        top_kora_stats = get_top_kora()
        top_dbl_kora = get_top_double_kora()
        top_txt = ""
        for i, gs in enumerate(top_kora_stats):
            top_txt += f"`{i+1:<2}` *{gs.user.name}*  `{gs.wins_kora}`\n"
        await message.reply_text("*TOP KORATEURS*\n\n" + top_txt)

        top_txt = ""
        for i, gs in enumerate(top_dbl_kora):
            top_txt += f"`{i+1:<2}` *{gs.user.name}*  `{gs.wins_dbl_kora}`\n"
        await message.reply_text("*TOP DOUBLE KORATEURS*\n\n" + top_txt)
    except ValueError:
        await message.reply_text("Une erreur est survenue")


async def show_stats(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows a user's stats"""
    if update.message and update.message.reply_to_message is not None:
        user = update.message.reply_to_message.from_user
    else:
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

        keyboard = create_achievement_matrix(a)
        await message.reply_text(stats_txt, reply_markup=InlineKeyboardMarkup(keyboard))
    except UserIsBanned:
        await message.reply_text(
            "Tu es ban du bot, gère avec les admins dans @lamapsupport"
        )
    except ValueError:
        await message.reply_text(
            "Je ne te know pas encore, tape /start j'ouvre ton registre"
        )


def create_achievement_matrix(achievements) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    row = []
    max_columns = 4
    for achievement in achievements:
        key = achievement.code
        timestamp = achievement.date_achieved.isoformat()

        # do not show if the user has hidden the achievement
        if not achievement.displayed:
            continue

        if key in ACHIEVEMENTS:
            button = InlineKeyboardButton(
                ACHIEVEMENTS[key]["emoji"],
                callback_data=f"{key}||{timestamp}",
            )
            row.append(button)

            if len(row) == max_columns:
                keyboard.append(row)
                row = []

    if row:
        keyboard.append(row)

    return keyboard
