#!/usr/bin/python

import unittest

from srv.registry import Registry
from logic.dice import Dice
from srv.inout.inout import InOut

class TestGame(unittest.TestCase):

	def test_game(self):
		gi = Registry()
		d = Dice()
		i = InOut()
		self.assertEquals(gi.getGameByNumber(0), i)
		dice = gi.getGameByName("dice")
		self.assertEqual(dice, gi.getGameByNumber(1))

if __name__ == '__main__':
	unittest.main()

