from datetime import datetime
from typing import Any

from telegram import User


class Player:
    def __init__(self, user: User):
        self.id = user.id
        self.user = user
        self.is_AI = False

        self.hand_of_cards: list[Any] = []
        self.turn_started_time = datetime.now()
