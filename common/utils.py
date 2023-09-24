"""
Some utils shared amoung the app module
"""

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def send_reply_message(update: Update, message: str):
    if update.message:
        await update.message.reply_text(
            message, reply_to_message_id=update.message.message_id
        )


def mention(title, link):
    if link:
        return f"[{title}]({link})"
    else:
        return f"{title}"
