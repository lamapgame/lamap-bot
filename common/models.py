from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime
from pony.orm import Optional, PrimaryKey, Set, Required, db_session
from common.database import db

if TYPE_CHECKING:
    from telegram import User


class UserDB(db.Entity):
    """The user entity"""

    id = PrimaryKey(int, auto=False, size=64)  # Telegram User ID
    name = Required(str)
    verified = Optional(bool, default=False)
    # Relationship to Game Statistics
    game_statistics = Set("GameStatisticsDB")
    # Relationship to User Achievements
    achievements = Set("AchievementsDB")


class GameStatisticsDB(db.Entity):
    """Game statistics entity, contains all player stats"""

    user = PrimaryKey(UserDB)
    points = Optional(int, default=0)
    games_played = Optional(int, default=0)
    kicked = Optional(int, default=0)
    wrong_card = Optional(int, default=0)
    quit = Optional(int, default=0)
    slept = Optional(int, default=0)
    losses = Optional(int, default=0)
    losses_special = Optional(int, default=0)
    losses_kora = Optional(int, default=0)
    losses_dbl_kora = Optional(int, default=0)
    wins = Optional(int, default=0)
    wins_special = Optional(int, default=0)
    wins_kora = Optional(int, default=0)
    wins_dbl_kora = Optional(int, default=0)
    wl_streak = Optional(int, default=0)
    nkap = Optional(int, default=30000)


class AchievementsDB(db.Entity):
    """User achievements entity, contains all player achievements"""

    user = Required(UserDB)
    code = Required(str)
    displayed = Optional(bool, default=False)
    date_achieved = Required(datetime, default=datetime.now())
    PrimaryKey(user, code)


# ----------------------
# ---- User Model ----
# ----------------------
@db_session
def add_user(user: User) -> None:
    """Adds a user to the database if they don't exist"""
    if not UserDB.exists(id=user.id):
        new_user = UserDB(id=user.id, name=user.first_name, verified=True)
        GameStatisticsDB(user=new_user)
        AchievementsDB(user=new_user, code="NEW_PLAYER")


@db_session
def get_user(user: User) -> tuple[UserDB, GameStatisticsDB]:
    """Returns a user and their stats from the database"""
    return (UserDB.get(id=user.id), GameStatisticsDB.get(user=user))
