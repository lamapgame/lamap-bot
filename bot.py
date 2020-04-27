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

from config import TOKEN


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start_game(update, context):
    """/start_game command handler"""
    if update.message.chat.type != 'private':
        first_name = update.message.from_user.first_name
        update.message.reply_text(f'Salut {first_name}')

    else:
        helpers.help_handler(update, context)


def new_game(update, context):
    """/new_game command handler"""
    if update.message.chat.type == 'private':
        helpers.help_handler(update, context)
    else:
        name = update.message.from_user.name
        # logger.info(pformat(update.message, indent=1, width=5))
        update.message.reply_text(f'Salut {name}')


def draw_card(update, context):
    """draw a set of 5 cards"""
    Deck().shuffle()
    hand_of_cards = Deck().draw()
    update.message.reply_text(f'Cards: {hand_of_cards}')


""" 
def sticker(update, context):
    
    logger.info(update.message.sticker.file_id)
    file_id = update.message.sticker.file_id
    update.message.reply_text(f"{file_id}")
 """


def help_me(update, context):
    update.message.reply_text("Use /new_game to start this bot.")


def main():
    # Create the Updater and pass it the bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_game))
    dp.add_handler(CommandHandler('new_game', new_game))
    dp.add_handler(CommandHandler('help', help_me))

    dp.add_handler(CommandHandler('draw_card', draw_card))

    # on noncommand message
    # dp.add_handler(MessageHandler(Filters.all, sticker))

    dp.add_error_handler(logger.error)

    helpers.register()

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
