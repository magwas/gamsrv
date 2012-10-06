#!/usr/bin/python

from lib.singleton import Singleton
from srv.game import Game
from srv.phase import Phase
from srv.variable import Variable

class InOutPhase(Phase, Singleton):

	_name = "inout"
	_idnum = 0

	def __init__(self):
		if None is getattr(self,"accounts",None):
			Variable("inmoney", 2, minmax = [0, 1000])
			Variable("outmoney", 1, minmax = [0, 1000])
			self.accounts = ["credit"]
			self.inputs = ["inmoney", "outmoney"]
			self.outputs = ["credit"]
			Phase.__init__(self)

	def play(self, state ):
		state.credit += state.inmoney - state.outmoney

	def validate(self, state):
		return state.credit > state.out

class InOut(Game, Singleton):
	_name = "inout"
	_idnum = 0

	def __init__(self):
		if None is getattr(self,"statemachine",None):
			Variable("credit", 0, ispersistent = True, minmax = [0, 1000])
			InOutPhase()
			self.statemachine = {
				"inout":
					[("inout", self.alwaysValidPhase)]
			}
			Game.__init__(self)

InOut()

