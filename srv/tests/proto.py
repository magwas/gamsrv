#!/usr/bin/python

import unittest

import socket
import struct
import sys

from srv.proto import Proto

from srv.config import listenaddress
from srv.listener import Listener

class MockValidator:
	def validateKeyValue(self,phs,key,value):
		return True
	def validateHeader(self,pktid,seq,phs,ne):
		return True
	def validateTokenLen(self,tokenlen):
		return True
	def validateToken(self,tokenlen):
		return True

class TestProto(unittest.TestCase):

	def callback(self,socket,address):
		p = Proto()
		validator = MockValidator()
		result = p.decode(socket,validator)
		vals=result[2]
		vals[42]=result[1]
		p.encode(socket,result[0],vals).encode('hex')
		socket.close()

	def test_proto(self):
		c = Listener(listenaddress,self.callback)
		self.c = c
		c.loop()
		s = socket.socket()
		s.connect(listenaddress)
		buf=struct.pack("!IIIHHHiHiH",0xdeadbeef,1,2,3,2,5,9,6,10,0)
		sys.stdout.flush()
		s.sendall(buf)
		res = s.recv(28)
		self.assertEqual(res,'\xde\xad\xbe\xef\x00\x00\x00\x02\x00\x03\x00*\x00\x00\x00\x03\x00\x05\x00\x00\x00\t\x00\x06\x00\x00\x00\n')
		c.shutdown()

	def tearDown(self):
		self.c.shutdown()

if __name__ == '__main__':
	unittest.main()

