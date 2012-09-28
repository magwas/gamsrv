#!/usr/bin/python

import unittest

from client.conn import Connection

class TestLogin(unittest.TestCase):

	def test_login(self):
		c = Connection()
		conn = c.Login()
		self.assertTrue(conn)

if __name__ == '__main__':
	unittest.main()

