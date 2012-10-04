#!/usr/bin/python

from lib.singleton import Singleton
from srv.phase import Phase
from srv.game import Game
from srv.variable import Variable
from srv.logic.doublerphase import DoublerPhase
from srv.logic.withdrawphase import WithdrawPhase

class DiceDoubler(DoublerPhase,Singleton):
	_name = "dicedoubler"
	_idnum = 11
	def __init__(self):
		if None is getattr(self,"accounts",None):
			DoublerPhase.__init__(self, "diceingame")

class DiceWithdraw(WithdrawPhase, Singleton):
	_name = "dicewithdraw"
	_idnum = 12
	def __init__(self):
		if None is getattr(self,"accounts",None):
			WithdrawPhase.__init__(self, "diceingame")

class DicePhase(Phase,Singleton):

	_name = "dice"
	_idnum = 13

	def __init__(self):
		if None is getattr(self,"accounts",None):
			Variable("diceingame", 131, ispersistent = True, minmax = [0, 1000])
			Variable("holddice1", 132, minmax = [0, 1])
			Variable("holddice2", 133, minmax = [0, 1])
			Variable("holddice3", 134, minmax = [0, 1])
			Variable("bet", 135, enumdict = {10:"10", 20:"20", 30:"30"})
			Variable("dice1state", 136, ispersistent = True, minmax = [1, 6])
			Variable("dice2state", 137, ispersistent = True, minmax = [1, 6])
			Variable("dice3state", 138, ispersistent = True, minmax = [1, 6])
			self.accounts = ["diceingame"]
			self.inputs = ["bet", "holddice1", "holddice2", "holddice3"]
			self.outputs = ["dice1state", "dice2state", "dice3state", "diceingame"]
			Phase.__init__(self)

	def play(self, state):
		state.diceingame -= state.bet
		if not inputs.holddice1:
			state.dice1state = random.randint(1, 6)
		if not inputs.holddice1:
			state.dice1state = random.randint(1, 6)
		if not inputs.holddice1:
			state.dice1state = random.randint(1, 6)
		state.ingame += ((state.dice1state + state.dice2state + state.dice1state)*2 + 1 ) * state.bet / 22 # ((3.5*3)*2 +1)/22 = 1

	def validate(self, state):
		if state.ingame < state.bet:
			return False

class Dice(Game,Singleton):
	_name = "dice"
	_idnum = 1

	def __init__(self):
		if None is getattr(self,"statemachine",None):
			doubler = DiceDoubler()
			mainphase = DicePhase()
			withdraw = DiceWithdraw()
			self.statemachine = {
				"dice":
					[("dice", self.alwaysValidPhase),
					 ("dicedoubler", self.alwaysValidPhase),
					 ("dicewithdraw", self.alwaysValidPhase)],
				"dicedoubler":
					[("dicedoubler", self.alwaysValidPhase),
					 ("dicewithdraw", self.alwaysValidPhase)],
				"dicewithdraw":
					[("dice", self.alwaysValidPhase)],
			}
			Game.__init__(self)

