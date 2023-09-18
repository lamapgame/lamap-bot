import logging
from telegram import Update
from telegram.ext import (CallbackContext)
from config import LOGGING_CHAT_ID

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Logger:

    def __init__(self, name):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)

    def info(self, message: str):
        self._logger.info(message)

    def error(self, message: str):
        self._logger.warning(message)

    def admin(self, message: str):
        """Logs the message to the logging chat"""
        context.bot.send_message(chat_id=LOGGING_CHAT_ID,
                             text=message, disable_web_page_preview=True)


