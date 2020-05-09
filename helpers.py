from telegram import ParseMode
from telegram.ext import CommandHandler

from vars import dispatcher
from utils import send_async


def help_handler(update, context):
    """Handler for the /help command"""
    help_text = "> Suivez les étapes suivantes:\n\n1. Ajoutez ce bot a un groupe\n2. Une fois dans le groupe, commençez une nouvelle partie avec /new\_game ou alors ajoutez-vous a une partie avec /join\n3. Ensuite lorsqu'au moins 2 joueurs ont rejoint la partie, commencez avec /start\_lamap\n4. Taggez le bot avec `@lamapbot` ensuite tappez `espace`. Vous verrez vos cartes et vous pourriez jouer. vous pouvez aussi cliquer sur 'via @lamapbot' pour voir vos cartes\n\n\n> Commandes d'administrateur (ou de lanceur de partie):\n/kick - Choissisez un jouer a retirer de la partie\n/close - Arrêter de prendre de nouveaux joueurs\n\n- [Lamap Updates](https://telegram.me/lamapbotupdates)\n- [Lamap Beta](https://telegram.me/lamapbeta)\n- [Lamap Devs](https://telegram.me/lamapdevs)"

    send_async(context.bot, update.message.chat_id, text=help_text,
               parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def modes(update, context):
    """Handler for the /modes_help command"""
    """ modes_explanation = "Ici on joue La Map, comme on connait là:\n\n🎴 *La Santé* – équivalent à un Classico (🃏) mais pour les pauvres.\n\n👮🏾‍♂️ *Le Bleu* – sans Kora, trois 7, trois 3 ni d'autres règles du kwatt\n\n🃏 *Le Classico [EN COURS DE DEVELOPEMENT]* – avec Kora, trois 7, trois 3, couleurs gagnent avec l'argent.\n" """

    modes_explanation = "LaMapBot est encore **version de dévéloppement**. On ne jouera que la map classique ici: 5 cartes, 4 joueurs, celui qui contrôle à la fin gagne."

    send_async(context.bot, update.message.chat_id, text=modes_explanation,
               parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def how_to_play(update, context):
    """Handler for the /how_to_play command"""
    h_t_p = "Regles de jeu"

    send_async(context.bot, update.message.chat_id, text=h_t_p,
               parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def rules(update, context):
    """Handler for the /rules command"""
    rules_text = "Regles de jeu"

    send_async(context.bot, update.message.chat_id, text=rules_text,
               parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def register():
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('modes_help', modes))
    dispatcher.add_handler(CommandHandler('how_to_play', how_to_play))
    dispatcher.add_handler(CommandHandler('rules', rules))
