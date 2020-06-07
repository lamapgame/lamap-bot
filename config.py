import json
import sys
import os

from dotenv import load_dotenv
from pathlib import Path

local_env_path = Path('.') / '.env.local'
prod_env_path = Path('.') / '.env.prod'

# read the config.json file
with open("config.json",
          "r") as f:
    config = json.loads(f.read())

WORKERS = config.get("WORKERS", 32)
ADMIN_LIST = config.get("ADMIN_LIST", None)
OPEN_LOBBY = config.get("OPEN_LOBBY", True)
DEFAULT_GAMEMODE = config.get("DEFAULT_GAMEMODE", "classic")
WAITING_TIME = config.get("WAITING_TIME", 60)
MIN_PLAYERS = config.get("min_players", 2)
MAX_PLAYERS = config.get("min_players", 4)
LOG_FILE = "./lamapbot.log"

if sys.argv[1] == "prod":
    load_dotenv(prod_env_path)
    TOKEN = os.getenv("TOKEN")
    print("prod", TOKEN)
else:
    load_dotenv(local_env_path)
    TOKEN = os.getenv("TOKEN")
    print("local", TOKEN)
