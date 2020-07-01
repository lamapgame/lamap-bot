from config import TOKEN, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, WORKERS, DB_NAME
import logging
from telegram.ext import Updater
from game_manager import GameManager
from database import db

db.bind('postgres', user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, database=DB_NAME, port=DB_PORT)
db.generate_mapping(create_tables=True)

updater = Updater(token=TOKEN, workers=WORKERS, use_context=True)
gm = GameManager()
dispatcher = updater.dispatcher
