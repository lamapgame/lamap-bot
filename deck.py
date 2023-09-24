from random import shuffle


class Card:
    def __init__(self, suit, value) -> None:
        self.suit = suit
        self.value = value


class Deck:
    def __init__(self):
        self.cards: list[Card] = []

    def shuffle_cards(self):
        shuffle(self.cards)
