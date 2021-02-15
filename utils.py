import logging

from telegram import ParseMode
from telegram.error import BadRequest

import helpers
from stats import user_won, user_lost
from gifs import win_Anim, win_kora_Anim, win_qw_Anim

from global_variables import gm
from mwt import MWT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TIMEOUT = 2.5


def error(bot, update, error):
    """Simple error handler"""
    logger.exception(error)


def send_async(bot, *args, **kwargs):
    """Send a message asynchronously"""
    remove = False
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT
    if 'to_delete' in kwargs:
        remove = True
        del kwargs['to_delete']
    try:
        msg_sent = bot.send_message(
            *args, **kwargs, disable_web_page_preview=True)
        if remove:
            gm.start_gm_msgs[args[0]].append(msg_sent.message_id)
    except Exception as e:
        error(None, None, e)


def send_animation_async(bot, *args, **kwargs):
    """Send an animation asynchronously"""
    remove = False
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT
    if 'to_delete' in kwargs:
        remove = True
        del kwargs['to_delete']
    try:
        msg_sent = bot.send_animation(
            *args, **kwargs, parse_mode=ParseMode.MARKDOWN)

        if remove:
            gm.start_gm_msgs[args[0]].append(msg_sent.message_id)

    except Exception as e:
        error(None, None, e)


def delete_async(bot, *args, **kwargs):
    """ Delete message from group """
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT
    try:
        bot.delete_message(*args, **kwargs)
    except Exception as e:
        pass


def delete_start_msgs(bot, chat_id, **kwargs):
    """ Delete message from group """
    for msg in gm.start_gm_msgs[chat_id]:
        delete_async(bot, chat_id, message_id=msg)


def answer_async(bot, *args, **kwargs):
    ''' Answer an inline query asynchronously '''
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT

    try:
        bot.answerInlineQuery(*args, **kwargs)
    except Exception as e:
        error(None, None, e)


def pin_game_message(bot, *args):
    game_start_msg_id = gm.start_gm_msgs[args[0]]
    bot.pin_chat_message(args[0], game_start_msg_id[0])


def game_is_running(game):
    return game in gm.chatid_games.get(game.chat.id, list())


def user_is_creator(user, game):
    return user.id in game.owner


def user_is_admin(user, bot, chat):
    return user.id in get_admin_ids(bot, chat.id)


def user_is_creator_or_admin(user, game, bot, chat):
    return user_is_creator(user, game) or user_is_admin(user, bot, chat)


def mention(user):
    return f'[{user.first_name}](tg://user?id={user.id})'


def n_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', ' kolos', ' bâtons', ' myondos', ' mitoumba'][magnitude])


def win_game(bot, game, chat, style, w_extension=None):
    winner = game.control_player.user

    if w_extension is not None:
        winner = w_extension

    if style == "n":
        send_animation_async(
            bot, chat.id, animation=win_Anim(), caption=f"Voilà {mention(winner)} qui part avec {n_format(game.bet * (len(game.players)-1))} !"
        )
        pts_won = user_won(winner.id, style, game.nkap,
                           game.bet*(len(game.players)-1))
        helpers.dm_information(chat, winner.id, bot, "W", pts_won,
                               game.bet, game.bet*(len(game.players)-1))

    if style == "kora":
        send_animation_async(
            bot, chat.id, animation=win_kora_Anim(), caption=f"KORA! {mention(winner)} porte {n_format((game.bet * (len(game.players)-1))*2)} !")
        pts_won = user_won(winner.id,
                           style, game.nkap, game.bet * (len(game.players)-1))
        helpers.dm_information(chat, winner.id, bot, "W",
                               pts_won, game.bet, game.bet * (len(game.players)-1)*2)

    if style == "dbl_kora":
        send_animation_async(
            bot, chat.id, animation=win_Anim(), caption=f"Garçon ! {mention(winner)} à laissé la consigne que la facture des 33 là c'est {n_format((game.bet * (len(game.players)-1))*4)} !")
        pts_won = user_won(winner.id,
                           style, game.nkap, game.bet * (len(game.players)-1))
        helpers.dm_information(chat, winner.id, bot, "W",
                               pts_won, game.bet, game.bet * (len(game.players)-1)*4)

    if (style == "fam" or style == "ax" or style == "777" or style == "333" or style == "21"):
        send_animation_async(
            bot, chat.id, animation=win_qw_Anim(), caption=f"Fin du game ! {mention(w_extension)} gagne {n_format(game.bet * (len(game.players)-1))}  !")
        pts_won = user_won(w_extension.id, style, game.nkap,
                           game.bet*(len(game.players)-1))
        helpers.dm_information(chat, w_extension.id, bot, "W",
                               pts_won, game.bet, game.bet*(len(game.players)-1))

    logger.info(
        f"WIN GAME in {style} ({winner.id}) in {chat.id}")


def lost_game(bot, game, chat, style, w_extension=None):

    loosers = [
        lost.user.id for lost in game.players if lost.user.id != game.control_player.user.id
    ]

    if w_extension:
        loosers = [
            lost.user.id for lost in game.players if lost.user.id != w_extension.id
        ]

    for looser in loosers:
        if style == "n":
            pts_loss = user_lost(looser, style, game.nkap, game.bet)
            helpers.dm_information(
                chat, looser, bot, "L", pts_loss, game.bet, game.bet)

        if style == "kora":
            pts_loss = user_lost(
                looser, style, game.nkap, game.bet)
            helpers.dm_information(chat, looser, bot, "L",
                                   pts_loss, game.bet, game.bet*2)

        if style == "dbl_kora":
            pts_loss = user_lost(
                looser, style, game.nkap, game.bet)
            helpers.dm_information(
                chat, looser, bot, "L", pts_loss, game.bet, game.bet*4)

        if (style == "fam" or style == "ax" or style == "777" or style == "333" or style == "21"):
            pts_loss = user_lost(looser, style, game.nkap, game.bet)
            helpers.dm_information(
                chat, looser, bot, "L", pts_loss, game.bet, game.bet)

        logger.info(
            f"LOSER(S) {style} ({looser}) in {chat.id}")


@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
