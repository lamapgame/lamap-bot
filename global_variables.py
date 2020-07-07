from config import TOKEN, WORKERS, DB_URL
from telegram.ext import Updater
from game_manager import GameManager
from database import db

''' db.bind('postgres', user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, database=DB_NAME, port=DB_PORT) '''

db.bind('postgres', DB_URL)
db.generate_mapping(create_tables=True)

updater = Updater(token=TOKEN, workers=WORKERS, use_context=True)
gm = GameManager()
dispatcher = updater.dispatcher
