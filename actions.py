import random

import logging

import card as c
from datetime import datetime

from telegram import Message, Chat, InlineKeyboardButton, InlineKeyboardMarkup

from config import WAITING_TIME
from errors import DeckEmptyError, NotEnoughPlayersError
from global_variables import gm
from utils import send_async, game_is_running, send_animation_async

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

    choice = [[InlineKeyboardButton(
        text=f"Afficher mes cartes", switch_inline_query_current_chat='')]]

    if game.control_player is not None:
        if game.play_round % len(game.players) == 0 and game.play_round < (len(game.players) * 5):
            game.control_card = None
            game.current_player = game.control_player

        if game.play_round != (len(game.players) * 5):
            send_async(bot, chat.id, text=f"○ {game.control_player.user.first_name} contrôle ({controller})\n● {game.current_player.user.name} à toi de jouer.",
                       reply_markup=InlineKeyboardMarkup(choice))

            game.game_round += 1

    if game.play_round == (len(game.players) * 5):
        # KORA
        if game.control_card.value == '3':
            send_animation_async(
                bot, chat.id, animation="https://media.giphy.com/media/WrgtbRE1zywNy/giphy.gif", caption=f"Fin de partie! {game.control_player.user.first_name} gagne par KORA!")

        # Normal win
        else:
            send_animation_async(
                bot, chat.id, animation="https://media.giphy.com/media/W9WSk4tEU1aJW/giphy.gif", caption=f"Fin de partie! {game.control_player.user.first_name} a gagné!")

        gm.end_game(chat, user)
