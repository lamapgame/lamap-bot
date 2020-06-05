# python modules
import logging
from pprint import pprint, pformat
import json
import random

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
                    NotEnoughPlayersError, DeckEmptyError, GameAlreadyStartedError)
from utils import send_async, send_animation_async, answer_async, delete_async, user_is_creator_or_admin, user_is_creator, TIMEOUT
from start_bot import start_bot
from results import (add_no_game, add_not_started,
                     add_other_cards, add_card, game_info)
from actions import do_play_card


from config import WAITING_TIME, DEFAULT_GAMEMODE, MIN_PLAYERS, LOG_FILE


logging.basicConfig(
    filename=LOG_FILE, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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

        join_btn = [[InlineKeyboardButton(
            "Rejoindre", callback_data="join_game")]]

        # Reply to inform the start of game
        send_animation_async(
            context.bot, chat_id, animation="https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized-large.gif", caption=f"Partie créée par {game.starter.first_name}! Rejoignez la partie avec le bouton ci dessous et commencez le jeu avec /start_lamap", reply_markup=InlineKeyboardMarkup(join_btn))


def join_game(update, context):
    """Handler for the /join command"""
    bot = context.bot
    if update.message is not None:
        chat = update.message.chat
        user = update.message.from_user
    else:
        chat = update.effective_message.chat
        user = update.effective_user

    if chat.type == 'private':
        helpers.help_handler(update, context)
        return
    try:
        gm.join_game(user, chat)

    except LobbyClosedError:
        send_async(bot, chat.id, text="La partie est fermée")

    except GameAlreadyStartedError:
        # delete_async(bot, chat.id, message_id=update.message.message_id)
        send_async(
            bot, chat.id, text="Impossible de rejoindre une partie en cours, utilisez /notify_me pour être notifié lorsque une nouvelle partie sera lancée dans ce groupe.")

    except NoGameInChatError:
        # delete_async(bot, chat.id, message_id=update.message.message_id)
        send_async(
            bot, chat.id, text="Il n'y a aucune partie en cours, crée une nouvelle avec /new_game.")

    except AlreadyJoinedError:
        # delete_async(bot, chat.id, message_id=update.message.message_id)
        send_async(
            bot, chat.id, text=f'{user.name}, vous avez déjà rejoint la partie qui va se debuter bientôt.')

    else:
        # delete_async(bot, chat.id, message_id=update.message.message_id)
        send_async(
            bot, chat.id, text=f'{user.name} à réjoint la partie !')


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
            # random.shuffle(game.players) # to make a random user start
            for player in game.players:
                player.draw_hand()
            choice = [[InlineKeyboardButton(
                text=f"Tu dégage avec quoi?", switch_inline_query_current_chat='')]]

            delete_async(bot, chat.id, message_id=update.message.message_id)

            @run_async
            def send_first():
                ''' Send the first card and player '''
                bot.send_message(chat.id, text=f"La partie vient d'être lancée, {game.current_player.user.name}, Tu joues la première carte", reply_markup=InlineKeyboardMarkup(
                    choice), timeout=TIMEOUT)

            game.first_player = game.current_player

            send_first()

    else:
        helpers.help_handler(update, context)


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
            ''' for card in sorted(player.cards):
                add_card(game, card, results, can_play=False) '''

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


def quit_game(update, context):
    """Handler for the /leave command"""
    chat = update.message.chat
    user = update.message.from_user
    bot = context.bot

    player = gm.player_for_user_in_chat(user, chat)

    if player is None:
        send_async(bot, chat.id, text=f"Tu n'est dans aucune partie dans ce groupe",
                   reply_to_message_id=update.message.message_id)
        return

    game = player.game
    user = update.message.from_user

    try:
        gm.leave_game(user, chat)

    except NoGameInChatError:
        send_async(bot, chat.id, text=f"Il n'y a aucune partie en cours dans groupe",
                   reply_to_message_id=update.message.message_id)

    except NotEnoughPlayersError:
        gm.end_game(chat, user)
        send_async(bot, chat.id, text=f"Plus assez de joueurs! Fin de partie!")

    else:
        if game.started:
            send_async(bot, chat.id,
                       text=f"Okay. Prochain joueur: {game.current_player.user.name}", reply_to_message_id=update.message.message_id)
        else:
            send_async(bot, chat.id, text=f"{user.name} a fui.",
                       reply_to_message_id=update.message.message_id)


def kill_game(update, context):
    """Handler for the /kill game"""
    chat = update.message.chat
    user = update.message.from_user
    games = gm.chatid_games.get(chat.id)
    bot = context.bot

    if update.message.chat.type == 'private':
        help_handler(bot, update)
        return

    if not games:
        send_async(bot, chat.id, text="Aucune partie lancé ici.")
        return

    game = games[-1]

    if user_is_creator_or_admin(user, game, bot, chat):

        try:
            gm.end_game(chat, user)
            send_async(bot, chat.id, text="J'ai tué le way!")

        except NoGameInChatError:
            send_async(bot, chat.id,
                       text="Aucune partie en cours", reply_to_message_id=update.message.message_id)

    else:
        send_async(
            bot, chat.id, text=f"Seul le créateur de la partie ({game.starter.first_name}) et un admin peuvent tuer le way.", reply_to_message_id=update.message.message_id)


def help_me(update, context):
    update.message.reply_text(
        "Utilise /new_game pour lancer une partie de Lamap."
    )


def cbhandler(update, context):
    query = update.callback_query
    if (query.data == 'join_game'):
        join_game(update, context)

    query.answer()


def main():

    # Get the dispatcher to register handlers
    dispatcher.add_handler(InlineQueryHandler(reply_to_query))
    dispatcher.add_handler(ChosenInlineResultHandler(process_result))
    dispatcher.add_handler(CommandHandler('new_game', new_game))
    dispatcher.add_handler(CommandHandler('start_lamap', start_lamap))
    dispatcher.add_handler(CommandHandler('join', join_game))
    dispatcher.add_handler(CommandHandler('close', close_game))
    dispatcher.add_handler(CommandHandler('quit', quit_game))
    dispatcher.add_handler(CommandHandler('help', help_me))
    dispatcher.add_handler(CommandHandler('tuer_le_way', kill_game))
    dispatcher.add_handler(CommandHandler('notify_me', notify_me))
    dispatcher.add_handler(CallbackQueryHandler(cbhandler))

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
