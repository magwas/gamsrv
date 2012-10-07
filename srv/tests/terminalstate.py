#!/usr/bin/python

import unittest

from persistence.state import State
from lib import log
from logic.dice import Dice
from srv.config import testloops
from srv.registry import registry
from srv.inout.inout import InOut
from srv.terminalstate import TerminalState

from xml.dom.minidom import parseString

class TestTerminalState(unittest.TestCase):

	def setUp(self):
		InOut()
		Dice()

	def test_terminalplay(self):
		dicephase = registry.getPhaseByName("dice")
		dicegame = registry.getGameByName("dice")
		withdrawphase = registry.getPhaseByName("dicewithdraw")
		inoutgame = registry.getGameByName("inout")
		inoutphase = registry.getPhaseByName("inout")
		terminal = State("terminal/1")
		terminal.set("enabled",True)
		terminal.set("gameenabled/%s"%dicegame.getId(),True)
		terminal.set("gameenabled/%s"%inoutgame.getId(),True)
		terminal.set("accounts/credit",100)
		t = TerminalState(1)
		n = 0
		while n < testloops:
			n += 1
			input = {135:10, 132:0, 133:0,134:0}
			state = t.phaseinit(dicegame,dicephase,input)
			if not dicephase.validate(state):
				inputadd = {2:100,1:0}
				statein = t.phaseinit(inoutgame,inoutphase,inputadd)
				inoutphase.play(statein)
				outstate = t.afterphase(inoutgame,inoutphase,statein)
			state = t.phaseinit(dicegame,dicephase,input)
			dicephase.play(state)
			outstate = t.afterphase(dicegame,dicephase,state)
			if outstate[131] > 20:
				#withdraw
				input = {131:outstate[131]}
				state = t.phaseinit(dicegame,withdrawphase,input)
				withdrawphase.play(state)
				outstate = t.afterphase(dicegame,withdrawphase,state)
				
			
				

if __name__ == '__main__':
	unittest.main()

