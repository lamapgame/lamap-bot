from telegram import Update
from telegram.ext import (CallbackContext)
from config import LOGGING_CHAT_ID


def log_to_admin(update: Update, context: CallbackContext, message: str):
    """Logs the message to the logging chat"""
    context.bot.send_message(chat_id=LOGGING_CHAT_ID,
                             text=message, disable_web_page_preview=True)
