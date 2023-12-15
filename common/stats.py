from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from common.models import get_user
from common.utils import mention, n_format
from config import ACHIEVEMENTS


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

        keyboard = create_achievement_matrix(a)
        await message.reply_text(stats_txt, reply_markup=InlineKeyboardMarkup(keyboard))
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
