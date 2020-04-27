class NoGameInChatError(Exception):
    pass


class AlreadyJoinedError(Exception):
    pass


class LobbyClosedError(Exception):
    pass


class NotEnoughPlayersError(Exception):
    pass


class DeckEmptyError(Exception):
    pass
