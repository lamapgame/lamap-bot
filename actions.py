import logging

import card as c

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


from global_variables import gm
from utils import send_async, send_animation_async, mention
from gifs import win_Anim, win_kora_Anim, win_qw_Anim

import stats

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
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

    choice = [[InlineKeyboardButton(
        text=f"Afficher mes cartes", switch_inline_query_current_chat='')]]

    if card in c.SPECIALS:
        if card == 'x_21':
            send_animation_async(
                bot, chat.id, animation=win_qw_Anim(), caption=f"Fin du game! {mention(user)} gagne avec le Tia (21)!")
            stats.user_won(user.id, '21')
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, '21')

            logger.debug(
                f"WIN GAME *X21* ({game.control_player.user.id}) in {chat.id}")
        if card == 'x_333':
            send_animation_async(
                bot, chat.id, animation=win_qw_Anim(), caption=f"Fin du game! {mention(user)} gagne avec les trois 3!")
            stats.user_won(user.id, '333')
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, '333')

            logger.debug(
                f"WIN GAME *X333* ({user.id}) in {chat.id}")
        if card == 'x_777':
            send_animation_async(
                bot, chat.id, animation=win_qw_Anim(), caption=f"Fin du game! {mention(user)} gagne avec les trois 7!")
            stats.user_won(user.id, '777')
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, '777')

            logger.debug(
                f"WIN GAME *X777* ({user.id}) in {chat.id}")
        if card == 'x_0':
            send_animation_async(
                bot, chat.id, animation=win_qw_Anim(), caption=f"Qui a partagé les cartes ci? Fin du game! {mention(user)} gagne avec la famille!")
            stats.user_won(user.id, 'fam')
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, 'fam')

            logger.debug(
                f"WIN GAME *FAM* ({user.id}) in {chat.id}")

        gm.end_game(chat, user)
        return

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
            send_async(bot, chat.id, text=f"○ {mention(game.control_player.user)} contrôle ({controller})\n● {mention(game.current_player.user)} à toi de jouer.",
                       reply_markup=InlineKeyboardMarkup(choice))

            # add this information to the game info list
            game.game_round += 1

    if game.play_round == (len(game.players) * 5):
        # KORA
        if game.control_card.value == '3':
            # DOUBLE KORA - if the 4th round was controlled with 3 by the same player
            if game.game_info[3]['control_card'].value == '3' and game.game_info[3]['control_player'].user.id == game.control_player.user.id:
                send_animation_async(
                    bot, chat.id, animation="https://media.giphy.com/media/zrj0yPfw3kGTS/giphy.gif", caption=f"{mention(game.control_player.user)} ça fait comme si ils ont bu ta 33 que tu avais posé là!")
                stats.user_won(user.id, 'dbl_kora')
                loosers = [
                    lost.user.id for lost in game.players if lost.user.id != user.id
                ]
                for looser in loosers:
                    stats.user_lost(looser, 'dbl_kora')

                logger.debug(
                    f"WIN GAME *DOUBLE-KORA* ({game.control_player.user.id}) in {chat.id}")
            else:
                send_animation_async(
                    bot, chat.id, animation=win_kora_Anim(), caption=f"Fin de partie! c'est par KORA que {mention(game.control_player.user)} gagne!")
                stats.user_won(user.id, 'kora')
                loosers = [
                    lost.user.id for lost in game.players if lost.user.id != user.id
                ]
                for looser in loosers:
                    stats.user_lost(looser, 'kora')

                logger.debug(
                    f"WIN GAME *KORA* ({game.control_player.user.id}) in {chat.id}")

        # Normal win
        else:
            send_animation_async(
                bot, chat.id, animation=win_Anim(), caption=f"Fin de partie! {mention(game.control_player.user)} a gagné!")
            stats.user_won(user.id, 'n')
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, 'n')

            logger.debug(
                f"WIN GAME ({game.control_player.user.id}) in {chat.id}")

        gm.end_game(chat, user)
        return


def save_info(user, card, play_round, game_round):
    """ Save the information for the current round """
