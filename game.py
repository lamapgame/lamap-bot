from datetime import datetime

from deck import Deck


class Game:
  def __init__(self, chat_id: str):
    self.chat_id = chat_id
    self.startedDate = datetime.now()
    self.players = []
    self.deck = Deck() # TODO: implement deck of cards (see deck.py) -> dylantientcheu/lamap-bot/deck.py and dylantientcheu/lamap-bot/card.py

    # add various game options here (number of players, koras, or more configuration options)
    self.max_player_number = 4
    self.has_quick_wins = True
    self.has_koras = True
    self.has_dbl_koras = True

