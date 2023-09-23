from datetime import datetime

from telegram import User


class Player:
    def __init__(self, user: User, score: int):
        self.user = user
        self.hand_of_cards = []
        self.turn_started_time = datetime.now()
