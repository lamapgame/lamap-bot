from pony.orm import Optional, PrimaryKey
from database import db


class UserDB(db.Entity):
    id = PrimaryKey(int, auto=False, size=64)  # Telegram User ID
    name = Optional(str, default="")
    points = Optional(float, default=0)
    games_started = Optional(int, default=0)
    games_played = Optional(int, default=0)
    kicked = Optional(int, default=0)
    quit = Optional(int, default=0)
    losses = Optional(int, default=0)
    losses_333 = Optional(int, default=0)
    losses_777 = Optional(int, default=0)
    losses_21 = Optional(int, default=0)
    losses_kora = Optional(int, default=0)
    losses_fam = Optional(int, default=0)
    losses_dbl_kora = Optional(int, default=0)
    last_game_win = Optional(bool, default=False)  # To help calculate streak
    wins = Optional(int, default=0)
    wins_333 = Optional(int, default=0)
    wins_777 = Optional(int, default=0)
    wins_21 = Optional(int, default=0)
    wins_fam = Optional(int, default=0)
    wins_kora = Optional(int, default=0)
    wins_dbl_kora = Optional(int, default=0)
    wl_streak = Optional(int, default=0)
    nkap = Optional(int, default=0)
