"""
Handles all the callbacks from the bot
"""

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultCachedSticker as Sticker,
)
from telegram.ext import ContextTypes
from common import interactions, jobs
from common.exceptions import (
    NotEnoughPlayersError,
    PlayerAlreadyInGameError,
    PlayerIsBanned,
    PlayerIsPoor,
    PlayerNotInGameError,
    TooManyPlayersError,
)
from config import SUPER_ADMIN_LIST

from deck import Card

from orchestrator import Orchestrator
from player import Player


async def handle_query(
    orchestrator: Orchestrator, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """handles callback queries (basically button clicks)"""
    query = update.callback_query

    if query and query.from_user and query.message and update.effective_chat:
        # if the query starts by "ACH" it's an achievement
        if query.data and query.data.startswith("ACH"):
            await interactions.ACHIEVEMENTS_DETAILS(query, context)
            return

        chat_id = update.effective_chat.id
        game = orchestrator.games[chat_id]
        user = query.from_user

        # join game query
        if query.data == "join_game":
            await join_game(update, query, game, user)

        # start game query
        elif query.data == "start_game":
            await start_game(update, context, query, chat_id, orchestrator, game, user)

        await query.answer()


async def join_game(update, query, game, user):
    """makes a player join the game from the query callback"""
    try:
        player = Player(user)
        game.add_player(player)
        msg = await update.effective_chat.send_message(
            f"{player.user.first_name} j'ai coupé tes cartes mon pro!"
        )
        game.add_message_to_delete(msg.message_id)
    except PlayerAlreadyInGameError:
        await query.answer("Calme toi! Tes cartes sont posés.", show_alert=True)
    except TooManyPlayersError:
        await query.answer("C'est plein, tu vas jouer après.", show_alert=True)
    except PlayerIsBanned:
        await query.answer("Tu es banni, tu ne joues pas.", show_alert=True)
    except PlayerIsPoor:
        await query.answer(
            "Tu sais bien que tu es pauvre, pourquoi tu nous déranges?", show_alert=True
        )


async def start_game(update, context, query, chat_id, orchestrator, game, user):
    """starts the game properly from the query callback"""
    is_admin = False
    is_super_admin = False

    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        is_admin = True

    if str(user.id) in SUPER_ADMIN_LIST:
        is_super_admin = True

    if (game.creator.id == user.id) or is_admin or is_super_admin:
        try:
            game.start_game()
            jobs.remove_job_if_exists(str(chat_id), context)
            await interactions.FIRST_CARD(update, context, chat_id, game, orchestrator)
            # delete the game messages
            for message_id in game.messages_to_delete:
                await context.bot.delete_message(chat_id, message_id)
        except NotEnoughPlayersError:
            await interactions.NOT_ENOUGH_PLAYERS(chat_id, query=query)

    else:
        await query.answer(
            "Tu n'as pas ouvert le terre, tu ne peux pas lancer",
            show_alert=True,
        )


async def process_inline_query_result(
    orchestrator: Orchestrator, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handles a selected inline query result.
    This is usually when a player picks a card
    """
    if update.chosen_inline_result:
        try:
            chat_id = int(update.chosen_inline_result.query or 0)
            game = orchestrator.games[chat_id]
            player = game.get_player(update.chosen_inline_result.from_user.id)
            if game.started and game.current_player:
                card = Card.from_id(update.chosen_inline_result.result_id)
                # play the card
                card_played, card_correctly_played = game.play_card(player, card)
                if card_played and card_correctly_played:
                    # if the game ends after playing the card register it
                    if not game.started:
                        await interactions.END_GAME(context, chat_id, game)
                        orchestrator.end_game(chat_id, context)
                        return

                    await interactions.PLAY_CARD(context, chat_id, game, orchestrator)

                elif card_played and not card_correctly_played:
                    await interactions.WRONG_CARD(context, chat_id, game, card, player)
        except KeyError:
            ...


async def handle_inline_query(orchestrator: Orchestrator, update: Update):
    """
    Handles all inline queries.
    Is triggered when a user attempts an inline query
    its aim is to understand the query and return the players' cards
    or let them know that they can't play
    """
    query_results = list()
    if update.inline_query:
        try:
            chat_id = int(update.inline_query.query or 0)
            game = orchestrator.games[chat_id]
            player = game.get_player(update.inline_query.from_user.id)
            if game.started and game.current_player:
                for card in sorted(player.hand_of_cards):
                    if game.is_playable_card(card, player.hand_of_cards):
                        query_results.append(Sticker(str(card), card.sticker))
                    else:
                        query_results.append(
                            Sticker(
                                str(card),
                                card.sticker,
                                input_message_content=InputTextMessageContent(""),
                            )
                        )
            else:
                raise KeyError

        except KeyError:
            # show nothing if the game is not started
            query_results.append(
                InlineQueryResultArticle(
                    "nogame",
                    title="Pas de partie dans ce groupe",
                    input_message_content=InputTextMessageContent(
                        "Aucune partie n'est lancé ici, commence une nouvelle avec /play."
                    ),
                )
            )
        except PlayerNotInGameError:
            query_results.append(
                InlineQueryResultArticle(
                    "notplaying",
                    title="Tu ne joues pas dans ce groupe",
                    input_message_content=InputTextMessageContent(
                        "J'attends la fin de la partie, faites moi savoir quand je peux jouer"
                    ),
                )
            )
        finally:
            await update.inline_query.answer(
                query_results, cache_time=0, is_personal=True
            )
