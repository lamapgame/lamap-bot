from telegram import ParseMode
from telegram.ext import CommandHandler

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
            "_Retiens que ça ne change rien sur tes cartes..._"
        )
    else:
        tchoko_text = ("En vrai? Vient on gère en solo...")

    context.bot.send_message(update.message.chat_id, text=tchoko_text,
                             parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)


def register():
    dispatcher.add_handler(CommandHandler('apprendre', apprendre))
    dispatcher.add_handler(CommandHandler('tchoko', tchoko))
    dispatcher.add_handler(CommandHandler('start', start))
