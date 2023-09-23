from random import shuffle


class Card:
    def __init__(self) -> None:
        self.suit = ""
        self.value = 0


class Deck:
    def __init__(self):
        self.cards: list[Card] = []

    def shuffle(self):
        shuffle(self.cards)
