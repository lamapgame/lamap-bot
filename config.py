import os
from dotenv import load_dotenv

# Load the stored environment variables
load_dotenv()

# Base values
# ----------------
# Telegram token
TOKEN = os.getenv("TOKEN")
# Connection url to db
DATABASE_URL = os.getenv("DATABASE_URL")

# Gameplay values
# ----------------
# time to start game after being initiated
GAME_START_TIMEOUT = int(os.getenv("GAME_START_TIMEOUT") or 40)
TIME_TO_AFK = int(os.getenv("TIME_TO_AFK") or 50)
LOGGING_CHAT_ID = os.getenv("LOGGING_CHAT_ID")


ACHIEVEMENTS = {
    "NEW_PLAYER": {
        "name": "Le nouveau",
        "emoji": "🐣",
        "description": "Bienvenu, tu as joué ta première partie.\n"
        "Reste concentré, ça va vite ici.",
    },
}
