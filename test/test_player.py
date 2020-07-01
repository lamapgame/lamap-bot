import unittest

from game import Game
from player import Player
import card as c
import deck as d


class Test(unittest.TestCase):

    game = None

    def setUp(self):
        self.game = Game(None)

    def test_insert(self):
        p0 = Player(self.game, "Player 0")
        p1 = Player(self.game, "Player 1")
        p2 = Player(self.game, "Player 2")

        self.assertEqual(p0, p2.next)
        self.assertEqual(p1, p0.next)
        self.assertEqual(p2, p1.next)

        self.assertEqual(p0.prev, p2)
        self.assertEqual(p1.prev, p0)
        self.assertEqual(p2.prev, p1)

    def test_leave(self):
        p0 = Player(self.game, "Player 0")
        p1 = Player(self.game, "Player 1")
        p2 = Player(self.game, "Player 2")

        p1.leave()

        self.assertEqual(p0, p2.next)
        self.assertEqual(p2, p0.next)

    def test_playable_cards_w_control(self):
        p = Player(self.game, "Player 0")
        self.game.control_card = c.Card('h', '5')
        p.cards = ['h_3', 'h_6', 's_8', 'd_5', 'c_8']
        expected = ['h_3', 'h_6']

        self.assertListEqual(p.playable_cards(), expected)

    def test_playable_cards_no_control(self):
        p = Player(self.game, "Player 0")
        self.game.last_card = 'h_5'
        p.cards = ['h_3', 'h_6', 's_8', 'd_5', 'c_8']
        expected = ['h_3', 'h_6', 's_8', 'd_5', 'c_8']

        self.assertListEqual(p.playable_cards(), expected)
