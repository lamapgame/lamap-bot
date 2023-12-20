from test import mock_objects
from deck import Deck, Card
from player import Player


def test_card_initialization():
    """Test that a card is initialized with the correct attributes."""
    card = Card("h", 5, "GALACTIC")
    assert card.suit == "h"
    assert card.value == 5
    assert card.design == "GALACTIC"
    assert card.icon == "♥️"


def test_deck_shuffling():
    """Test that the deck is shuffled."""
    deck1 = Deck()
    deck2 = Deck()
    # There's a small chance this could fail due to randomness
    assert deck1.cards != deck2.cards


def test_special_card_computation():
    """Test computation of special cards based on a hand."""
    deck = Deck()
    hand = [Card("h", 3, "DEFAULT"), Card("d", 3, "DEFAULT"), Card("s", 3, "DEFAULT")]
    special_cards = deck.compute_cards(hand)
    assert Card("x", 333, "DEFAULT") in special_cards


def test_card_comparison():
    """Test the comparison of two cards."""
    card1 = Card("h", 5, "DEFAULT")
    card2 = Card("h", 6, "DEFAULT")
    assert Card.is_better_than(card2, card1)


def test_cut_cards_with_special():
    """Test deck cutting cards including special card computation."""
    deck = Deck()
    player = Player(mock_objects.user1)
    deck.cut_cards(player)
    assert len(player.hand_of_cards) >= 5


def test_card_equality_and_string():
    """Test card equality and string representation."""
    card1 = Card("h", 5, "DEFAULT")
    card2 = Card("h", 5, "DEFAULT")
    card3 = Card("d", 5, "DEFAULT")
    assert card1 == card2
    assert card1 != card3
    assert str(card1) == "h_5"
