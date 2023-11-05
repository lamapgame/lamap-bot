from __future__ import annotations

from datetime import datetime
from typing import Any

from telegram import User


class Player:
    def __init__(self, user: User):
        self.id = user.id
        self.user = user
        self.is_AI = False
        self.is_controller = False

        self.hand_of_cards: list[Any] = []
        self.turn_started_time = datetime.now()

    def __eq__(self, p: object) -> bool:
        if not isinstance(p, Player):
            return NotImplemented
        return str(object=self.id) == str(p.id)
