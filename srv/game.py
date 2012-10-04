#!/usr/bin/python

from lib.ifaced import Ifaced
from srv.registry import Registry

class Game(Ifaced):
	def __init__(self):
		r = Registry()
		r.registerGame(self)

	def alwaysValidPhase(self):
		return True

