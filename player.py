from datetime import datetime

from telegram import User

from deck import Card


class Player:
    def __init__(self, user: User, score: int):
        self.user = user
        self.hand_of_cards: list[Card] = []
        self.turn_started_time = datetime.now()
