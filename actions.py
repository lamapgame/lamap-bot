import logging

import card as c

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


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

    next_bet = game.bet

    if next_bet == 0:
        next_bet = 500

    restart_keyboard = [
        [f"/nkap {next_bet}", f"/nkap {next_bet*2}", f"/nkap {next_bet*5}"], ["/new_game", "/call_me_back"]]
    restart_markup = ReplyKeyboardMarkup(
        restart_keyboard, one_time_keyboard=True, resize_keyboard=True)

    c_list = []
    no_cards = len(player.cards)

    for _ in range(no_cards):
        c_list.append("🎴")
    for _ in range(5-no_cards):
        c_list.append("🃏")

    choice = [[InlineKeyboardButton(
        text=f"".join(c_list), switch_inline_query_current_chat='')]]

    if card in c.SPECIALS:
        if card == 'x_21':
            send_animation_async(
                bot, chat.id, animation=win_qw_Anim(), caption=f"Fin du game! {mention(user)} gagne avec le Tia (21)!")
            stats.user_won(user.id, '21', game.nkap, game.bet)
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, '21', game.nkap, game.bet)

            logger.debug(
                f"WIN GAME *X21* ({game.control_player.user.id}) in {chat.id}")
        if card == 'x_333':
            send_animation_async(
                bot, chat.id, animation=win_qw_Anim(), caption=f"Fin du game! {mention(user)} gagne avec les trois 3!")
            stats.user_won(user.id, '333', game.nkap, game.bet)
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, '333', game.nkap, game.bet)

            logger.debug(
                f"WIN GAME *X333* ({user.id}) in {chat.id}")
        if card == 'x_777':
            send_animation_async(
                bot, chat.id, animation=win_qw_Anim(), caption=f"Fin du game! {mention(user)} gagne avec les trois 7!")
            stats.user_won(user.id, '777', game.nkap, game.bet)
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, '777', game.nkap, game.bet)

            logger.debug(
                f"WIN GAME *X777* ({user.id}) in {chat.id}")
        if card == 'x_0':
            send_animation_async(
                bot, chat.id, animation=win_qw_Anim(), caption=f"Qui a partagé les cartes ci? Fin du game! {mention(user)} gagne avec la famille!")
            stats.user_won(user.id, 'fam', game.nkap, game.bet)
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, 'fam', game.nkap, game.bet)

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
            send_async(
                bot, chat.id, text=f"👑 {mention(game.control_player.user)} - {controller}\n〰️\n🤙🏾 {mention(game.current_player.user)} à toi.", reply_markup=InlineKeyboardMarkup(choice))

            # add this information to the game info list
            game.game_round += 1

    if game.play_round == (len(game.players) * 5):
        # KORA
        if game.control_card.value == '3':
            # DOUBLE KORA - if the 4th round was controlled with 3 by the same player
            if game.game_info[3]['control_card'].value == '3' and game.game_info[3]['control_player'].user.id == game.control_player.user.id:
                if game.nkap:
                    send_animation_async(
                        bot, chat.id, animation=win_Anim(), caption=f"Eyeehh! {mention(game.control_player.user)} la facture des 33 là c'est {game.bet*4} Ň!")
                else:
                    send_animation_async(
                        bot, chat.id, animation="https://media.giphy.com/media/zrj0yPfw3kGTS/giphy.gif", caption=f"{mention(game.control_player.user)} ça fait comme si ils ont bu ta 33 que tu avais posé là!")
                stats.user_won(game.control_player.user.id,
                               'dbl_kora', game.nkap, game.bet)
                loosers = [
                    lost.user.id for lost in game.players if lost.user.id != game.control_player.user.id
                ]
                for looser in loosers:
                    stats.user_lost(looser, 'dbl_kora', game.nkap, game.bet)

                logger.debug(
                    f"WIN GAME *DOUBLE-KORA* ({game.control_player.user.id}) in {chat.id}")
            else:
                if game.nkap:
                    send_animation_async(
                        bot, chat.id, animation=win_Anim(), caption=f"KORA! {mention(game.control_player.user)} porte {game.bet*2} Ň!")
                else:
                    send_animation_async(
                        bot, chat.id, animation=win_kora_Anim(), caption=f"Fin de partie! c'est par KORA que {mention(game.control_player.user)} gagne!")
                stats.user_won(game.control_player.user.id,
                               'kora', game.nkap, game.bet)
                loosers = [
                    lost.user.id for lost in game.players if lost.user.id != game.control_player.user.id
                ]
                for looser in loosers:
                    stats.user_lost(looser, 'kora', game.nkap, game.bet)

                logger.debug(
                    f"WIN GAME *KORA* ({game.control_player.user.id}) in {chat.id}")

        # Normal win
        else:
            if game.nkap:
                send_animation_async(
                    bot, chat.id, animation=win_Anim(), caption=f"Voilà {mention(game.control_player.user)} qui part avec {game.bet} Ň!", reply_markup=restart_markup)
            else:
                send_animation_async(
                    bot, chat.id, animation=win_Anim(), caption=f"Fin de partie! {mention(game.control_player.user)} a gagné!", reply_markup=restart_markup)

            stats.user_won(game.control_player.user.id,
                           'n', game.nkap, game.bet)
            loosers = [
                lost.user.id for lost in game.players if lost.user.id != game.control_player.user.id
            ]
            for looser in loosers:
                stats.user_lost(looser, 'n', game.nkap, game.bet)

            logger.debug(
                f"WIN GAME ({game.control_player.user.id}) in {chat.id}")

        gm.end_game(chat, user)
        return


def save_info(user, card, play_round, game_round):
    """ Save the information for the current round """
