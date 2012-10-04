#!/usr/bin/python

import unittest

from persistence.state import State

class TestListener(unittest.TestCase):

	def test_state(self):
		state = State("test")
		state.set("foo",3)
		foo=state.get("foo")
		self.assertEqual(foo,3)

if __name__ == '__main__':
	unittest.main()

