#!/usr/bin/python

from srv.phase import Phase

class WithdrawPhase(Phase):
	def __init__(self, ingameaccount):
		self.ingameaccount = ingameaccount
		self.accounts = [ingameaccount]
		self.inputs = []
		self.outputs = ["credit"]
		Phase.__init__(self)

	def play(self,state):
		state.credit = state[self.ingameaccount]
		state[self.ingameaccount] = 0

	def validate(self,state):
		return True

