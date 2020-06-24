from telegram import ParseMode
from telegram.ext import CommandHandler

from pony.orm import db_session
from user_db import UserDB
from global_variables import dispatcher
from utils import send_async


def help_handler(update, context):
    """Handler for the /help command"""
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
    if update.message.chat.type == 'private':
        rules_text = "La Map est un jeu de cartes rapide de 2-4 joueurs.\nPour qu'un joueur gagnes, il doit d'avoir le contrôle du jeu à la fin.\nPour prendre le contrôle, il faut jouer une carte de la même famille et supérieur en chiffre à la carte qui contrôle ce tour. Si vous n'avez pas une carte correspondante, vous jouez ce que vous voulez\n\n- [Explications illustrées](https://github.io/blurdylan/lamapbot/htp)"
    else:
        rules_text = ("Ne t'affiches pas, vient me demander ça en solo.")

    context.bot.send_message(update.message.chat_id, text=rules_text,
                             parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)


def tchoko(update, context):
    """Handler for the /tchoko command"""
    tchoko_text = "Faire un don"

    if update.message.chat.type == 'private':
        tchoko_text = (
            "Ah! Tu veux me tchoko?\n\n"
            "- Cause avec le [freeboy ci](https://t.me/panachaud), pour gérer par Mobile Money.\n"
            "- Ou alors, tu peux gérer [sur Paypal](https://www.paypal.me/DylanTientcheu) si tu as la rage\n\n"
            "Mais, saches que ce n'est pas une bière qui va donner des bonnes cartes..._"
        )
    else:
        tchoko_text = ("En vrai? Vient on gère en solo...")

    context.bot.send_message(update.message.chat_id, text=tchoko_text,
                             parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)


@db_session
def stats(update, context):
    if update.message.reply_to_message is not None:
        user = update.message.reply_to_message.from_user
    else:
        user = update.message.from_user
    u = UserDB.get(id=user.id)

    if not u:
        UserDB(id=user.id)
        context.bot.send_message(
            update.message.chat_id, text="Mola, je n'ai pas tes stats. Il faut jouer d'abord.")
    else:
        w_pct = str(100 * float(u.wins)/float(u.games_played)) + "%"
        l_pct = str(100 * float(u.losses)/float(u.games_played)) + "%"

        stats_txt = (
            f"`{u.points:>6}`    {'points LaMap':<5}"
            f"\n`{u.games_played:>6}`    {'parties joués':<5}"
            f"\n`{u.wins:>6}`    {'parties gagnées':<5}"
            f"\n`{u.losses:>6}`    {'parties perdues':<5}"
            f"\n`{u.wins_kora:>6}`    {'Kora donnés':<5}"
            f"\n`{u.losses_kora:>6}`    {'Kora reçus':<5}"
            f"\n`{w_pct:>6}`    {'pct gagné':<5}"
            f"\n`{l_pct:>6}`    {'pct perdu':<5}"
            f"\n`{u.kicked:>6}`    {'parties quittées':<5}"
            f"\n`{u.quit:>6}`    {'fois chassés':<5}"
        )

        context.bot.send_message(update.message.chat_id, text=stats_txt,
                                 parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)


def register():
    dispatcher.add_handler(CommandHandler('apprendre', apprendre))
    dispatcher.add_handler(CommandHandler('tchoko', tchoko))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stats', stats))
