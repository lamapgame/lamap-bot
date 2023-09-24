from functools import wraps
from typing import Callable

from telegram.ext import ContextTypes

from common.interactions import INIT_USER


class Validator:
    """
    To use:
    @Validator.check_user_is_not_bot

    """

    @classmethod
    def check_user_is_admin(cls, func: Callable):
        ...

    @classmethod
    def check_message_is_group(cls, func: Callable):
        @wraps(func)
        async def wrapper(update, context: ContextTypes.DEFAULT_TYPE):
            if update.message.chat.type != "private":
                return await func(update, context)
            else:
                await INIT_USER(update)

        return wrapper

    @classmethod
    def check_user_is_not_bot(cls, func: Callable):
        @wraps(func)
        async def wrapper(update, context: ContextTypes.DEFAULT_TYPE):
            if update.effective_user is not None and not update.effective_user.is_bot:
                return await func(update, context)

        return wrapper
