from config import TOKEN, WORKERS, DB_URL
from telegram import ParseMode
from telegram.ext import Updater, Defaults
from game_manager import GameManager
from database import db

''' db.bind('postgres', user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, database=DB_NAME, port=DB_PORT) '''


defaults = Defaults(parse_mode=ParseMode.MARKDOWN, run_async=True)

db.bind('postgres', DB_URL)
db.generate_mapping(create_tables=True)

updater = Updater(token=TOKEN, workers=WORKERS, defaults=defaults)
gm = GameManager()
dispatcher = updater.dispatcher
