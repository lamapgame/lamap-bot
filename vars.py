from config import TOKEN, WORKERS
import logging
from telegram.ext import Updater

from game_manager import GameManager

updater = Updater(token=TOKEN, workers=WORKERS, use_context=True)
gm = GameManager()
dispatcher = updater.dispatcher
