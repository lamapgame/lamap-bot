import json


with open("config.json",
          "r") as f:
    config = json.loads(f.read())

TOKEN = config.get("TOKEN")
WORKERS = config.get("WORKERS", 32)
ADMIN_LIST = config.get("ADMIN_LIST", None)
OPEN_LOBBY = config.get("OPEN_LOBBY", True)
DEFAULT_GAMEMODE = config.get("DEFAULT_GAMEMODE", "fast")
WAITING_TIME = config.get("WAITING_TIME", 90)
MIN_PLAYERS = config.get("min_players", 2)
MAX_PLAYERS = config.get("min_players", 4)
