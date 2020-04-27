from config import TOKEN
import logging
from telegram.ext import Updater

from game_manager import GameManager

updater = Updater(token=TOKEN, use_context=True)
gm = GameManager()
dispatcher = updater.dispatcher
