import logging

from telegram.ext.dispatcher import run_async
from global_variables import gm

from mwt import MWT

logger = logging.getLogger(__name__)

TIMEOUT = 2.5


def error(bot, update, error):
    """Simple error handler"""
    logger.exception(error)


@run_async
def send_async(bot, *args, **kwargs):
    """Send a message asynchronously"""
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT
    try:
        msg_sent = bot.sendMessage(*args, **kwargs)
        if 'to_delete' in kwargs:
            gm.start_gm_msgs.append(msg_sent.message_id)
    except Exception as e:
        error(None, None, e)
    return msg_sent


def send_msg(bot, *args, **kwargs):
    """ Send direct message """


@run_async
def send_animation_async(bot, *args, **kwargs):
    """Send an animation asynchronously"""
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT
    try:
        msg_sent = bot.send_animation(*args, **kwargs)
        if 'to_delete' in kwargs:
            gm.start_gm_msgs.append(msg_sent.message_id)
    except Exception as e:
        error(None, None, e)


@run_async
def delete_async(bot, *args, **kwargs):
    """ Delete message from group """
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT
    try:
        bot.delete_message(*args, **kwargs)
    except Exception as e:
        error(None, None, e)


def delete_start_msgs(bot, chat_id, **kwargs):
    """ Delete message from group """
    for msg in gm.start_gm_msgs:
        delete_async(bot, chat_id, message_id=msg)


@run_async
def answer_async(bot, *args, **kwargs):
    ''' Answer an inline query asynchronously '''
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT

    try:
        bot.answerInlineQuery(*args, **kwargs)
    except Exception as e:
        error(None, None, e)


def game_is_running(game):
    return game in gm.chatid_games.get(game.chat.id, list())


def user_is_creator(user, game):
    return user.id in game.owner


def user_is_admin(user, bot, chat):
    return user.id in get_admin_ids(bot, chat.id)


def user_is_creator_or_admin(user, game, bot, chat):
    return user_is_creator(user, game) or user_is_admin(user, bot, chat)


@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
