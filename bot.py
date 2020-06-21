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
import logger as loggero


from global_variables import gm, updater, dispatcher
from errors import (NoGameInChatError, LobbyClosedError, AlreadyJoinedError,
                    NotEnoughPlayersError, DeckEmptyError, GameAlreadyStartedError, MaxPlayersReached)
from utils import send_async, send_animation_async, answer_async, delete_async, delete_start_msgs, user_is_creator_or_admin, user_is_creator, TIMEOUT
from start_bot import start_bot
from results import (add_no_game, add_not_started,
                     add_special_card, add_card, game_info, check_quick_win)
from actions import do_play_card

from settings import set_waiting_time


from config import WAITING_TIME, DEFAULT_GAMEMODE, MIN_PLAYERS, TIME_TO_START


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
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
                    bot, user, text=f"Ca veut déjà lancer dans le groupe {title}")
            del gm.remind_dict[chat_id]
        game = gm.new_game(update.message.chat)
        game.starter = update.message.from_user
        game.owner.append(update.message.from_user.id)

        join_btn = [
            [InlineKeyboardButton("Rejoindre", callback_data="join_game")]
        ]

        # Reply to inform the start of game
        send_animation_async(
            context.bot, chat_id, animation="https://media.giphy.com/media/37q7weFc48rocjJGW7/giphy.gif", caption=f"{game.starter.first_name} a ouvert le terre! Rejoint avec le bouton ci-dessous.", reply_markup=InlineKeyboardMarkup(join_btn), to_delete=True)

        # start the game after TIME_TO_START secs
        context.job_queue.run_once(
            start_the_game, TIME_TO_START, context=update)


def start_the_game(context):
    chat = context.job.context.effective_message.chat
    user = context.job.context.effective_user
    try:
        game = gm.chatid_games[chat.id][-1]
    except (KeyError, IndexError):
        return
    if len(game.players) >= MIN_PLAYERS and not game.started:
        start_lamap(context.job.context, context)
    elif not game.started:
        send_async(context.bot, chat.id,
                   text=f'Les gars ne sont pas chaud, je tue le way.')
        delete_start_msgs(context.bot, chat.id)


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
        send_async(bot, chat.id, text="La partie est fermée", to_delete=True)

    except MaxPlayersReached:
        send_async(bot, chat.id, text="Le terre est plein, tu ne peux pas joindre. Utilise /notify_me pour être notifié lorsque une nouvelle partie sera lancée dans ce groupe.", to_delete=True)

    except GameAlreadyStartedError:
        send_async(
            bot, chat.id, text="Impossible de rejoindre une partie en cours, utilise /notify_me pour être notifié lorsque une nouvelle partie sera lancée dans ce groupe.", to_delete=True)

    except NoGameInChatError:
        send_async(
            bot, chat.id, text="Il n'y a aucune partie en cours, crée une nouvelle avec /new_game.", to_delete=True)

    except AlreadyJoinedError:
        send_async(
            bot, chat.id, text=f"{user.name}, calme toi, j'ai déjà coupé tes cartes.", to_delete=True)

    else:
        send_async(
            bot, chat.id, text=f'{user.name} à réjoint la partie !', to_delete=True)


def start_lamap(update, context):
    """Handler for the /start_lamap command"""
    bot = context.bot

    if update.message is not None:
        chat = update.message.chat
        user = update.message.from_user
    else:
        chat = update.effective_message.chat
        user = update.effective_user

    if chat.type != 'private':
        try:
            game = gm.chatid_games[chat.id][-1]

        except (KeyError, IndexError):
            send_async(
                bot, chat.id, text="Il n'y a aucune partie en cours, crée une nouvelle avec /new_game.")
            return

        if game.started:
            send_async(
                bot, chat.id, text=f'{user.name}, la partie a déjà commencée.')

        elif len(game.players) < MIN_PLAYERS:
            send_async(
                bot, chat.id, text=f'Une partie doit avoir au moins {MIN_PLAYERS} joueurs pour commencer.', to_delete=True)
            gm.end_game(chat, user)

        else:
            game.start()
            delete_start_msgs(bot, chat.id)
            for player in game.players:
                player.draw_hand()
            choice = [[InlineKeyboardButton(
                text=f"Tu dégage avec quoi?", switch_inline_query_current_chat='')]]

            game.first_player = random.choice(game.players)
            game.current_player = game.first_player

            @run_async
            def send_first():
                ''' Send the first card and player '''
                bot.send_message(chat.id, text=f"La partie vient d'être lancée, {game.first_player.user.name}, Tu joues la première carte", reply_markup=InlineKeyboardMarkup(
                    choice), timeout=TIMEOUT)

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
            qw_check = check_quick_win(player.cards)
            if qw_check is not None and len(player.cards) == 5:
                add_special_card(game, qw_check, results, can_play=True)
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
    except (KeyError, AttributeError, ValueError):
        # handle errors that occurs when players play wrong cards
        return

    do_play_card(bot, player, result_id)


def close_game(update, context):
    ''' Handler for the close command '''
    chat = update.message.chat
    bot = context.bot
    user = update.message.from_user
    games = gm.chatid_games.get(chat.id)

    if not games:
        send_async(
            bot, chat.id, f"Il n'y a aucune partie en cours dans ce groupe")

    game = games[-1]

    if user.id in game.owner:
        game.open = False
        send_async(
            bot, chat.id, f"On a fermé le terre. Tu ne peux plus joindre.")
        return

    else:
        send_async(
            bot, chat.id, f"Tu es qui pour lock le terre? Seul le créateur de la partie {game.starter.name} ou l'admin peuvent lock le terre", reply_to_message_id=update.message.message_id)
        return


def quit_game(update, context):
    """Handler for the /leave command"""
    chat = update.message.chat
    user = update.message.from_user
    bot = context.bot

    player = gm.player_for_user_in_chat(user, chat)

    if player is None:
        send_async(bot, chat.id, text=f"Tu te banque alors que ça n'a pas commencé?",
                   reply_to_message_id=update.message.message_id)
        return

    game = player.game
    user = update.message.from_user

    try:
        if game.control_player != None:
            if game.control_player.user.id != user.id:
                gm.leave_game(user, chat)
            else:
                send_async(bot, chat.id, text=f"Molah, Tu pars où alors que tu as le contrôle ?",
                           reply_to_message_id=update.message.message_id)
                return
        elif game.current_player.user.id == user.id:
            send_async(bot, chat.id, text=f"{user.name} a fui en voyant ses cartes.",
                       reply_to_message_id=update.message.message_id)
            gm.leave_game(user, chat)
        else:
            send_async(bot, chat.id, text=f"{user.name} a fui sans voir ses cartes.",
                       reply_to_message_id=update.message.message_id)
            gm.leave_game(user, chat)

    except NoGameInChatError:
        send_async(bot, chat.id, text=f"Il n'y a aucune partie en cours dans groupe",
                   reply_to_message_id=update.message.message_id)

    except NotEnoughPlayersError:
        gm.end_game(chat, user)
        if game.control_player is None:
            send_async(
                bot, chat.id, text=f"Comment vous partez tous?! Fin de partie!")
        else:
            send_animation_async(
                bot, chat.id, animation="https://media.giphy.com/media/NG6dWJC9wFX2/giphy.gif", caption=f"Les gars ont tous fui?! Je considère que {game.control_player.user.first_name} a gagné")
            logger.debug(
                f"WIN GAME FOFEIT ({game.control_player.user.id}) in {chat.id}")

    else:
        if game.started:
            send_async(bot, chat.id,
                       text=f"{user.name} comme tu pars là, ne vient plus. Prochain joueur: {game.current_player.user.name}", reply_to_message_id=update.message.message_id)
            try:
                gm.leave_game(user, chat)

            except NotEnoughPlayersError:
                if game.control_player is None:
                    send_async(
                        bot, chat.id, text=f"Comment vous partez tous?! Fin de partie!")
                else:
                    send_animation_async(
                        bot, chat.id, animation="https://media.giphy.com/media/NG6dWJC9wFX2/giphy.gif", caption=f"Les gars ont tous fui?! Je considère que {game.control_player.user.first_name} a gagné")

                gm.end_game(chat, user)
        else:
            send_async(bot, chat.id, text=f"{user.name} a fui.",
                       reply_to_message_id=update.message.message_id)
            try:
                gm.leave_game(user, chat)
            except NotEnoughPlayersError:
                if game.control_player is None:
                    send_async(
                        bot, chat.id, text=f"Comment vous partez tous?! Fin de partie!")
                else:
                    send_animation_async(
                        bot, chat.id, animation="https://media.giphy.com/media/NG6dWJC9wFX2/giphy.gif", caption=f"Les gars ont tous fui?! Je considère que {game.control_player.user.first_name} a gagné")

                gm.end_game(chat, user)


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
            logger.debug("KILLED GAME in chat " +
                         str(chat.id) + "by user" + str(user.id))

        except NoGameInChatError:
            send_async(bot, chat.id,
                       text="Aucune partie en cours", reply_to_message_id=update.message.message_id)

    else:
        send_async(
            bot, chat.id, text=f"Tu es qui pour tuer le way? Seul le créateur de la partie ({game.starter.first_name}) et un admin peuvent tuer le way.", reply_to_message_id=update.message.message_id)


def kick_player(update, context):
    """Handler for the /chasser command"""
    bot = context.bot

    if update.message.chat.type == 'private':
        return

    chat = update.message.chat
    user = update.message.from_user

    try:
        game = gm.chatid_games[chat.id][-1]

    except (KeyError, IndexError):
        send_async(bot, chat.id,
                   text=f"On ne joue pas encore boss.",
                   reply_to_message_id=update.message.message_id, to_delete=True)
        return

    if not game.started:
        send_async(bot, chat.id,
                   text="La partie n'a pas encore débuté.",
                   reply_to_message_id=update.message.message_id)
        return

    if user_is_creator_or_admin(user, game, bot, chat):

        if update.message.reply_to_message:
            kicked = update.message.reply_to_message.from_user
            if game.control_player.user.id == kicked.id:
                send_async(bot, chat.id, text=f"Calme toi {user.name}, il a le contrôle.",
                           reply_to_message_id=update.message.message_id)
                return

            try:
                gm.leave_game(kicked, chat)

            except NoGameInChatError:
                send_async(bot, chat.id, text=f"Tu veux chasser {kicked.name} alors qu'il ne joue pas?",
                           reply_to_message_id=update.message.message_id)
                return

            except NotEnoughPlayersError:
                gm.end_game(chat, user)
                send_async(bot, chat.id,
                           text=f"Woko!! {user.name} a chassé {kicked.name}!")
                send_async(
                    bot, chat.id, text=f"Plus assez de joueurs, Fin de partie!")
                return

            send_async(
                bot, chat.id, text=f"C'est pas la salle d'attente ici, {user.name} a chassé {kicked.name}!")

        else:
            send_async(bot, chat.id,
                       text=f"Réessaies en repondant à un de ses messages.",
                       reply_to_message_id=update.message.message_id)
            return

        send_async(bot, chat.id,
                   text=f"C'est free... Prochain joueur: {game.current_player.user.name}",
                   reply_to_message_id=update.message.message_id)

    else:
        send_async(bot, chat.id,
                   text=f"Tu chasse en tant que qui ?",
                   reply_to_message_id=update.message.message_id)


def help_me(update, context):
    update.message.reply_text(
        "Utilise /new_game pour lancer une partie de Lamap."
    )


def cbhandler(update, context):
    bot = context.bot
    chat = update.effective_message.chat
    query = update.callback_query
    user = update.effective_user

    game = gm.chatid_games[chat.id][-1]

    if (query.data == 'join_game'):
        join_game(update, context)
    elif query.data == 'start_game':
        if user_is_creator_or_admin(user, game, bot, chat):
            start_lamap(update, context)

    query.answer()


def mes(update, context):
    if update.message.chat.type == 'private':
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Ok free")


def main():

    # Get the dispatcher to register handlers
    dispatcher.add_handler(InlineQueryHandler(reply_to_query))
    dispatcher.add_handler(ChosenInlineResultHandler(process_result))
    dispatcher.add_handler(CommandHandler('new_game', new_game))
    dispatcher.add_handler(CommandHandler('close', close_game))
    dispatcher.add_handler(CommandHandler('se_banquer', quit_game))
    dispatcher.add_handler(CommandHandler('help', help_me))
    dispatcher.add_handler(CommandHandler('tuer_le_way', kill_game))
    dispatcher.add_handler(CommandHandler('notify_me', notify_me))
    dispatcher.add_handler(CommandHandler('start_game', start_lamap))

    # muted commands
    dispatcher.add_handler(CommandHandler('join', join_game))
    dispatcher.add_handler(CommandHandler('chasser', kick_player))

    # callback queries handler
    dispatcher.add_handler(CallbackQueryHandler(cbhandler))

    # all handler (use ONLY for debugging!)
    # dispatcher.add_handler(MessageHandler(Filters.all, mes))

    dispatcher.add_error_handler(loggero.error)

    helpers.register()

    # Start the Bot
    start_bot(updater)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
