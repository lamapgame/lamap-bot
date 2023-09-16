from datetime import datetime

from telegram import User
from random import shuffle


class Deck:
  def __init__(self):
    self.cards = []

  def shuffle(self):
    shuffle(self.cards)
