import logging

import card as c

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from global_variables import gm, updater
from utils import send_async, mention, win_game, lost_game

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Countdown(object):
    player = None
    job_queue = None

    def __init__(self, player, job_queue):
        self.player = player
        self.job_queue = job_queue


def do_play_card(bot, player, result_id):
    """Plays the selected card and sends an update to the group if needed"""

    card = c.from_str(result_id)
    player.play(card)
    game = player.game
    chat = game.chat
    user = player.user
    controller = repr(game.control_card)
    info = dict()

    # draw cards ui
    c_list = []
    number_of_cards = len(player.cards)
    for _ in range(number_of_cards):
        c_list.append("🎴")
    for _ in range(5-number_of_cards):
        c_list.append("🃏")
    choice = [[InlineKeyboardButton(
        text=f"".join(c_list), switch_inline_query_current_chat='')]]

    """ updater.job_queue.stop()
    updater.job_queue.run_once(end_by_afk, game.waiting_time) """

    if game.control_player is not None:
        if game.play_round % len(game.players) == 0 and game.play_round < (len(game.players) * 5):
            # update game_info
            info.update({'round': game.game_round, 'control_card': game.control_card,
                         'control_player': game.control_player})
            game.game_info.append(info)

            # reset control card and controller -> current user
            game.control_card = None
            game.current_player = game.control_player

        # 5 play_round = 1 game round
        if game.play_round != (len(game.players) * 5):
            send_async(
                bot, chat.id, text=f"👑 {mention(game.control_player.user)} - {controller}\n〰️\n🤙🏾 {mention(game.current_player.user)} à toi.", reply_markup=InlineKeyboardMarkup(choice))

            # add this information to the game info list
            game.game_round += 1

    if card in c.SPECIALS:
        gm.end_game(chat, user)
        if card == 'x_21':
            win_game(bot, game, chat, "21", user)
            lost_game(bot, game, chat, "21")
        if card == 'x_333':
            win_game(bot, game, chat, "333", user)
            lost_game(bot, game, chat, "333")
        if card == 'x_777':
            win_game(bot, game, chat, "777", user)
            lost_game(bot, game, chat, "777")
        if card == 'x_0':
            win_game(bot, game, chat, "fam", user)
            lost_game(bot, game, chat, "fam")

        return

    if game.play_round == (len(game.players) * 5):
        # KORA
        if check_kora(game):
            # DOUBLE KORA - if the 4th round was controlled with 3 by the same player
            if check_dbl_kora(game):
                gm.end_game(chat, user)
                win_game(bot, game, chat, "dbl_kora")
                lost_game(bot, game, chat, "dbl_kora")
            else:
                gm.end_game(chat, user)
                win_game(bot, game, chat, "kora")
                lost_game(bot, game, chat, "kora")

        # Normal win
        else:
            gm.end_game(chat, user)
            win_game(bot, game, chat, "n")  # n is the simple win
            lost_game(bot, game, chat, "n")  # n is the simple lose
        return


def check_kora(game):
    """ Check if game is being won by kora """
    return game.control_card.value == '3'


def check_dbl_kora(game):
    """ Check if game is being won by double kora """
    return game.game_info[3]['control_card'].value == '3' and game.game_info[3]['control_player'].user.id == game.control_player.user.id


def end_by_afk():
    print("end by afk")
