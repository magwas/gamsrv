#!/usr/bin/python

from persistence.state import State
from persistence.rangetype import RangeType
from persistence.enumtype import EnumType
from lib.ifaced import Ifaced
from srv.registry import Registry

class EnumVar(EnumType,Ifaced):
	pass

class RangeVar(RangeType,Ifaced):
	pass

class Variable(State, Ifaced):

	def __init__(self, name, number, ispersistent = False, enum = None, enumdict = None, cleanup = False, incremental = False, persistant = True, minmax = None):
		self._name = name
		self._idnum = number
		State.__init__(self, name)
		parent = self.get("type")
		if parent is None:
			if ((enum is not None) or (enumdict is not None)) and (minmax is None):
				parent = "enum"
			elif minmax is not None:
				parent = "range"
			else:
				raise ValueError("invalid combination of args")

		if parent == "enum":
			self.__class__ = EnumVar
			EnumType.__init__(self, name=name, enum=enum, enumdict=enumdict, cleanup=cleanup, incremental=True, persistant=persistant)
		elif parent == "range":
			self.__class__ = RangeVar
			RangeType.__init__(self, name=name, minmax=minmax, cleanup=cleanup, incremental=True, persistant=persistant)
		else:
			raise ValueError("unknown type: %s"%parent)
		self.addOrSame("persistent", ispersistent)
		if not incremental:
			self.finalize()

		r = Registry()
		r.registerVariable(self)

