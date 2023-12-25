from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Literal
import humanize

from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    User,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from common.jobs import remove_job_if_exists
from common.utils import mention, n_format, send_reply_message
from config import ACHIEVEMENTS, GAME_START_TIMEOUT, TIME_TO_AFK

if TYPE_CHECKING:
    from deck import Card
    from game import Game
    from orchestrator import Orchestrator
    from player import Player


# remove the linter warning for the snake case
# :p this is my chosen interaction notation, I like it.

# pylint: disable=invalid-name
# pylint: disable=line-too-long


async def INIT_USER(update: Update) -> None:
    if update.message and update.message.chat.type == "private":
        if update.effective_user and update.message:
            await update.message.reply_text(
                f"Ao {update.effective_user.first_name}.\nBienvenue sur Lamap Bot. c'est en 3 étapes! \n\n1. Tchouk moi dans un groupe\n2. Mets moi ADMIN\n3. Lance /play et on se met bien. \n\nSi tu souhaites apprendre à jouer, lance /learn et je t'explique tout!"
            )
    else:
        await send_reply_message(
            update,
            "Bienvenue sur Lamap Bot.\n"
            "Pour jouer, lance /play <montant> et je vous met bien.",
        )


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

    if game.nkap > 0:
        return await update.effective_chat.send_animation(
            "https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized.gif",
            caption=f"{game.creator.first_name} veut nous mettre bien."
            f" Il a déposé {n_format(game.nkap)}."
            "\nQui est chaud?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    return await update.effective_chat.send_animation(
        "https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized.gif",
        caption=f"{game.creator.first_name} veut nous mettre bien. Qui est chaud?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def CANNOT_START_GAME(update, reason: Literal["neg"]):
    if reason == "neg":
        await update.effective_chat.send_message(
            "Chez ta grand-mère, vous utilisez l'argent négatif ?"
        )


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

    if game.end_reason == "QUIT":
        message = await context.bot.send_animation(
            chat_id,
            "https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized.gif",
            caption=f"Il ne reste qu'un joueur, {winners} gagne {n_format(game.amount_won)} par forfait. On remet ça ?",
        )
        return message

    if game.end_reason == "SPECIAL":
        message = await context.bot.send_animation(
            chat_id,
            "https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized.gif",
            caption=f"{winners} a gagné {n_format(game.amount_won)} avec une carte spéciale. On remet ça ?",
        )
        return message

    if game.end_reason == "KILL":
        if not game.killer:
            raise ValueError("No killer")

        message = await context.bot.send_message(
            chat_id,
            f"🔨 {game.killer.first_name} a tué la partie. On remet ça ?",
        )
        return message

    if game.end_reason == "AFK":
        message = await context.bot.send_animation(
            chat_id,
            "https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized.gif",
            caption=f"{losers} a AFK. La mise était {n_format(game.nkap)} On remet ça?",
        )
        return message

    if game.controlling_player:
        message = await context.bot.send_animation(
            chat_id,
            "https://media.giphy.com/media/qrXMFgQ5UOI8g/giphy-downsized.gif",
            caption=f"{winners} nous a allumé comme il faut et prends {n_format(game.amount_won)}. On remet ça ?",
        )
        return message


async def NEXT_PLAYER(
    update,
    game: Game,
):
    if game.current_player:
        choice = [
            [
                InlineKeyboardButton(
                    text="Dégager",
                    switch_inline_query_current_chat=str(game.chat_id),
                )
            ]
        ]
        await update.effective_chat.send_message(
            f"{mention(game.current_player.user.first_name, f'tg://user?id={game.current_player.user.id}')} c'est toi qui joue maintenant",
            reply_markup=InlineKeyboardMarkup(choice),
        )


async def FIRST_CARD(
    update,
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    game: Game,
    orchestrator: Orchestrator,
):
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
            f"{mention(game.current_player.user.first_name, f'tg://user?id={game.current_player.user.id}')} tu joues la première carte",
            reply_markup=InlineKeyboardMarkup(choice),
        )
        passed_data = {
            "chat_id": chat_id,
            "game": game,
            "player": game.current_player,
            "orchestrator": orchestrator,
        }

        if not context.job_queue:
            raise ValueError("No job queue")

        # END GAME BY AFK
        context.job_queue.run_once(
            WARN_AFK,
            int(TIME_TO_AFK / 2),
            passed_data,
            name=str(object=chat_id),
        )
        context.job_queue.run_once(
            orchestrator.end_game_from_afk,
            int(TIME_TO_AFK),
            passed_data,
            name=str(chat_id),
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
                    text="".join(c_list),
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

        if not context.job_queue:
            raise ValueError("No job queue")

        context.job_queue.run_once(
            WARN_AFK,
            int(TIME_TO_AFK / 2),
            passed_data,
            name=str(object=chat_id),
        )
        context.job_queue.run_once(
            orchestrator.end_game_from_afk,
            int(TIME_TO_AFK),
            passed_data,
            name=str(chat_id),
        )
        return message
    else:
        raise ValueError("error in computing player and controlling card")


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
            f"🤦🏾‍♂️ {mention(player.user.first_name, f'tg://user?id={player.id}')}, merci on a vu!\n Mais ce n'est pas ton tour de jouer",
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
            f"🤦🏾‍♂️ Ok tara, on a vu, mais ce n'est pas le {card.icon} qui contrôle ce tour. C'est le {current_controlling_card.value}{current_controlling_card.icon} \n\nJe sais que tu a la carte, joue la!",
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


async def ACHIEVEMENTS_DETAILS(
    query: CallbackQuery, _context: ContextTypes.DEFAULT_TYPE
):
    if not query.data:
        return

    achievement_code, achievement_date = query.data.split("||")
    achievement_emoji = ACHIEVEMENTS[achievement_code]["emoji"]
    achievement_title = ACHIEVEMENTS[achievement_code]["name"]
    achievement_description = ACHIEVEMENTS[achievement_code]["description"]

    humanize.activate("fr_FR")
    date_from_now = humanize.naturaltime(
        datetime.now() - datetime.fromisoformat(achievement_date)
    )

    text = (
        f"{achievement_emoji} {achievement_title}\n\n{achievement_description}\n\n"
        f"Obtenu {date_from_now}"
    )
    await query.answer(text, show_alert=True)


async def CANNOT_KILL_GAME(update: Update) -> None:
    await send_reply_message(update, "Tu ne peux pas tuer une partie qui n'existe pas.")


async def NOT_ADMIN(update: Update) -> None:
    await send_reply_message(
        update, "Tara, tu n'as pas les accréditations pour faire ça."
    )


async def TRANSFER_NKAP(
    update: Update, amount: int, sender_name: str, reciever_name: str
):
    await send_reply_message(
        update, f"{sender_name} a donné {n_format(amount)} à {reciever_name}"
    )


async def CANNOT_TRANSFER_NKAP(
    update: Update,
    reason: Literal[
        "banned",
        "bot",
        "self",
        "not_enough",
        "unknown",
        "no_nkap_specified",
        "no_reply",
        "neg",
        "admin",
    ],
) -> None:
    if reason == "banned":
        await send_reply_message(update, "Be cool, tu ne peux pas donner à un banni.")

    elif reason == "bot":
        await send_reply_message(
            update, "Tu me donnes les dos là, tu ne verras plus jamais ça."
        )

    elif reason == "self":
        await send_reply_message(
            update,
            "Tu ne peux pas te donner à toi même. Sinon tout le monde va être riche.",
        )

    elif reason == "not_enough":
        await send_reply_message(update, "Tu n'as pas assez d'argent pour donner.")

    elif reason == "unknown":
        await send_reply_message(
            update, "Tara, je ne sais pas à qui tu veux transférer l'argent là."
        )

    elif reason == "neg":
        await send_reply_message(
            update,
            "Hahaha, tu dois être un free boy ein, toi là. Imagine que je te paies en négatif. Qui gagnes ?",
        )

    elif reason == "no_reply":
        await send_reply_message(update, "Tu dois répondre à un message pour donner.")

    else:
        await send_reply_message(update, "Je ne comprends pas boss.")


async def CANNOT_DO_THIS(update: Update) -> None:
    await send_reply_message(update, "Je ne comprends pas boss.")


async def DID_REM(update: Update, amount: int) -> None:
    await send_reply_message(
        update,
        f"C'est fait boss. J'ai déposé {n_format(amount)} dans son compte.",
    )


async def QUIT_GAME(update: Update, user: User):
    return await send_reply_message(
        update, f"{user.first_name} as fui, comme d'habitude..."
    )


async def CANNOT_QUIT_GAME(
    update: Update,
    reason: Literal["before_start", "not_in_game", "no_game", "controller"],
):
    message = None
    if reason == "before_start":
        message = await send_reply_message(
            update, "Tu ne peux pas quitter une partie qui n'a pas encore commencé."
        )
    elif reason == "not_in_game":
        message = await send_reply_message(
            update, "Tu ne peux pas quitter une partie dans laquelle tu n'es pas."
        )
    elif reason == "controller":
        message = await send_reply_message(
            update, "C'est toi qui contrôles, tu ne peux pas quitter maintenant."
        )
    elif reason == "no_game":
        message = await send_reply_message(
            update, "Tu ne peux pas quitter une partie qui n'existe pas."
        )
    return message


async def DID_RET(update: Update, amount: int) -> None:
    await send_reply_message(
        update,
        f"Le retour est géré. Le mboutman a payé {n_format(amount)}.",
    )


async def BLOCK_USER(update: Update, user: User | int) -> None:
    if isinstance(user, int):
        await send_reply_message(update, f"J'ai bloqué {user}.")
        return
    await send_reply_message(
        update, f"J'ai bloqué {mention(user.first_name, f'tg://user?id={user.id}')}."
    )


async def UNBLOCK_USER(update: Update, user: User | int) -> None:
    if isinstance(user, int):
        await send_reply_message(update, f"J'ai débloqué {user}.")
        return
    await send_reply_message(
        update, f"J'ai débloqué {mention(user.first_name, f'tg://user?id={user.id}')}."
    )


async def YOU_ARE_NOT_SUPER_ADMIN(update: Update) -> None:
    await send_reply_message(update, "Tu n'es pas un super admin.")
