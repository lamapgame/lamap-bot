from __future__ import annotations
from typing import TYPE_CHECKING

from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from common.jobs import remove_job_if_exists
from common.utils import mention, send_reply_message
from config import GAME_START_TIMEOUT, TIME_TO_AFK

if TYPE_CHECKING:
    from deck import Card
    from game import Game
    from orchestrator import Orchestrator
    from player import Player


# remove the linter warning for the snake case
# :p this is my chosen interaction notation, I like it.

# pylint: disable=invalid-name


async def INIT_USER(update: Update) -> None:
    if update.message and update.message.chat.type == "private":
        if update.effective_user and update.message:
            await update.message.reply_text(
                f"Ao {update.effective_user.first_name}.\nBienvenue sur Lamap Bot. c'est en 3 étapes! \n\n1. Tchouk moi dans un groupe\n2. Mets moi ADMIN\n3. Lance /play et on se met bien. \n\nSi tu souhaites apprendre à jouer, lance /learn et je t'explique tout!"
            )
    else:
        await send_reply_message(update, "DM moi!")


async def LEARN(update: Update) -> None:
    if update.effective_user and update.message and update.effective_chat:
        rules_text = "La Map est un jeu de cartes rapide de 2-4 joueurs.\nPour qu'un joueur gagne, il doit d'avoir le contrôle du jeu à la fin.\nPour prendre le contrôle, il faut jouer une carte de la même famille et supérieur en chiffre à la carte qui contrôle ce tour. Si vous n'avez pas une carte correspondante, vous jouez ce que vous voulez\n\n- [Clique ici pour tout savoir.](https://lamap-bot.vercel.app/learn)"

        if update.message.chat.type == "private":
            await update.message.reply_text(rules_text, ParseMode.MARKDOWN, True)
        else:
            rules_cta = "Je t'ai écrit en DM. Verifie tes messages privés."
            await update.effective_chat.send_message(
                rules_cta,
                ParseMode.MARKDOWN,
                True,
                reply_to_message_id=update.message.message_id,
            )
            await update.effective_user.send_message(
                rules_text, ParseMode.MARKDOWN, True
            )


async def NEW_GAME(update, game: Game):
    keyboard = [
        [
            InlineKeyboardButton("🖐🏽 Joindre", callback_data="join_game"),
            InlineKeyboardButton("Lancer ✨", callback_data="start_game"),
        ],
    ]

    message = await update.effective_chat.send_animation(
        "https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized.gif",
        caption=f"{game.creator.first_name} veut nous mettre bien. Qui est chaud?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return message


async def END_GAME(context: ContextTypes.DEFAULT_TYPE, chat_id: int, game: Game):
    # get the names of all losers separated by a comma
    losers = ", ".join(
        [
            mention(player.user.first_name, f"tg://user?id={player.id}")
            for player in game.losers
        ]
    )
    winners = ", ".join(
        [
            mention(player.user.first_name, f"tg://user?id={player.id}")
            for player in game.winners
        ]
    )

    if game.controlling_player:
        message = await context.bot.send_animation(
            chat_id,
            "https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized.gif",
            caption=f"{winners} nous a allumé comme il faut et comme d'habitude {losers} perds. On remet ça?",
        )
        return message


async def END_GAME_BY_AFK(context: ContextTypes.DEFAULT_TYPE, chat_id: int, game: Game):
    if game.controlling_player:
        message = await context.bot.send_animation(
            chat_id,
            "https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized.gif",
            caption=f"{game.controlling_player.user.first_name} a gagné par forfait. On remet ça ?",
        )
        return message


async def FIRST_CARD(update, game: Game):
    if game.current_player:
        choice = [
            [
                InlineKeyboardButton(
                    text="Dégager",
                    switch_inline_query_current_chat=str(game.chat_id),
                )
            ]
        ]
        message = await update.effective_chat.send_message(
            f"{game.current_player.user.first_name} tu joues la première carte",
            reply_markup=InlineKeyboardMarkup(choice),
        )
        return message
    else:
        raise ValueError("No current player")


async def WARN_AFK(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job

    if job:
        chat_id: int = job.data["chat_id"]  # type: ignore
        game: Game = job.data["game"]  # type: ignore
        player: Player = job.data["player"]  # type: ignore
        msg = await context.bot.send_message(
            chat_id,
            f"{mention(player.user.first_name, f'tg://user?id={player.id}')} si tu ne joue pas dans les prochaines {int(TIME_TO_AFK/2)} secondes tu perds",
        )
        game.add_message_to_delete(msg.message_id)


async def PLAY_CARD(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    game: Game,
    orchestrator: Orchestrator,
):
    # clear the previous turn afk job
    remove_job_if_exists(str(chat_id), context)

    if game.current_player and game.prev_controlling_card and game.controlling_player:
        c_list = []
        game_round_from_0 = game.round - 1
        for _ in range(game_round_from_0):
            c_list.append("🎴")
        for _ in range(5 - game_round_from_0):
            c_list.append("🃏")

        choice = [
            [
                InlineKeyboardButton(
                    text=f"".join(c_list),
                    switch_inline_query_current_chat=str(game.chat_id),
                )
            ]
        ]

        controlling_player = game.controlling_player.user
        current_player = game.current_player.user
        message = await context.bot.send_message(
            chat_id,
            f"👑 {mention(controlling_player.first_name, f'tg://user?id={current_player.id}')} - {game.prev_controlling_card.icon}{game.prev_controlling_card.value}\n〰️\n🤙🏾 {mention(current_player.first_name, f'tg://user?id={current_player.id}')} à toi.",
            reply_markup=InlineKeyboardMarkup(choice),
        )

        passed_data = {
            "chat_id": chat_id,
            "game": game,
            "player": game.current_player,
            "orchestrator": orchestrator,
        }

        context.job_queue.run_once(  # type: ignore
            WARN_AFK,
            int(TIME_TO_AFK / 2),
            passed_data,
            name=str(object=chat_id),
        )
        context.job_queue.run_once(  # type: ignore
            orchestrator.end_game_from_afk,
            int(TIME_TO_AFK),
            passed_data,
            name=str(chat_id),
        )
        return message
    else:
        raise Exception("error in computing player and controlling card")


async def WRONG_CARD(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    game: Game,
    card: Card,
    player: Player,
):
    current_controlling_card = game.controlling_card
    if not game.controlling_card:
        current_controlling_card = game.prev_controlling_card

    if not current_controlling_card:
        message = await context.bot.send_message(
            chat_id,
            f"🤦🏾‍♂️ {mention(player.user.first_name, f'tg://user?id={player.id}')}Merci on a vu!\n Mais ce n'est pas ton tour de jouer",
        )
        return message

    if (game.current_player != player) and game.started:
        message = await context.bot.send_message(
            chat_id,
            f"🤦🏾‍♂️ {mention(player.user.first_name, f'tg://user?id={player.id}')}, merci on a vu!\n Mais ce n'est pas ton tour de jouer",
        )
    else:
        message = await context.bot.send_message(
            chat_id,
            f"Ok tara, on a vu, mais ce n'est pas le {card.icon} qui contrôle ce tour. C'est le {current_controlling_card.value}{current_controlling_card.icon} \n\nJe sais que tu a la carte, joue la!",
        )

    return message


async def WARN_GAME_START(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job

    if job:
        chat_id: int = job.data["chat_id"]  # type: ignore
        game: Game = job.data["game"]  # type: ignore
        msg = await context.bot.send_message(
            chat_id, f"On lance dans {int(GAME_START_TIMEOUT/2)} secondes"
        )
        game.add_message_to_delete(msg.message_id)


async def NOT_ENOUGH_PLAYERS(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE | None = None,
    query: CallbackQuery | None = None,
) -> None:
    text = "Pas assez de joueurs pour lancer.\nInvite les autres à rejoindre avant de lancer"
    if context:
        await context.bot.send_message(chat_id, text)
    if query:
        await query.answer(text, show_alert=True)
