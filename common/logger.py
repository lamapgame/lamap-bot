import logging
from telegram.ext import CallbackContext
import config

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Logger(logging.Logger):
    def __init__(self, name: str, level: int = logging.NOTSET):
        super().__init__(name)

    def admin(self, message: str, context: CallbackContext) -> None:
        """Logs the message to the logging chat"""
        context.bot.send_message(
            chat_id=config.LOGGING_CHAT_ID, text=message, disable_web_page_preview=True
        )
