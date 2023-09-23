from telegram import Update
from telegram.constants import ParseMode
from common.utils import send_reply_message


async def INIT_USER(update: Update) -> None:
    if update.message and update.message.chat.type == "private":
        if update.effective_user and update.message:
            await update.message.reply_text(
                f"Ao {update.effective_user.first_name}.\nBienvenue sur Lamap Bot. c'est en 3 étapes! \n\n1. Tchouk moi dans un groupe\n2. Mets moi ADMIN\n3. Lance /play et on se met bien. \n\nSi tu souhaites apprendre à jouer, lance /learn et je t'explique tout!"
            )
    else:
        await send_reply_message(update, "Ca s'envoi en DM ça!")


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
