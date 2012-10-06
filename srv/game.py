#!/usr/bin/python

from xml.dom.minidom import Element
from lib.ifaced import Ifaced
from persistence.state import State
from srv.registry import Registry

class Game(Ifaced,State):
	"""
	The game defines how the phases can follow each other.
	The init of  agame should define the state machine
	"""
	def __init__(self):
		r = Registry()
		r.registerGame(self)
		self.phases = []
		self.phaseids = []
		for phasename in self.statemachine.keys():
			game = r.getPhaseByName(phasename)
			self.phases.append(game)
			self.phaseids.append(game.getId())
		State.__init__(self,self._name)
		self.addOrSame("name",self.getName())
		self.addOrSame("id",self.getId())
		self.addOrSame("phases",sorted(self.phaseids))

	def alwaysValidPhase(self):
		return True

	def toDom(self):
		r = Registry() # making it an attribute in init would not be much cheaper
		ret = Element("game")
		ret.setAttribute("name",self.getName())
		for phase in self.phases:
			ret.appendChild(phase.toDom())
		return ret
		

