#!/usr/bin/python

from lib.singleton import Singleton
from persistence.enumtype import EnumType

class Registry(Singleton):

	def __init__(self):
		if None is getattr(self,"gameregistry",None):
			self.gameregistry = EnumType("games", incremental = True)
			self.phaseregistry = EnumType("phases", incremental = True)
			self.variableregistry = EnumType("variables", incremental = True)
			self.games = {}
			self.phases = {}
			self.variables = {}

	def registerGame(self, game):
		name = game.getName()
		idnum = game.getId()
		self.games[idnum] = game
		self.gameregistry.registerOne(name, idnum)

	def getGameByName(self, name):
		return self.games[self.gameregistry.intFor(name)]

	def getGameByNumber(self, idnum):
		return self.games[idnum]

	def registerPhase(self, phase):
		name = phase.getName()
		idnum = phase.getId()
		self.phases[idnum] = phase
		self.phaseregistry.registerOne(name, idnum)

	def getPhaseByName(self, name):
		return self.phases[self.phaseregistry.intFor(name)]

	def getPhaseByNumber(self, idnum):
		return self.phases[idnum]

	def registerVariable(self, variable):
		name = variable.getName()
		idnum = variable.getId()
		self.variables[idnum] = variable
		self.variableregistry.registerOne(name,idnum)

	def getVariableByName(self, name):
		return self.variables[self.variableregistry.intFor(name)]

	def getVariableByNumber(self, idnum):
		return self.variables[idnum]

	def todom(self):
		r = Element("registry")
		r.appendChild(self.gameregistry.todom())
		r.appendChild(self.phaseregistry.todom())
		r.appendChild(self.variableregistry.todom())
		return r

