from pony.orm import db_session
from user_db import UserDB


@db_session
def users():
    """ Users """


@db_session
def user_quit(id):
    """ User quit """
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    else:
        u.quit += 1
        u.points -= 0.5


@db_session
def user_kicked(id):
    """ User kicked """
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    else:
        u.kicked += 1
        u.points -= 0.5


@db_session
def user_plays(id):
    """ User plays """
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    else:
        u.games_played += 1
        u.points += 0.5


@db_session
def user_started(id):
    """ User started """
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    else:
        u.games_started += 1
        u.points += 0.5


@db_session
def user_won(id, style):
    """ User win """
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    else:
        u.points += 2
        u.wins += 1
        u.wl_streak += 1
        if style is "kora":
            u.wins_kora += 1
        elif style is "dbl_kora":
            u.wins_dbl_kora += 1
        elif style is "333":
            u.wins_333 += 1
        elif style is "777":
            u.wins_777 += 1
        elif style is "21":
            u.wins_21 += 1
        elif style is "fam":
            u.wins_fam += 1
        u.last_game_win = True


@db_session
def user_lost(id, style):
    """ User lost """
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    else:
        u.points -= 1
        u.losses += 1
        u.wl_streak -= 1
        if style is "kora":
            u.losses_kora += 1
        elif style is "dbl_kora":
            u.losses_dbl_kora += 1
        elif style is "333":
            u.losses_333 += 1
        elif style is "777":
            u.losses_777 += 1
        elif style is "21":
            u.losses_21 += 1
        elif style is "fam":
            u.losses_fam += 1
        u.last_game_win = False
