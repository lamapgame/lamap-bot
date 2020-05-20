from telegram import ParseMode
from telegram.ext import CommandHandler

from global_variables import dispatcher
from utils import send_async


def help_handler(update, context):
    """Handler for the /help command"""
    help_text = "Cette commande ne peut être lancé que dans un groupe.\nAjoutez ce bot a votre groupe, rendez le administrateur, lancez une nouvelle partie avec /new\_game et suivez les instructions.\n\nUtilisez /rules pour apprendre les règles\n\n\n- [Lamap Updates Channel](https://t.me/lamapupdates)\n- [Lamap Private Bot](https://telegram.me/lamapprivatebot) *(en dévéloppement...)*\n- [Lamap Devs Group](https://t.me/lamapdevs)"

    send_async(context.bot, update.message.chat_id, text=help_text,
               parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def modes(update, context):
    """Handler for the /modes_help command"""
    """ modes_explanation = "Ici on joue La Map, comme on connait là:\n\n🎴 *La Santé* – équivalent à un Classico (🃏) mais pour les pauvres.\n\n👮🏾‍♂️ *Le Bleu* – sans Kora, trois 7, trois 3 ni d'autres règles du kwatt\n\n🃏 *Le Classico [EN COURS DE DEVELOPEMENT]* – avec Kora, trois 7, trois 3, couleurs gagnent avec l'argent.\n" """

    modes_explanation = "LaMapBot est encore en *version de dévéloppement*.\n\nOn ne jouera que la map classique: 5 cartes, 4 joueurs maxi, 3x3, 3x7, le 3 korate et celui qui contrôle à la fin gagne."

    send_async(context.bot, update.message.chat_id, text=modes_explanation,
               parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def rules(update, context):
    """Handler for the /rules command"""
    rules_text = "Regles de jeu"

    send_async(context.bot, update.message.chat_id, text=rules_text,
               parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def donate(update, context):
    """Handler for the /donate command"""
    donate_text = "Faire un don"

    send_async(context.bot, update.message.chat_id, text=donate_text,
               parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def register():
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('modes_help', modes))
    dispatcher.add_handler(CommandHandler('rules', rules))
    dispatcher.add_handler(CommandHandler('donate', donate))
