#!/usr/bin/python

import unittest

import socket

from srv.config import listenaddress
from srv.listener import Listener

class TestListener(unittest.TestCase):

	def callback(self,socket,address):
		s = socket.makefile()
		d = s.read(4)
		s.write(d)
		s.close()

	def test_listener(self):
		c = Listener(listenaddress,self.callback)
		self.c = c
		c.loop()
		s = socket.socket()
		s.connect(listenaddress)
		f=s.makefile()
		f.write("abcd")
		f.flush()
		d=f.read(4)
		self.assertEqual("abcd",d)
		c.shutdown()

	def tearDown(self):
		self.c.shutdown()

if __name__ == '__main__':
	unittest.main()

