from telegram import ParseMode
from telegram.ext import CommandHandler

from pony.orm import db_session
from user_db import UserDB

from global_variables import dispatcher
from utils import mention


def help_handler(update, context):
    """Handler for the /help command"""

    # pyright: reportInvalidStringEscapeSequence=false
    help_text = "Cette commande ne peut être lancé que dans un groupe.\nAjoutez ce bot a votre groupe, rendez le administrateur, lancez une nouvelle partie avec /new\_game et suivez les instructions.\n\nUtilisez /rules pour apprendre les règles\n\n\n- [Lamap Updates Channel](https://t.me/lamapupdates)\n- [Lamap Devs Group](https://t.me/lamapdevs)"

    context.bot.send_message(update.message.chat_id, text=help_text,
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def start(update, context):
    """ Handler for /start command """
    start_txt = (
        "Ao !? \n\n1.Tchouk moi dans un groupe\n2. Mets moi ADMIN\n3. Lance /new\_game et on se met bien."
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
            f"`{str(u.nkap)+' Ň':<3}`    {mention(user)}"
            f"\n\n`{u.games_played:<3}`    {'Parties jouées'}"
            f"\n`{u.wins:<3}`    {'Parties gagnées'+w_pct}"
            f"\n`{u.losses:<3}`    {'Parties perdues'+l_pct}"
            f"\n`{ufinished:<3}`    {'Non terminées'+ufinished_pct}"
            f"\n`{u.wins_kora:<3}`    {'Kora donnés'}"
            f"\n`{u.losses_kora:<3}`    {'Kora reçus'}"
            f"\n`{u.quit:<3}`    {'Fois banquées'}"
            f"\n\n`{u.points:<3}`    {'Points'}"
        )

        context.bot.send_message(update.message.chat_id, text=stats_txt,
                                 parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def register():
    dispatcher.add_handler(CommandHandler('apprendre', apprendre))
    dispatcher.add_handler(CommandHandler('tchoko', tchoko))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stats', stats))
