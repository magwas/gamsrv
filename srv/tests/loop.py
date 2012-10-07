#!/usr/bin/python

import unittest

import socket
import struct
import sys

from srv.proto import Proto

from srv.config import listenaddress
from srv.listener import Listener
from srv.registry import registry

from srv.inout.inout import InOut
from srv.terminalstate import TerminalState
from logic.dice import Dice



InOut()
Dice()

class TestLoop(unittest.TestCase):

	def callback(self,socket,address):
		p = Proto()
		ts = TerminalState(1)
		seq,gam,phs,vals,token = p.decode(socket,ts)
		game = registry.getGameById(gam)
		if not phs in game.phaseids:
			raise ValueError
		phase = registry.getPhaseById(phs)
		state = ts.phaseinit(game,phase,vals)
		if phase.validate(state):
			phase.play(state)
			outstate = ts.afterphase(game,phase,state)
		p.encode(socket,seq,outstate)
		print outstate
		socket.close()

	def test_loop(self):
		c = Listener(listenaddress,self.callback)
		self.c = c
		c.loop()
		s = socket.socket()
		s.connect(listenaddress)
		buf=struct.pack("!IIIHHHHiHiHiHiH",0xdeadbeef,1,2,1,13,4,132,0,133,0,134,0,135,10,0)
		sys.stdout.flush()
		s.sendall(buf)
		res = s.recv(28)
		self.assertEqual(res[:13],'\xde\xad\xbe\xef\x00\x00\x00\x02\x00\x04\x00\x88\x00')
		c.shutdown()

	def tearDown(self):
		self.c.shutdown()

if __name__ == '__main__':
	unittest.main()

