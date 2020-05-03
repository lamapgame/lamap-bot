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


from config import WAITING_TIME, DEFAULT_GAMEMODE, MIN_PLAYERS


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
        send_async(bot, chat.id, text="Il n'y a aucune partie en cours, crée une nouvelle avec /new_game.",
                   reply_to_message_id=update.message.message_id)

    except AlreadyJoinedError:
        send_async(bot, chat.id, text=f'{update.message.from_user.name}, vous avez déjà rejoint la partie qui va se debuter bientôt.',
                   reply_to_message_id=update.message.message_id)

    else:
        send_async(bot, chat.id, text=f'{update.message.from_user.name} à réjoint la partie !',
                   reply_to_message_id=update.message.message_id)


def start_lamap(context, update, args, job_queue):
    """ Handler for the /start_lamap command"""
    bot = context.bot

    if update.message.chat.type != 'private':
        chat = update.message.chat

        try:
            game = gm.chatid_games[chat.id][-1]
        except (KeyError, IndexError):
            send_async(
                bot, chat.id, text="Il n'y a aucune partie en cours, crée une nouvelle avec /new_game.")
            return

        if game.started:
            send_async(
                bot, chat.id, text=f'{update.message.from_user.name}, la partie a déjà commencée.')

        elif len(game.players) < MIN_PLAYERS:
            send_async(
                bot, chat.id, f'Une partie doit avoir au moins {MIN_PLAYERS} joueurs pour commencer. Utilisez /join pour rejoindre une partie en cours.')

        else:
            game.start()
            for player in game.players:
                player.draw_hand()

    else:
        help_handler(bot, update)


def help_me(update, context):
    update.message.reply_text(
        "Utilise /new_game pour lancer une partie de Lamap.")


def main():

    # Get the dispatcher to register handlers
    dispatcher.add_handler(CommandHandler('new_game', new_game))
    dispatcher.add_handler(CommandHandler(
        'start_lamap', start_lamap, pass_args=True, pass_job_queue=True))
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
