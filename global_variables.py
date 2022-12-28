from config import TOKEN, WORKERS, DB_URL
from telegram import ParseMode
from telegram.ext import Updater, Defaults
from game_manager import GameManager
from database import db


defaults = Defaults(parse_mode=ParseMode.MARKDOWN)

db.bind('postgres', DB_URL)
db.generate_mapping(create_tables=True)

updater = Updater(token=str(TOKEN), workers=WORKERS, defaults=defaults)
# LMjobQueue = updater.job_queue

gm = GameManager()
dispatcher = updater.dispatcher
