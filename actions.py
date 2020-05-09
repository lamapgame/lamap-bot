import random

import logging

import card as c
from datetime import datetime

from telegram import Message, Chat, InlineKeyboardButton, InlineKeyboardMarkup

from config import WAITING_TIME
from errors import DeckEmptyError, NotEnoughPlayersError
from vars import gm
from utils import send_async, game_is_running, next_player_message

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

    # todo: give mid-play infos
    choice = [[InlineKeyboardButton(
        text=f"Afficher mes cartes", switch_inline_query_current_chat='')]]

    send_async(bot, chat.id, text=f"○ {game.current_player.next.user.name} prends contrôle du jeu.\n● {game.current_player.next.user.name} à toi de jouer",
               reply_markup=InlineKeyboardMarkup(choice))

    if game.last_card is None:
        player.controls_game = True

    if len(player.cards) == 1:
        send_async(bot, chat.id, text="Dernière carte!")

    if len(player.cards) == 0:
        send_async(bot, chat.id, text=f"{user.first_name} a Gagné!")

        try:
            gm.leave_game(user, chat)
        except NotEnoughPlayersError:
            send_async(bot, chat.id, text="Fin de partie!")

            gm.end_game(chat, user)
