#!/usr/bin/python

from xml.dom.minidom import Element
from lib.singleton import Singleton
from persistence.enumtype import EnumType
from srv import log

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
		log.log(log.LOG_INFO,"registergame", "srv/registry", name,idnum=idnum)

	def getGameByName(self, name):
		return self.games[self.gameregistry.intFor(name)]

	def getGameById(self, idnum):
		return self.games[idnum]

	def registerPhase(self, phase):
		name = phase.getName()
		idnum = phase.getId()
		self.phases[idnum] = phase
		self.phaseregistry.registerOne(name, idnum)
		log.log(log.LOG_INFO,"registerphase", "srv/registry", name,idnum=idnum)

	def getPhaseByName(self, name):
		return self.phases[self.phaseregistry.intFor(name)]

	def getPhaseById(self, idnum):
		return self.phases[idnum]

	def registerVariable(self, variable):
		name = variable.getName()
		idnum = variable.getId()
		self.variables[idnum] = variable
		self.variableregistry.registerOne(name,idnum)
		log.log(log.LOG_INFO,"registervariable", "srv/registry", name,idnum=idnum)

	def getVariableByName(self, name):
		log.debug("registry",6,name=name)
		return self.variables[self.variableregistry.intFor(name)]

	def getVariableById(self, idnum):
		return self.variables[idnum]

	def toDom(self):
		r = Element("registry")
		r.appendChild(self.gameregistry.toDom())
		r.appendChild(self.phaseregistry.toDom())
		r.appendChild(self.variableregistry.toDom())
		for game in self.games.values():
			r.appendChild(game.toDom())
		return r

