class GameDoesntExistError(Exception):
    """is thrown when there's no game in a chat"""


class GameAlreadyExistError(Exception):
    """is thrown when there's already a game in a chat"""


class CannotTransferToUnknownPlayerError(Exception):
    """is thrown when a player tries to transfer money to an unknown player"""


class CannotTransferToSelfError(Exception):
    """is thrown when a player tries to transfer money to themselves"""


class CannotTransferToBotError(Exception):
    """is thrown when a player tries to transfer money to the bot"""


class PlayerRemovedBeforeGameStart(Exception):
    """is thrown when a player is removed before the game starts"""


class CannotTransferToBannedError(Exception):
    """is thrown when a player tries to transfer money to a banned player"""


class NotEnoughNkapError(Exception):
    """is thrown when a user doesn't have enough nkap for an operation"""


class NotEnoughPlayersError(Exception):
    """is thrown when the number of players is less than the max number of players"""


class PlayerAlreadyInGameError(Exception):
    """is thrown when a player is already in a game"""


class PlayerIsBanned(Exception):
    """is thrown when a player is banned from the bot"""


class PlayerIsPoor(Exception):
    """is thrown when a player doesn't have enough money bot"""


class PlayerNotInGameError(Exception):
    """is thrown when a player is not in a game"""


class TooManyPlayersError(Exception):
    """is thrown when the number of players exceeds the max number of players"""


class NotVerifiedError(Exception):
    """is thrown when a user is not verified or banned"""


class LobbyClosedError(Exception):
    """is thrown when a game lobby has been closed"""


class DeckEmptyError(Exception):
    """a rare issue where the deck is empty"""


class DifferentSuitError(Exception):
    """is thrown when a player tries to play a card of a different suit"""


class UserIsBanned(Exception):
    """is thrown when a player is banned from the bot"""


class CannotRemoveControllerError(Exception):
    """is thrown when a player tries to remove the current controller"""


class CannotRemoveLastPlayer(Exception):
    """is thrown when a player tries to remove the current controller"""
