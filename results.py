from telegram import InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultCachedSticker as Sticker
import card as c
from uuid import uuid4


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


def add_other_cards(player, results, game):
    """Add hand cards when choosing suit"""

    results.append(
        InlineQueryResultArticle(
            "hand",
            title=_("Card (tap for game state):",
                    "Cards (tap for game state):",
                    len(player.cards)),
            description=', '.join([repr(card) for card in player.cards]),
            input_message_content=game_info(game)
        )
    )


def player_list(game):
    """ Generate a list of players """
    return [player.user.name + "(" + str(len(player.cards)) + "carte(s))" for player in game.players]


def add_no_game(results):
    """Add text result if user is not playing"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title="Vous ne jouez pas",
            input_message_content=InputTextMessageContent("Vous n'êtes dans aucune partie actuellement, veuiller commencer une nouvelle avec /new_game ou rejoignez une en cours dans ce groupe avec /join."))
    )


def add_not_started(results):
    """Add text result if the game has not started yet"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title="Le jeu n'a pas encore commencer",
            input_message_content=InputTextMessageContent(
                'Start the game with / start')
        )
    )


def who_controls(game):
    """ Determines who controls the game """
    return None


def game_info(game):
    players = player_list(game)
    name = game.current_player.user.name
    card = repr(game.last_card)
    controller = {"card": game.control_card, "player": game.control_player}

    return InputTextMessageContent(f"Joueur actuel: {name} \nDernière carte: {card}" + "\n\nJoueurs:\n" + "\n".join(players))
    """ return InputTextMessageContent(f"Joueur actuel: {name} \nDernière carte: {card} \nContrôle 🤴🏾: {controller.player.name} - {controller.card}") """
