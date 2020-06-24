from config import TOKEN, WORKERS
import logging
from telegram.ext import Updater
from database import db
from game_manager import GameManager

db.bind('sqlite', 'lamap.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

updater = Updater(token=TOKEN, workers=WORKERS, use_context=True)
gm = GameManager()
dispatcher = updater.dispatcher
