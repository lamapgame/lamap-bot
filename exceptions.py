class GameDoesntExistError(Exception):
  """is thrown when there's no game in a chat"""

class GameAlreadyExistError(Exception):
  """is thrown when there's already a game in a chat"""
  pass

class NotEnoughNkapError(Exception):
  """is thrown when a user doesn't have enough nkap for an operation"""
  pass

class NotVerifiedError(Exception):
  """is thrown when a user is not verified or banned"""
  pass

class LobbyClosedError(Exception):
  """is thrown when a game lobby has been closed"""
  pass

class NotEnoughPlayersError(Exception):
  """is thrown when a game is about to start but there's not enough players"""
  pass

class DeckEmptyError(Exception):
  """a rare issue where the deck is empty"""
  pass

class DifferentSuitError(Exception):
  """is thrown when a player tries to play a card of a different suit"""
  pass