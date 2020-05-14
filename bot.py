# python modules
import logging
from pprint import pprint, pformat
import json

# telegram api
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import InlineQueryHandler, ChosenInlineResultHandler, Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

# bot modules
import helpers
import logger
from deck import Deck
from global_variables import gm, updater, dispatcher
from errors import (NoGameInChatError, LobbyClosedError, AlreadyJoinedError,
                    NotEnoughPlayersError, DeckEmptyError)
from utils import send_async, answer_async, delete_async, TIMEOUT
from start_bot import start_bot
from results import (add_no_game, add_not_started,
                     add_other_cards, add_card, game_info)
from actions import do_play_card


from config import WAITING_TIME, DEFAULT_GAMEMODE, MIN_PLAYERS


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def notify_me(update, context):
    bot = context.bot
    """Handler for /notify_me command, pm people for next game"""
    chat_id = update.message.chat_id
    if update.message.chat.type == 'private':
        send_async(bot, chat_id, text=f"Envoyez cette commande dans un groupe avec le bot et vous serez notifié lorsqu'une nouvelle partie sera lancé.")
    else:
        try:
            gm.remind_dict[chat_id].add(update.message.from_user.id)
        except KeyError:
            gm.remind_dict[chat_id] = {update.message.from_user.id}


def new_game(update, context):
    """/new_game command handler"""
    chat_id = update.message.chat_id
    title = update.message.chat.title
    bot = context.bot
    if update.message.chat.type == 'private':
        helpers.help_handler(update, context)
    else:
        if chat_id in gm.remind_dict:
            for user in gm.remind_dict[chat_id]:
                send_async(
                    bot, user, text=f"Une nouvelle partie a été lancé dans le groupe {title}")
            del gm.remind_dict[chat_id]
        game = gm.new_game(update.message.chat)
        game.starter = update.message.from_user
        game.owner.append(update.message.from_user.id)

        # Reply to inform the start of game
        send_async(context.bot, chat_id,
                   text=f"Partie créée par {game.starter.first_name}! Réjoignez avec /join et commencez le jeu avec /start_lamap")


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
        delete_async(bot, chat.id, message_id=update.message.message_id)
        send_async(
            bot, chat.id, text=f'{update.message.from_user.name} à réjoint la partie !')


def start_lamap(update, context):
    """Handler for the /start_lamap command"""
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
                bot, chat.id, text=f'Une partie doit avoir au moins {MIN_PLAYERS} joueurs pour commencer. Utilisez /join pour rejoindre une partie en cours.')

        else:
            game.start()
            for player in game.players:
                player.draw_hand()
            choice = [[InlineKeyboardButton(
                text=f"Tu dégage avec quoi?", switch_inline_query_current_chat='')]]

            @run_async
            def send_first():
                ''' Send the first card and player '''
                bot.send_message(chat.id, text=f"La partie vient d'être lancée, {game.starter.name}, Tu joues la première carte", reply_markup=InlineKeyboardMarkup(
                    choice), timeout=TIMEOUT)

            send_first()

    else:
        help_handler(bot, update)


def reply_to_query(update, context):
    """
    Handler for inline queries.
    Builds the result list for inline queries and answers to the client.
    """
    results = list()
    bot = context.bot

    try:
        user = update.inline_query.from_user
        user_id = user.id
        players = gm.userid_players[user_id]
        player = gm.userid_current[user_id]
        game = player.game
    except KeyError:
        add_no_game(results)
    else:
        # the game has not yet started
        if not game.started:
            if user_is_creator(user, game):
                logger.debug(f"{user.id} wants to start a game")
            else:
                add_not_started(results)

        elif user_id == game.current_player.user.id:
            # to help show the cards in the same order each time
            playable = player.playable_cards()
            for card in sorted(player.cards):
                add_card(game, card, results, can_play=(card in playable))

        elif user_id != game.current_player.user.id or not game.started:
            for card in sorted(player.cards):
                add_card(game, card, results, can_play=False)

    answer_async(bot, update.inline_query.id, results, cache_time=0,
                 switch_pm_parameter='select')


def process_result(update, context):
    """ 
    Handler for chosen inline results.
    """

    bot = context.bot

    try:
        user = update.chosen_inline_result.from_user
        player = gm.userid_current[user.id]
        game = player.game
        result_id = update.chosen_inline_result.result_id
        chat = game.chat
    except (KeyError, AttributeError):
        return

    do_play_card(bot, player, result_id)


def close_game(update, context):
    ''' Handler for the close command '''
    chat = update.message.chat
    bot = context.bot
    user = update.message.from_user
    games = gm.chatid_games.get(chat.id)

    if not games:
        send_async(bot, chat.id, f"Il n'y a aucune partie en cours dans ce chat")

    game = games[-1]

    if user.id in game.owner:
        game.open = False
        send_async(
            bot, chat.id, f"La partie est fermée. Vous ne pouvez plus joindre.")
        return

    else:
        send_async(
            bot, chat.id, f"Seul le créateur de la partie {game.starter.name} ou l'admin peuvent effectuer cette action", reply_to_message_id=update.message.message_id)
        return


def help_me(update, context):
    update.message.reply_text(
        "Utilise /new_game pour lancer une partie de Lamap."
    )


def main():

    # Get the dispatcher to register handlers
    dispatcher.add_handler(InlineQueryHandler(reply_to_query))
    dispatcher.add_handler(ChosenInlineResultHandler(process_result))
    dispatcher.add_handler(CommandHandler('new_game', new_game))
    dispatcher.add_handler(CommandHandler('start_lamap', start_lamap))
    dispatcher.add_handler(CommandHandler('join', join_game))
    dispatcher.add_handler(CommandHandler('close', close_game))
    dispatcher.add_handler(CommandHandler('help', help_me))
    dispatcher.add_handler(CommandHandler('notify_me', notify_me))

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
