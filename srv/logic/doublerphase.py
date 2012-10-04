#!/usr/bin/python

from srv.phase import Phase
from srv.variable import Variable

class DoublerPhase(Phase):

	def __init__(self, doubledaccount):
		self.doubledaccount = doubledaccount
		Variable("betcolor", 101, enumdict = {0:'red', 1:'black'})
		Variable("outcolor", 102, enumdict = {0:'red', 1:'black'})
		Variable("doubledamount", 103, minmax = (0, 1000))
		self.accounts = [doubledaccount]
		self.inputs = ["betcolor"]
		self.outputs = ["outcolor", "doubledamount"]
		Phase.__init__(self)

	def play(self, state):
		state.outcolor = random.randint(0, 1)
		if state.outcolor == state.betcolor:
			state[self.doubledaccount] *= 2 
		else:
			state[self.doubledaccount] = 0
		state.doubledamount = state[self.doubledaccount]

	def validate(self, state):
		return state[self.doubledaccount] > 0

