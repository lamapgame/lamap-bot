from __future__ import annotations

from datetime import datetime
from typing import Any

from telegram import User


class Player:
    """A player already in a game"""

    def __init__(self, user: User):
        self.id = user.id
        self.user = user
        self.is_ai = False
        # the player will pay kora if is_koratable is True
        self.is_koratable = True
        self.is_controller = False

        # money lost or won, (negative if lost)
        self.nkap = 0

        self.hand_of_cards: list[Any] = []
        self.turn_started_time = datetime.now()

    def __eq__(self, p: object) -> bool:
        if not isinstance(p, Player):
            return NotImplemented
        return str(object=self.id) == str(p.id)
