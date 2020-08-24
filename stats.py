from pony.orm import db_session
from user_db import UserDB


@db_session
def init_stats(id, name):
    """ User init stats """
    u = UserDB.get(id=id)
    un = UserDB.get(name=name)
    if not u:
        UserDB(id=id)
    if not un:
        u.name = name


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


@db_session
def user_won(id, style, nkap, bet):
    """ User win """
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    else:
        u.points += 2
        u.wins += 1
        u.wl_streak += 1
        if nkap:
            u.nkap += bet
            u.points += 30
        if style is "kora":
            if nkap:
                u.nkap += bet
            u.points += 2
            u.wins_kora += 1
        elif style is "dbl_kora":
            if nkap:
                u.nkap += bet*3
            u.points += 4
            u.wins_dbl_kora += 1
        elif style is "333":
            u.points += 1
            u.wins_333 += 1
        elif style is "777":
            u.points += 1
            u.wins_777 += 1
        elif style is "21":
            u.points += 1
            u.wins_21 += 1
        elif style is "fam":
            u.points += 1
            u.wins_fam += 1
        u.last_game_win = True


@db_session
def user_lost(id, style, nkap, bet):
    """ User lost """
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    else:
        u.points -= 1
        u.losses += 1
        u.wl_streak -= 1
        if nkap:
            u.nkap -= bet
            u.points -= 1
        if style is "kora":
            if nkap:
                u.nkap -= bet
            u.points -= 1
            u.losses_kora += 1
        elif style is "dbl_kora":
            if nkap:
                u.nkap -= bet*3
            u.points -= 2
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


@db_session
def reset_all_stats(id):
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    else:
        u.points = 0
        u.games_started = 0
        u.games_played = 0
        u.kicked = 0
        u.quit = 0
        u.losses = 0
        u.losses_333 = 0
        u.losses_777 = 0
        u.losses_21 = 0
        u.losses_kora = 0
        u.losses_fam = 0
        u.losses_dbl_kora = 0
        u.last_game_win = 0
        u.wins = 0
        u.wins_333 = 0
        u.wins_777 = 0
        u.wins_21 = 0
        u.wins_fam = 0
        u.wins_kora = 0
        u.wins_dbl_kora = 0
        u.wl_streak = 0
        u.nkap = 100


@db_session
def get_nkap(id):
    u = UserDB.get(id=id)
    if not u:
        UserDB(id=id)
    return u.nkap
