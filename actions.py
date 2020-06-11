import random

import logging

import card as c
from datetime import datetime

from telegram import Message, Chat, InlineKeyboardButton, InlineKeyboardMarkup

from config import WAITING_TIME
from errors import DeckEmptyError, NotEnoughPlayersError
from global_variables import gm
from utils import send_async, game_is_running, send_animation_async

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
            send_async(bot, chat.id, text=f"○ {game.control_player.user.first_name} contrôle ({controller})\n● {game.current_player.user.name} à toi de jouer.",
                       reply_markup=InlineKeyboardMarkup(choice))
            # add this information to the game info list
            game.game_round += 1

    if game.play_round == (len(game.players) * 5):
        print(game.game_info)
        # KORA
        if game.control_card.value == '3':
            # DOUBLE KORA - if the 4th round was controlled with 3 by the same player
            if game.game_info[3].get('control_card').value == '3' and game.game_info[3].get('control_player').user.id == game.control_player.user.id:
                send_animation_async(
                    bot, chat.id, animation="https://media.giphy.com/media/zrj0yPfw3kGTS/giphy.gif", caption=f"Fin de partie! {game.control_player.user.first_name} gagne par DOUBLE KORA (33) !")
                logger.debug(
                    f"WIN GAME *DOUBLE-KORA* ({game.control_player.user.id}) in {chat.id}")
            else:
                send_animation_async(
                    bot, chat.id, animation="https://media.giphy.com/media/WrgtbRE1zywNy/giphy.gif", caption=f"Fin de partie! {game.control_player.user.first_name} gagne par KORA!")
                logger.debug(
                    f"WIN GAME *KORA* ({game.control_player.user.id}) in {chat.id}")

        # Normal win
        else:
            send_animation_async(
                bot, chat.id, animation="https://media.giphy.com/media/W9WSk4tEU1aJW/giphy.gif", caption=f"Fin de partie! {game.control_player.user.first_name} a gagné!")
            logger.debug(
                f"WIN GAME ({game.control_player.user.id}) in {chat.id}")

        gm.end_game(chat, user)


def save_info(user, card, play_round, game_round):
    """ Save the information for the current round """
