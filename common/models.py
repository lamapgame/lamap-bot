from __future__ import annotations
from math import log10
from typing import TYPE_CHECKING, Any
from datetime import datetime
from pony.orm import PrimaryKey, Set, Required, db_session

from common.database import db
from config import BASE_POINTS

if TYPE_CHECKING:
    from game import Game
    from telegram import User


class UserDB(db.Entity):
    """The user entity"""

    _table_ = "users"
    id = PrimaryKey(int, auto=False, size=64)  # Telegram User ID
    name = Required(str)
    verified = Required(bool, default=False)
    # Relationship to Game Statistics
    game_statistics = Set("GameStatisticsDB")
    # Relationship to User Achievements
    achievements = Set("AchievementsDB")


class GameStatisticsDB(db.Entity):
    """Game statistics entity, contains all player stats"""

    _table_ = "stats"
    user = PrimaryKey(UserDB)
    points = Required(int, default=0)
    games_played = Required(int, default=0)
    kicked = Required(int, default=0)
    wrong_card = Required(int, default=0)
    quit = Required(int, default=0)
    slept = Required(int, default=0)
    losses = Required(int, default=0)
    losses_special = Required(int, default=0)
    losses_kora = Required(int, default=0)
    losses_dbl_kora = Required(int, default=0)
    wins = Required(int, default=0)
    wins_special = Required(int, default=0)
    wins_kora = Required(int, default=0)
    wins_dbl_kora = Required(int, default=0)
    wl_streak = Required(int, default=0)
    nkap = Required(int, default=30000)


class AchievementsDB(db.Entity):
    """User achievements entity, contains all player achievements"""

    _table_ = "achievements"
    user = Required(UserDB)
    code = Required(str)
    displayed = Required(bool, default=True)
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
        AchievementsDB(user=new_user, code="ACH_NEW_PLAYER")


@db_session
def get_user(
    user: User,
) -> tuple[UserDB, GameStatisticsDB, Any]:
    """Returns a user and their stats from the database"""
    userdb = UserDB.get(id=user.id)

    # incase the user doesn't exist in the database yet,
    # probably their first time to play
    if not userdb:
        # log: f"[User] {user.id} - {user.first_name} first time user"
        raise ValueError("User doesn't exist in the database")

    gamestatsdb = GameStatisticsDB.get(user=userdb)
    achievements_query = AchievementsDB.select(lambda a: a.user == userdb)

    # players seem to always change name, so we need to update it
    userdb.name = user.first_name

    return (userdb, gamestatsdb, list(achievements_query))


# ----------------------
# ---- Stats Model ----
# ----------------------
@db_session
def get_stats(user: User) -> tuple[UserDB, GameStatisticsDB]:
    """Returns a user's stats from the database"""
    userdb = UserDB.get(id=user.id)
    return userdb, GameStatisticsDB.get(user=userdb)


@db_session
def compute_game_stats(game: Game):
    """Compute the points for the winners and the loosers"""
    winners = game.winners
    loosers = game.losers
    nkap = game.nkap
    points = BASE_POINTS

    # do not compute stats if there's no winner or no looser
    if len(winners) == 0 or len(loosers) == 0:
        return

    # if player wins by kora, double the points and the money
    if game.end_reason == "KORA":
        points *= 2
        nkap *= 2

    # if player wins by double kora, quadruple
    if game.end_reason == "DBL_KORA":
        points *= 4
        nkap *= 4

    # if we are playing a money game, assign points based on the nkap
    if nkap > 0:
        # logarithmic scale for money games
        # details: https://chat.openai.com/share/5db4c576-8e26-4339-a6e5-2e660a492ff6
        points = int(BASE_POINTS * log10(1 + nkap))

    for player in winners:
        # add points to the db
        stats = GameStatisticsDB.get(user=player.user.id)
        stats.points += points
        stats.wins += 1
        stats.games_played += 1
        stats.wl_streak += 1
        stats.nkap += game.nkap

        # if a game finishes by AFK or QUIT at the >3 round, the player wins 3 times the nkap
        # this is because the looser might have done this on purpose to avoid losing money
        if (game.end_reason == "AFK" or game.end_reason == "QUIT") and game.round >= 3:
            stats.nkap += game.nkap * 3

        if game.end_reason == "KORA":
            stats.wins_kora += 1
        if game.end_reason == "DBL_KORA":
            stats.wins_dbl_kora += 1
        if game.end_reason == "SPECIAL":
            stats.wins_special += 1

    for player in loosers:
        stats = GameStatisticsDB.get(user=player.user.id)
        stats.points -= points // 2
        stats.wins -= 1
        stats.games_played -= 1
        stats.wl_streak -= 1
        stats.nkap -= game.nkap

        # if a game finishes by AFK or QUIT >3 round, the player loses 3 times the nkap to all players
        if (game.end_reason == "AFK" or game.end_reason == "QUIT") and game.round >= 3:
            stats.nkap -= game.nkap * 3 * len(winners)

        if game.end_reason == "KORA":
            stats.losses_kora += 1
        if game.end_reason == "DBL_KORA":
            stats.losses_dbl_kora += 1
        if game.end_reason == "SPECIAL":
            stats.losses_special += 1


# ----------------------
# ---- Achievements Model -
# ----------------------
@db_session
def get_achievements(user_id: int):
    """Get the achievements of a user"""
    achievements = AchievementsDB.select(lambda a: a.user == user_id)
    return achievements
