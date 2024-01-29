from __future__ import annotations
import logging
from math import log10
from typing import TYPE_CHECKING, Any
from datetime import datetime
from pony.orm import PrimaryKey, Set, Required, db_session, desc

from common.database import db
from common.exceptions import (
    CannotTransferToBannedError,
    CannotTransferToBotError,
    CannotTransferToUnknownPlayerError,
    NotEnoughNkapError,
    UserIsBanned,
)
from config import BASE_POINTS, BOT_ID
from player import Player

if TYPE_CHECKING:
    from game import Game
    from telegram import User

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
    afk = Required(int, default=0)
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

    if userdb.verified is False:
        raise UserIsBanned()

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

    add_user(user)
    userdb = UserDB.get(id=user.id)
    return userdb, GameStatisticsDB.get(user=userdb)


# ruff: noqa: E501 # pylint: disable=line-too-long disable=anomalous-backslash-in-string


@db_session
def compute_game_achievements(player: Player, game: Game):
    stats = GameStatisticsDB.get(user=player.user.id)
    if (
        stats.games_played >= 150
        and AchievementsDB.get(user=player.id, code="ACH_NOVICE_PLAYER") is None
    ):
        AchievementsDB(user=player.id, code="ACH_NOVICE_PLAYER")
    if (
        stats.games_played >= 1500
        and AchievementsDB.get(user=player.id, code="ACH_MID_PLAYER") is None
    ):
        AchievementsDB(user=player.id, code="ACH_MID_PLAYER")
    if (
        stats.games_played >= 5000
        and AchievementsDB.get(user=player.id, code="ACH_PRO_PLAYER") is None
    ):
        AchievementsDB(user=player.id, code="ACH_PRO_PLAYER")
    if (
        stats.games_played >= 50000
        and AchievementsDB.get(user=player.id, code="ACH_GOD_PLAYER") is None
    ):
        AchievementsDB(user=player.id, code="ACH_GOD_PLAYER")
    if (
        stats.wl_streak == 20
        and AchievementsDB.get(user=player.id, code="ACH_LE_DON_MAN") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_DON_MAN")
    if (
        game.end_reason == "SPECIAL"
        and game.play_history[-1].move.value == 99
        and AchievementsDB.get(user=player.id, code="ACH_LA_FAMILLE") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LA_FAMILLE")
    if (
        stats.nkap <= -500_000_000
        and AchievementsDB.get(user=player.id, code="ACH_LE_PAUVRE") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_PAUVRE")
    if (
        stats.nkap >= 500_000_000
        and AchievementsDB.get(user=player.id, code="ACH_LE_BOBO") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_BOBO")
    if (
        stats.nkap >= 1_000_000_000
        and AchievementsDB.get(user=player.id, code="ACH_LE_TETE") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_TETE")
    if (
        stats.wins_kora >= 200
        and AchievementsDB.get(user=player.id, code="ACH_LE_KORATEUR") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_KORATEUR")
    if (
        stats.wins_dbl_kora >= 200
        and AchievementsDB.get(user=player.id, code="ACH_LE_SNACKBAR") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_SNACKBAR")
    if (
        stats.wins_special >= 200
        and AchievementsDB.get(user=player.id, code="ACH_LE_NTONG_MAN") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_NTONG_MAN")
    if (
        stats.wl_streak <= -20
        and AchievementsDB.get(user=player.id, code="ACH_LE_NOOB") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_NOOB")
    if (
        stats.quit >= 500
        and AchievementsDB.get(user=player.id, code="ACH_LE_NDEM_MAN") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_NDEM_MAN")
    if (
        stats.losses_kora >= 200
        and AchievementsDB.get(user=player.id, code="ACH_LE_KORATE") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_KORATE")
    if (
        stats.losses_dbl_kora >= 200
        and AchievementsDB.get(user=player.id, code="ACH_LE_BUVEUR") is None
    ):
        AchievementsDB(user=player.id, code="ACH_LE_BUVEUR")
    if (
        stats.nkap < 0
        and AchievementsDB.get(user=player.id, code="ACH_LE_BOBO") is not None
        and AchievementsDB.get(user=player.id, code="ACH_L'ANCIEN_RICHE") is None
    ):
        achievement = AchievementsDB.get(user=player.id, code="ACH_LE_BOBO")
        achievement.delete()
        AchievementsDB(user=player.id, code="ACH_L'ANCIEN_RICHE")
    if (
        stats.nkap > 0
        and AchievementsDB.get(user=player.id, code="ACH_LE_PAUVRE") is not None
        and AchievementsDB.get(user=player.id, code="ACH_LA_REMONTADA") is None
    ):
        achievement = AchievementsDB.get(user=player.id, code="ACH_LE_PAUVRE")
        achievement.delete()
        AchievementsDB(user=player.id, code="ACH_LA_REMONTADA")


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
        nkap = nkap * 2

    # if player wins by double kora, quadruple
    if game.end_reason == "DBL_KORA":
        points *= 4
        nkap = nkap * 4

    # if we are playing a money game, assign points based on the nkap
    if nkap > 0:
        # logarithmic scale for money games
        # details: https://chat.openai.com/share/5db4c576-8e26-4339-a6e5-2e660a492ff6
        points = int(BASE_POINTS * log10(1 + nkap))

    for player in winners:
        # add points to the db
        stats = GameStatisticsDB.get(user=player.user.id)
        amount_won = 0
        stats.points += points
        stats.wins += 1
        stats.games_played += 1
        if stats.wl_streak < 0:
            stats.wl_streak = 1
        else:
            stats.wl_streak += 1

        # Compute achievements
        compute_game_achievements(player, game)

        # if a game finishes by AFK or QUIT at the >3 round,
        # the player wins 3 times the nkap
        # this is because the looser might quit to avoid losing money
        if (game.end_reason == "AFK" or game.end_reason == "QUIT") and game.round >= 3:
            amount_won += nkap * 3

        if game.end_reason == "KORA":
            stats.wins_kora += 1
        if game.end_reason == "DBL_KORA":
            stats.wins_dbl_kora += 1
        if game.end_reason == "SPECIAL":
            stats.wins_special += 1

        # if the game ends by afk, pay the nkap to all players
        # else, the winner takes from the loosers
        if game.end_reason == "AFK":
            amount_won = nkap
        else:
            amount_won = nkap * len(loosers)

        stats.nkap += amount_won
        game.amount_won = amount_won

        # find this player in the game and update the amount
        for p in game.players:
            if p.id == player.id:
                p.nkap = amount_won
                p.points = points

    for player in loosers:
        stats = GameStatisticsDB.get(user=player.user.id)
        amount_lost = 0
        stats.points = stats.points - (points // 2)
        stats.losses += 1
        stats.games_played += 1
        if stats.wl_streak > 0:
            stats.wl_streak = -1
        else:
            stats.wl_streak -= 1

        # if a game finishes by AFK or QUIT >3 round,
        # the player loses 3 times the nkap to all players
        if (game.end_reason == "AFK" or game.end_reason == "QUIT") and game.round >= 3:
            amount_lost += nkap * 3 * len(winners)
        else:
            amount_lost = nkap

        if game.end_reason == "AFK":
            stats.afk += 1
        if game.end_reason == "QUIT":
            stats.quit += 1
        if game.end_reason == "KORA" and player.is_koratable:
            stats.losses_kora += 1
        if game.end_reason == "DBL_KORA" and player.is_koratable:
            stats.losses_dbl_kora += 1
        if game.end_reason == "SPECIAL":
            stats.losses_special += 1

        stats.nkap -= amount_lost

        # Computing achievements
        compute_game_achievements(player, game)

        # find this player in the game and update the amount
        for p in game.players:
            if p.id == player.id:
                p.nkap = amount_lost
                p.points = (points // 2) * -1


@db_session
def compute_transfer_nkap(from_id: int, to_id: int, amount: int):
    """Transfer nkap from one user to another"""
    userdb_from = UserDB.get(id=from_id)
    userdb_to = UserDB.get(id=to_id)

    if userdb_to is None:
        raise CannotTransferToUnknownPlayerError()

    stats_from = GameStatisticsDB.get(user=userdb_from)
    stats_to = GameStatisticsDB.get(user=userdb_to)

    if userdb_to.verified is False or userdb_from.verified is False:
        raise CannotTransferToBannedError()

    if stats_from.nkap >= amount:
        stats_from.nkap -= amount
        stats_to.nkap += amount
    else:
        raise NotEnoughNkapError()


@db_session
def compute_ret_rem(user_id: int, amount: int, ret: bool = True):
    """Rem or Ret nkap from one user to another"""
    userdb = UserDB.get(id=user_id)
    stats = GameStatisticsDB.get(user=userdb)

    if userdb.id == BOT_ID:
        raise CannotTransferToBotError()

    if ret:  # retour
        stats.nkap -= amount
    else:  # remboursement
        stats.nkap += amount


@db_session
def compute_ban_unban(user_id: int | User, ban: bool = True):
    """Ban or Unban a user"""
    if not isinstance(user_id, int):
        user_id = user_id.id

    userdb = UserDB.get(id=user_id)

    if userdb.id == BOT_ID:
        raise CannotTransferToBotError()

    if ban:  # ban
        userdb.verified = False
    else:  # unban
        userdb.verified = True


@db_session
def get_top_nkap():
    return GameStatisticsDB.select().order_by(lambda gs: desc(gs.nkap)).limit(15)[:]


@db_session
def get_top_points():
    return GameStatisticsDB.select().order_by(lambda gs: desc(gs.points)).limit(15)[:]


@db_session
def get_top_kora():
    return (
        GameStatisticsDB.select().order_by(lambda gs: desc(gs.wins_kora)).limit(15)[:]
    )


@db_session
def get_top_double_kora():
    return (
        GameStatisticsDB.select()
        .order_by(lambda gs: desc(gs.wins_dbl_kora))
        .limit(15)[:]
    )


# ----------------------
# ---- Achievements Model -
# ----------------------
@db_session
def get_achievements(user_id: int):
    """Get the achievements of a user"""
    achievements = AchievementsDB.select(lambda a: a.user == user_id)
    return achievements


@db_session
def add_achievement(user_id: int, code: str):
    """Add an achievement to a user"""
    userdb = UserDB.get(id=user_id)
    AchievementsDB(user=userdb, code=code)


@db_session
def remove_achievement(user_id: int, code: str):
    """Add an achievement to a user"""
    userdb = UserDB.get(id=user_id)
    achievement = AchievementsDB.get(user=userdb, code=code)
    if achievement:
        achievement.delete()


@db_session
def refresh_all_nkap(amount: int):
    """Refresh all nkap"""
    db.execute(
        """UPDATE stats SET nkap=$amount""",
        {"amount": amount},
    )
