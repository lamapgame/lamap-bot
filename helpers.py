from telegram import ParseMode
from telegram.ext import CommandHandler

from pony.orm import db_session, desc
from user_db import UserDB

from global_variables import dispatcher
from utils import mention, n_format


def help_handler(update, context):
    """Handler for the /help command"""

    # pyright: reportInvalidStringEscapeSequence=false
    help_text = "Cette commande ne peut être lancé que dans un groupe.\nAjoutez ce bot a votre groupe, rendez le administrateur, lancez une nouvelle partie avec /nkap et suivez les instructions.\n\nUtilisez /rules pour apprendre les règles\n\n\n- [Lamap Updates Channel](https://t.me/lamapupdates)\n- [Lamap Devs Group](https://t.me/lamapdevs)"

    context.bot.send_message(update.message.chat_id, text=help_text,
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def start(update, context):
    """ Handler for /start command """
    start_txt = (
        "Ao !? \n\n1.Tchouk moi dans un groupe\n2. Mets moi ADMIN\n3. Lance /nkap et on se met bien."
    )
    context.bot.send_message(update.message.chat_id, text=start_txt,
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def apprendre(update, context):
    """Handler for the /apprendre command"""
    rules_text = "La Map est un jeu de cartes rapide de 2-4 joueurs.\nPour qu'un joueur gagne, il doit d'avoir le contrôle du jeu à la fin.\nPour prendre le contrôle, il faut jouer une carte de la même famille et supérieur en chiffre à la carte qui contrôle ce tour. Si vous n'avez pas une carte correspondante, vous jouez ce que vous voulez\n\n- [Clique ici pour tout savoir.](https://lamap-bot.vercel.app/learn)"

    if update.message.chat.type == 'private':
        context.bot.send_message(update.message.chat_id, text=rules_text,
                                 parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)
    else:
        rules_cta = ("Ne t'affiches pas, vient me demander ça en solo.")
        context.bot.send_message(update.message.chat_id, text=rules_cta,
                                 parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)
        context.bot.send_message(update.message.from_user.id, text=rules_text,
                                 parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def tchoko(update, context):
    """Handler for the /tchoko command"""
    tchoko_text = (
        "Oh ma personne! Vient on gère...\n\n"
        "- Cause avec le [freeboy ci](https://t.me/panachaud), pour gérer par Mobile Money.\n"
        "- Ou alors, tu peux gérer [sur Paypal](https://www.paypal.me/DylanTientcheu) si tu as la rage\n\n"
        "Mais, saches que ce n'est pas une bière qui va donner des bonnes cartes..."
    )

    if update.message.chat.type == 'private':
        tchoko_text1 = (
            "Ah tu veux me donner une bière! Vient on gère...\n\n"
            "- Cause avec le [freeboy ci](https://t.me/panachaud), pour gérer par Mobile Money.\n"
            "- Ou alors, tu peux gérer [sur Paypal](https://www.paypal.me/DylanTientcheu) si tu as la rage\n\n"
            "Mais, saches que ce n'est pas une bière qui va donner des bonnes cartes..."
        )
        context.bot.send_message(update.message.chat_id, text=tchoko_text1,
                                 parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)
    else:
        tchoko_texto = "En vrai? Vient on gère en solo..."
        context.bot.send_message(update.message.chat_id, text=tchoko_texto,
                                 parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)
        context.bot.send_message(update.message.from_user.id, text=tchoko_text,
                                 parse_mode=ParseMode.MARKDOWN)


@db_session
def stats(update, context):
    if update.message.reply_to_message is not None:
        user = update.message.reply_to_message.from_user
    else:
        user = update.message.from_user
    u = UserDB.get(id=user.id)

    if not u:
        UserDB(id=user.id, name=user.name)
        context.bot.send_message(
            update.message.chat_id, text="Mola, je n'ai pas tes stats. Il faut d'abord jouer.")
    else:
        ufinished = u.games_played - (u.wins + u.losses)

        if u.games_played != 0:
            w_pct = " (" + str(round(100 * float(u.wins) /
                                     float(u.games_played), 1)) + "%" + ")"
            l_pct = " (" + str(round(100 * float(u.losses) /
                                     float(u.games_played), 1)) + "%" + ")"
            ufinished_pct = " (" + str(round(100 * float(ufinished) /
                                             float(u.games_played), 1)) + "%" + ")"
        else:
            w_pct = " (0%)"
            l_pct = " (0%)"
            ufinished = 0
            ufinished_pct = " (0%)"

        stats_txt = (
            f"`{n_format(u.nkap):<3}`    {mention(user)}"
            f"\n\n`{n_format(u.games_played):<3}`    {'Parties jouées'}"
            f"\n`{n_format(u.wins):<3}`    {'Parties gagnées'+w_pct}"
            f"\n`{n_format(u.losses):<3}`    {'Parties perdues'+l_pct}"
            f"\n`{n_format(ufinished):<3}`    {'Non terminées'+ufinished_pct}"
            f"\n`{n_format(u.wins_kora):<3}`    {'Kora donnés'}"
            f"\n`{n_format(u.losses_kora):<3}`    {'Kora reçus'}"
            f"\n\n`{n_format(u.points):<3}`    {'Points'}"
        )

        context.bot.send_message(
            update.message.chat_id, text=stats_txt, disable_web_page_preview=True)


def dm_information(chat, user, bot, result, points, bet, gains_losses):
    ''' DM player about his results '''
    title = chat.title
    text = ""
    if result == "L":
        text = (
            f"{title}: PERDU"
            f"\n\nMise: `{n_format(bet)}`"
            f"\nPertes: `{n_format(gains_losses)}`"
            f"\nPoints: `-{points}`"
        )
    if result == "W":
        text = (
            f"{title}: GAGNÉ"
            f"\n\nMise: `{n_format(bet)}`"
            f"\nGains: `+{n_format(gains_losses)}`"
            f"\nPoints: `+{points}`"
        )

    bot.send_message(user, text=text, disable_web_page_preview=True)


@db_session
def top_players(update, context):
    top_10_players = list(UserDB.select().order_by(
        lambda u: desc(u.points))[:10])
    top_txt = []
    for idx, user in enumerate(top_10_players, start=1):
        string = f"`{idx}–` *{user.name}* - {user.points} Points\n"
        top_txt.append(string)

    context.bot.send_message(update.message.chat_id, text=''.join(
        top_txt), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@db_session
def top_rich_players(update, context):
    top_10_rich = list(UserDB.select().order_by(
        lambda u: desc(u.nkap))[:10])
    top_txt = []
    for idx, user in enumerate(top_10_rich, start=1):
        string = f"`{idx}–` *{user.name}* - {n_format(user.nkap)}\n"
        top_txt.append(string)

    context.bot.send_message(update.message.chat_id, text=''.join(top_txt),
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def register():
    dispatcher.add_handler(CommandHandler('apprendre', apprendre))
    dispatcher.add_handler(CommandHandler('tchoko', tchoko))
    dispatcher.add_handler(CommandHandler('top10', top_players))
    dispatcher.add_handler(CommandHandler('top10nkap', top_rich_players))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stats', stats))
