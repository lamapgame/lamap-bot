# python modules
import logging
from pprint import pprint, pformat
import json

# telegram api
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# bot modules
import helpers
import logger
from deck import Deck
from vars import gm, updater, dispatcher
from errors import (NoGameInChatError, LobbyClosedError, AlreadyJoinedError,
                    NotEnoughPlayersError, DeckEmptyError)
from utils import send_async
from start_bot import start_bot


from config import TOKEN


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def new_game(update, context):
    """/new_game command handler"""
    chat_id = update.message.chat_id
    title = update.message.chat.title
    if update.message.chat.type == 'private':
        helpers.help_handler(update, context)
    else:
        if chat_id in gm.remind_dict:
            for user in gm.remind_dict[chat_id]:
                context.bot.send_message(
                    chat_id=chat_id, text=f"Une partie a été lancé dans le groupe {title}"
                )
            del gm.remind_dict[chat_id]
    game = gm.new_game(update.message.chat)
    game.starter = update.message.from_user
    game.owner.append(update.message.from_user.id)

    # Reply to inform the start of game
    send_async(context.bot, chat_id,
               text=f"Partie créée par {game.starter.name}! Réjoignez avec /join et commencez le jeu avec /start_lamap", reply_to_message_id=update.message.message_id)


def join_game(update, context):
    """Handler for the /join command"""
    chat = update.message.chat
    bot = context.bot

    if update.message.chat.type == 'private':
        helpers.help_handler(update, context)
        return
    try:
        gm.join_game(update.message.from_user, chat)

    except LobbyClosedError:
        send_async(bot, chat.id, text="La partie est fermée")

    except NoGameInChatError:
        send_async(bot, chat.id, text="Il n'y a aucune partie en cours, crée une nouvelle avec /new_game",
                   reply_to_message_id=update.message.message_id)

    except AlreadyJoinedError:
        send_async(bot, chat.id, text=f'{update.message.from_user.name}, vous avez déjà rejoint la partie qui va se débuter bientôt',
                   reply_to_message_id=update.message.message_id)

    else:
        send_async(bot, chat.id, text=f'{update.message.from_user.name} à réjoint la partie',
                   reply_to_message_id=update.message.message_id)


def help_me(update, context):
    update.message.reply_text("Use /new_game to start this bot.")


def main():

    # Get the dispatcher to register handlers
    dispatcher.add_handler(CommandHandler('new_game', new_game))
    dispatcher.add_handler(CommandHandler('join', join_game))
    dispatcher.add_handler(CommandHandler('help', help_me))

    # on noncommand message
    # dispatcher.add_handler(MessageHandler(Filters.all, sticker))

    dispatcher.add_error_handler(logger.error)

    helpers.register()

    # Start the Bot
    start_bot(updater)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
