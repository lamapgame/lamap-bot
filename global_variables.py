from config import TOKEN, WORKERS
import logging
from telegram.ext import Updater
from game_manager import GameManager
from database import db

db.bind('sqlite', 'themap.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

updater = Updater(token=TOKEN, workers=WORKERS, use_context=True)
gm = GameManager()
dispatcher = updater.dispatcher
