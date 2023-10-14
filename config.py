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
