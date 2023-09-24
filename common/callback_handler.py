from telegram import Update
from telegram.ext import ContextTypes
from common import interactions
from common.exceptions import (
    NotEnoughPlayersError,
    PlayerAlreadyInGameError,
    TooManyPlayersError,
)

from orchestrator import Orchestrator
from player import Player


async def handle_query(
    orchestrator: Orchestrator, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """handles callback queries"""
    query = update.callback_query

    if query and query.from_user and query.message and update.effective_chat:
        chat_id = update.effective_chat.id
        game = orchestrator.games[chat_id]
        user = query.from_user
        if query.data == "join_game":
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

        elif query.data == "start_game":
            if game.creator.id == user.id:
                try:
                    game.start_game()
                    await interactions.FIRST_CARD(update, game)
                    # delete the game messages
                    for message_id in game.messages_to_delete:
                        await context.bot.delete_message(chat_id, message_id)
                except NotEnoughPlayersError:
                    await query.answer(
                        "Pas assez de joueurs pour lancer.\nInvite les autres à rejoindre avant de lancer",
                        show_alert=True,
                    )

            else:
                await query.answer(
                    "Tu n'as pas ouvert le terre, tu ne peux pas lancer",
                    show_alert=True,
                )

        await query.answer()
