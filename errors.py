class NoGameInChatError(Exception):
    pass


class MaxPlayersReached(Exception):
    pass


class AlreadyJoinedError(Exception):
    pass


class GameAlreadyStartedError(Exception):
    pass


class AlreadyGameInChat(Exception):
    pass


class NotEnoughNkap(Exception):
    pass

class NotVerifiedError(Exception):
    pass


class LobbyClosedError(Exception):
    pass


class NotEnoughPlayersError(Exception):
    pass


class DeckEmptyError(Exception):
    pass


class DifferentSuitError(Exception):
    pass
