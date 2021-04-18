import logging
from config import SUPERMOD_LIST
from stats import init_stats
from telegram import ParseMode
from telegram.ext import CommandHandler, CallbackContext, Updater

from pony.orm import db_session, desc
from user_db import UserDB

from global_variables import dispatcher
from utils import mention, n_format


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BOTS = [1397177261, 1101987755]


def help_handler(update, context):
    """Handler for the /help command"""

    help_text = "Cette commande ne peut être lancé que dans un groupe.\nAjoutez ce bot a votre groupe, rendez le administrateur, lancez une nouvelle partie avec /nkap et suivez les instructions.\n\nUtilisez /rules pour apprendre les règles\n\n\n- [Lamap Updates Channel](https://t.me/lamapupdates)\n- [Lamap Devs Group](https://t.me/lamapdevs)"

    context.bot.send_message(update.message.chat_id, text=help_text,
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def start(update, context):
    """ Handler for /start command """
    user = update.message.from_user
    init_stats(user.id, user.first_name)
    start_txt = (
        "Ao !? \n\n1.Tchouk moi dans un groupe\n2. Mets moi ADMIN\n3. Lance /nkap et on se met bien."
    )
    context.bot.send_message(update.message.chat_id, text=start_txt,
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def apprendre(update, context):
    """Handler for the /apprendre command"""
    rules_text = "La Map est un jeu de cartes rapide de 2-4 joueurs.\nPour qu'un joueur gagne, il doit d'avoir le contrôle du jeu à la fin.\nPour prendre le contrôle, il faut jouer une carte de la même famille et supérieur en chiffre à la carte qui contrôle ce tour. Si vous n'avez pas une carte correspondante, vous jouez ce que vous voulez\n\n- [Clique ici pour tout savoir.](https://lamap-bot.vercel.app/learn)"

    if update.message.chat.type == 'private':
        context.bot.send_message(update.message.chat_id, text=rules_text,
                                 parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)
    else:
        rules_cta = ("Ne t'affiches pas, vient me demander ça en solo.")
        context.bot.send_message(update.message.chat_id, text=rules_cta,
                                 parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)
        context.bot.send_message(update.message.from_user.id, text=rules_text,
                                 parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def tchoko(update, context):
    """Handler for the /tchoko command"""
    tchoko_text = (
        "Oh ma personne! Vient on gère...\n\n"
        "- Cause avec le [freeboy ci](https://t.me/panachaud), pour gérer par Mobile Money.\n"
        "- Ou alors, tu peux gérer [sur Paypal](https://www.paypal.me/DylanTientcheu) si tu as la rage\n\n"
        "Mais, saches que ce n'est pas une bière qui va donner des bonnes cartes..."
    )

    if update.message.chat.type == 'private':
        tchoko_text1 = (
            "Ah tu veux me donner une bière! Vient on gère...\n\n"
            "- Cause avec le [freeboy ci](https://t.me/panachaud), pour gérer par Mobile Money.\n"
            "- Ou alors, tu peux gérer [sur Paypal](https://www.paypal.me/DylanTientcheu) si tu as la rage\n\n"
            "Mais, saches que ce n'est pas une bière qui va donner des bonnes cartes..."
        )
        context.bot.send_message(update.message.chat_id, text=tchoko_text1,
                                 parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)
    else:
        tchoko_texto = "En vrai? Vient on gère en solo..."
        context.bot.send_message(update.message.chat_id, text=tchoko_texto,
                                 parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)
        context.bot.send_message(update.message.from_user.id, text=tchoko_text,
                                 parse_mode=ParseMode.MARKDOWN)


@db_session
def stats(update, context):
    if update.message.reply_to_message is not None:
        user = update.message.reply_to_message.from_user
    else:
        user = update.message.from_user

    u = UserDB.get(id=user.id)

    if not u:
        UserDB(id=user.id, name=user.first_name)
        context.bot.send_message(
            update.message.chat_id, text=f"Ok {user.first_name}, je te connais maintenant.")
    else:
        ufinished = u.games_played - (u.wins + u.losses)
        # update name
        u.name = user.first_name

        if u.games_played != 0:
            w_pct = " (" + str(round(100 * float(u.wins) /
                                     float(u.games_played), 1)) + "%" + ")"
            l_pct = " (" + str(round(100 * float(u.losses) /
                                     float(u.games_played), 1)) + "%" + ")"
            ufinished_pct = " (" + str(round(100 * float(ufinished) /
                                             float(u.games_played), 1)) + "%" + ")"
        else:
            w_pct = " (0%)"
            l_pct = " (0%)"
            ufinished = 0
            ufinished_pct = " (0%)"

        stats_txt = (
            f"`{n_format(u.nkap):<3}`    {mention(user)}"
            f"\n\n`{u.games_played:<3}`    {'Parties jouées'}"
            f"\n`{u.wins:<3}`    {'Parties gagnées'+w_pct}"
            f"\n`{u.losses:<3}`    {'Parties perdues'+l_pct}"
            f"\n`{ufinished:<3}`    {'Non terminées'+ufinished_pct}"
            f"\n`{u.wins_kora:<3}`    {'Kora donnés'}"
            f"\n`{u.losses_kora:<3}`    {'Kora reçus'}"
            f"\n\n`{u.points:<3}`    {'Points'}"
        )

        context.bot.send_message(
            update.message.chat_id, text=stats_txt, disable_web_page_preview=True)
        return


@db_session
def dm_information(chat, user, bot, result, points, bet, gains_losses):
    ''' DM player about his results '''
    title = chat.title
    text = ""
    if result == "L":
        text = (
            f"**PERDU**:\n\n{title}"
            f"\n\nMise: `{n_format(bet)}`"
            f"\nPertes: `{n_format(gains_losses)}`"
            f"\nPoints: `-{points}`"
        )
    if result == "W":
        text = (
            f"**GAGNÉ**:\n\n{title}"
            f"\n\nMise: `{n_format(bet)}`"
            f"\nGains: `+{n_format(gains_losses)}`"
            f"\nPoints: `+{points}`"
        )

    try:
        bot.send_message(user, text=text, disable_web_page_preview=True)
    except Exception:
        pass


@db_session
def top_players(update, context):
    top_10_players = list(UserDB.select().order_by(
        lambda u: desc(u.points))[:10])
    top_txt = []
    for idx, user in enumerate(top_10_players, start=1):
        string = f"`{idx}–` *{str(user.name)}* - {user.points} Points\n"
        top_txt.append(string)

    context.bot.send_message(update.message.chat_id, text=''.join(
        top_txt), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    return


@db_session
def top_pauvrards(update, context):
    top_10_poor = list(UserDB.select().order_by(
        lambda u: (u.nkap))[:10])
    top_txt = []
    for idx, user in enumerate(top_10_poor, start=1):
        string = f"`{idx}–` *{str(user.name)}* - {n_format(user.nkap)}\n"
        top_txt.append(string)

    context.bot.send_message(update.message.chat_id, text=''.join(top_txt),
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    return


@db_session
def top_rich_players(update, context):
    top_10_rich = list(UserDB.select().order_by(
        lambda u: desc(u.nkap))[:15])
    top_txt = []
    for idx, user in enumerate(top_10_rich, start=1):
        string = f"`{idx}–` *{str(user.name)}* - {n_format(user.nkap)}\n"
        top_txt.append(string)

    context.bot.send_message(update.message.chat_id, text=''.join(top_txt),
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    return


@db_session
def top_korateurs(update, context):
    top_kora(update, context)
    top_dbl_korateurs(update, context)


@db_session
def top_kora(update, context):
    top_10_korat = list(UserDB.select().order_by(
        lambda u: desc(u.wins_kora))[:10])
    top_txt = []
    for idx, user in enumerate(top_10_korat, start=1):
        string = f"`{idx}–` *{str(user.name)}* - {user.wins_kora}\n"
        top_txt.append(string)

    context.bot.send_message(update.message.chat_id, text='TOP KORATEURS\n\n' + ''.join(top_txt),
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    return


@db_session
def top_dbl_korateurs(update, context):
    top_10_db_korat = list(UserDB.select().order_by(
        lambda u: desc(u.wins_dbl_kora))[:10])
    top_txt = []
    for idx, user in enumerate(top_10_db_korat, start=1):
        string = f"`{idx}–` *{user.name}* - {user.wins_dbl_kora}\n"
        top_txt.append(string)

    context.bot.send_message(update.message.chat_id, text='DOUBLE KORATEURS\n\n' + ''.join(top_txt),
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@db_session
def transfert(update: Updater, context:  CallbackContext):
    cheaters = list(UserDB.select(lambda u: u.verified == False))
    if update.message.reply_to_message is not None:
        try:
            amount = int(context.args[0].replace(" ", ""))

            sender = update.message.from_user
            reciever = update.message.reply_to_message.from_user

            if sender.id in cheaters or reciever.id in cheaters:
                s = UserDB.get(id=sender.id)
                r = UserDB.get(id=reciever.id)

                if not s or not r or sender.id == reciever.id or amount < 0:
                    context.bot.send_message(
                        update.message.chat_id, text="Je ne fais pas la magie, Il y a eu un problème pendant ce transfert.")
                else:
                    if reciever.id not in BOTS:
                        if s.nkap > amount:
                            s.nkap -= amount
                            r.nkap += amount
                            context.bot.send_message(
                                update.message.chat_id, text=f"Confiance ! Tu as envoyé {n_format(amount)} à {mention(reciever)}.")
                            logger.info(
                                f"TRANSFERT from {sender.id} to {reciever.id} of {amount}")
                        else:
                            context.bot.send_message(
                                update.message.chat_id, text="Molah, doucement !.")
                    else:
                        context.bot.send_message(
                            update.message.chat_id, text="Fais attention à qui tu envoi tes dos, si je prends ça je garde.")
            else:
                context.bot.send_message(
                    update.message.chat_id, text="Désolé je ne peux pas gérer le transfert ci, il y a au moins un fraudeur parmis vous.\n\nSi vous pensez que cette affirmation est fausse, écrivez nous dans @lamapsupport")
        except ValueError:
            context.bot.send_message(
                update.message.chat_id, text="Je ne comprends pas le montant là, éssayes un vrai montant.")
        except IndexError:
            context.bot.send_message(
                update.message.chat_id, text="Je ne comprends pas désolé.")
    else:
        context.bot.send_message(
            update.message.chat_id, text="Renvoi moi cette commande en repondant à un autre message.")


@db_session
def le_retour(update: Updater, context:  CallbackContext):
    if update.message.reply_to_message is not None:
        if update.message.from_user.id in SUPERMOD_LIST:
            try:
                reciever = update.message.reply_to_message.from_user
                amount = int(context.args[0].replace(" ", ""))
                r = UserDB.get(id=reciever.id)
                r.nkap -= amount
                context.bot.send_message(
                    update.message.chat_id, text=f"C'est bon, le retour est géré.\n\n{mention(reciever)} a payé {n_format(amount)}")
                logger.info(
                    f"RETOUR from {reciever.id} of {amount}")
            except (ValueError, IndexError):
                context.bot.send_message(
                    update.message.chat_id, text="Je ne comprends pas bien boss.")
        else:
            context.bot.send_message(
                update.message.chat_id, text="Ca ne pourra jamais te concerner.")


@db_session
def verify(update: Updater, context:  CallbackContext):
    if update.message.reply_to_message is not None:
        if update.message.from_user.id in SUPERMOD_LIST:
            try:
                reciever = update.message.reply_to_message.from_user
                r = UserDB.get(id=reciever.id)
                r.verified = True
                context.bot.send_message(
                    update.message.chat_id, text=f"C'est bon, ta personne peut jouer dans mon terre")
                logger.info(
                    f"AUTH {reciever.id}")
            except (ValueError, IndexError):
                context.bot.send_message(
                    update.message.chat_id, text="Je ne comprends pas bien boss.")
        else:
            context.bot.send_message(
                update.message.chat_id, text="Ca ne pourra jamais te concerner.")


@db_session
def unverify(update: Updater, context:  CallbackContext):
    if update.message.reply_to_message is not None:
        if update.message.from_user.id in SUPERMOD_LIST:
            try:
                reciever = update.message.reply_to_message.from_user
                r = UserDB.get(id=reciever.id)
                r.verified = False
                context.bot.send_message(
                    update.message.chat_id, text=f"Ah bon? Il triche? Il va lire l'heure...")
                logger.info(
                    f"DE-AUTH {reciever.id}")
            except (ValueError, IndexError):
                context.bot.send_message(
                    update.message.chat_id, text="Je ne comprends pas bien boss.")
        else:
            context.bot.send_message(
                update.message.chat_id, text="Ca ne pourra jamais te concerner.")


@db_session
def status_check(update: Updater, context:  CallbackContext):
    if update.message.reply_to_message is not None:
        if update.message.from_user.id in SUPERMOD_LIST:
            try:
                reciever = update.message.reply_to_message.from_user
                r = UserDB.get(id=reciever.id)
                context.bot.send_message(
                    update.message.chat_id, text=f"ID: {r.id}\nNM: {r.name}\nNK: {r.nkap}\nVF: {r.verified}")
            except (ValueError, IndexError):
                context.bot.send_message(
                    update.message.chat_id, text="Je ne comprends pas bien boss.")
        else:
            context.bot.send_message(
                update.message.chat_id, text="Ca ne pourra jamais te concerner.")


@db_session
def remboursement(update: Updater, context:  CallbackContext):
    if update.message.reply_to_message is not None:
        if update.message.from_user.id in SUPERMOD_LIST:
            try:
                reciever = update.message.reply_to_message.from_user
                amount = int(context.args[0].replace(" ", ""))
                r = UserDB.get(id=reciever.id)
                r.nkap += amount
                context.bot.send_message(
                    update.message.chat_id, text=f"La paie a été éffectué.\n\n{mention(reciever)} est payé {n_format(amount)}")
                logger.info(
                    f"REMBOURSEMENT to {reciever.id} of {amount}")

            except (ValueError, IndexError):
                context.bot.send_message(
                    update.message.chat_id, text="Je ne comprends pas bien boss.")
        else:
            context.bot.send_message(
                update.message.chat_id, text="Ca ne pourra jamais te concerner.")


def register():
    dispatcher.add_handler(CommandHandler(
        'apprendre', apprendre))
    dispatcher.add_handler(CommandHandler('tchoko', tchoko))
    dispatcher.add_handler(CommandHandler(
        'top10', top_players))
    dispatcher.add_handler(CommandHandler(
        'top_nkap', top_rich_players))
    dispatcher.add_handler(CommandHandler(
        'top_koras', top_korateurs))
    dispatcher.add_handler(CommandHandler(
        'top_pauvrard', top_pauvrards))
    dispatcher.add_handler(CommandHandler(
        'transfert', transfert))
    dispatcher.add_handler(CommandHandler(
        'retour', le_retour))
    dispatcher.add_handler(CommandHandler(
        'verify', verify))
    dispatcher.add_handler(CommandHandler(
        'unverify', unverify))
    dispatcher.add_handler(CommandHandler(
        'deepcheck', status_check))
    dispatcher.add_handler(CommandHandler(
        'remboursement', remboursement))
    dispatcher.add_handler(CommandHandler('stats', stats))
    dispatcher.add_handler(CommandHandler('start', start))
