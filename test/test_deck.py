import pytest
from deck import Deck, Card
from player import Player
from test import mock_objects


def test_deck_initialization():
    deck = Deck()
    assert isinstance(deck.cards, list)
    assert len(deck.cards) >= 31
    assert all(isinstance(card, Card) for card in deck.cards)


def test_deck_shuffle():
    deck = Deck()
    original_cards = deck.cards.copy()
    deck.shuffle_cards()
    assert deck.cards != original_cards


def test_deck_cut():
    deck = Deck()
    player = Player(mock_objects.user1)
    deck.cut_cards(player)
    assert len(player.hand_of_cards) == 5
    assert all(isinstance(card, Card) for card in player.hand_of_cards)
    assert all(card not in deck.cards for card in player.hand_of_cards)
