from telegram import ParseMode
from telegram.ext import CommandHandler

from vars import dispatcher


def help_handler(update, context):
    """Handler for the /help command"""
    help_text = "Suivez les étapes suivantes:\n\n1. Ajoutez ce bot a un groupe\n2. Une fois dans le groupe, commençez une nouvelle partie avec /new ou alors ajoutez-vous a une partie avec /join\n"

    update.message.reply_text(help_text, )



def modes(bot, update):
    """Handler for the /modes_help command"""
    modes_explanation = "Ici on joue La Map, comme on connait là.\n\n🃏 Le classique avec Kora, trois 7, trois 3, couleurs gagnent avec l'argent.\n 🦉 Le bleu, sans Kora, trois 7, trois 3 ni autres règles du kwatt\n ⚕ La Santé, equivalent a un classique mais pour les pauvres.\n"
    update.message.reply_text(modes_explanation)


def register():
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('modes', modes))
