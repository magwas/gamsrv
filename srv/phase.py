#!/usr/bin/python

from lib.ifaced import Ifaced
from srv.registry import Registry

class Phase(Ifaced):

	def __init__(self):
		r = Registry()
		r.registerPhase(self)

	#virtual
	def play(self, state):
		raise NotImplementedError

	#virtual
	def validate(self, state):
		raise NotImplementedError

