from telegram import InlineQueryResultArticle, ParseMode,  InputTextMessageContent, \
    InlineQueryResultCachedSticker as Sticker
import card as c
from utils import mention, n_format
from uuid import uuid4
from collections import Counter


def add_card(game, card, results, can_play):
    """Add an option that represents a card"""

    if can_play:
        results.append(
            Sticker(str(card), sticker_file_id=c.STICKERS[str(card)])
        )
    else:
        ''' results.append(
            Sticker(str(uuid4()), sticker_file_id=c.STICKERS_GREY[str(card)],
                    input_message_content=game_info(game))
        ) '''
        results.append(
            Sticker(str(uuid4()), sticker_file_id=c.STICKERS[str(card)],
                    input_message_content=game_info(game))
        )


def add_special_card(game, special, results, can_play):
    """ Add special quick win options """
    results.append(
        Sticker(str(special), sticker_file_id=c.STICKERS[str(special)])
    )


def check_quick_win(cards):
    my_cards = [c.from_str(acard) for acard in cards]
    suits = [s.suit for s in my_cards]
    values = [int(i.value) for i in my_cards]
    val_counter = Counter(values)
    total_value = sum(values)

    # check x_21
    if total_value <= 21:
        return 'x_21'
    # check x_333
    elif values.count(3) >= 3:
        return 'x_333'
    # check x_777
    elif values.count(7) >= 3:
        return 'x_777'
    # check carre-daxe
    elif len(set(suits)) == 1:
        return 'x_0'
    # check x_0
    elif val_counter.most_common(1)[0][1] >= 4:
        return 'x_5555'

    return None


def player_list(game):
    """ Generate a list of players """
    return [player.user.name + "(" + str(len(player.cards)) + "carte(s))" for player in game.players]


def add_no_game(results):
    """Add text result if user is not playing"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title="Vous ne jouez pas",
            input_message_content=InputTextMessageContent("Vous n'êtes dans aucune partie actuellement, veuillez commencer une nouvelle avec /nkap ou rejoignez une lancé."))
    )


def add_not_started(results):
    """Add text result if the game has not started yet"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title="Le jeu n'a pas encore commencé",
            input_message_content=InputTextMessageContent(
                'Commencez la partie')
        )
    )


def game_info(game):
    players = player_list(game)
    name = mention(game.current_player.user)
    card = repr(game.last_card)
    controlling_card = "Aucune carte"
    controlling_player = "Aucun joueur"

    if game.control_player is not None:
        controlling_player = mention(game.control_player.user)
        controlling_card = repr(game.control_card)

    if controlling_card is None:
        return InputTextMessageContent(f"🤙🏾 - {controlling_player}", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    else:
        return InputTextMessageContent(f"🤴🏾: {controlling_card} - {controlling_player}", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def get_game_status(game):
    ''' Get the current status of the game played '''
    status_txt = [f"`Mise: {n_format(game.bet)}`\n\n"]

    for idx, round in enumerate(game.game_info, start=1):
        string = f"`Tour {idx}:` **{mention(round['control_player'].user)}** - **{repr(round['control_card'])}**\n"
        status_txt.append(string)

    return ''.join(status_txt)


def get_end_game_status(game):
    end_game_txt = []

    for player in game.game_players:
        string = f"{player.user.first_name}: "
        for card in player.cards:
            p_card = repr(c.from_str(card))
            string += f" - {p_card}"
        string += "\n"
        end_game_txt.append(string)

    return "".join(end_game_txt)
