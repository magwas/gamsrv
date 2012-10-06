#!/usr/bin/python

from xml.dom.minidom import Element
from lib.ifaced import Ifaced
from persistence.state import State
from srv.registry import Registry

class Phase(Ifaced,State):
	"""
	The game phase is the "atomic unit" of a gameplay.
	It have inputs, states and outputs.
	It validates the inputs before playing.
		
	"""

	def __init__(self):
		r = Registry()
		r.registerPhase(self)
		allvars = set(self.accounts).union(set(self.inputs)).union(set(self.outputs))
		self.variables = {}
		for varname in allvars:
			var = r.getVariableByName(varname)
			self.variables[var.getId()] = var
		State.__init__(self,self._name)
		# redundant self.addOrSame("variables",sorted(self.variables.keys)))
		self.addOrSame("accounts",sorted(self.accounts))
		self.addOrSame("inputs",sorted(self.inputs))
		self.addOrSame("outputs",sorted(self.outputs))

	#virtual
	def play(self, state):
		"""
		This method should be implemented by the actual gamephase.
		The state and outpt variables should be computed from the input and state variables.
		Stateand output should conform to the domain of their respective types.
		"""
		raise NotImplementedError

	#virtual
	def validate(self, state):
		"""
		This method should be implemented by the actual game phase
		The validate method is used to tell whether a phase is allowed to commence.
		The method should examine the inputs, whether they are allowed value/combination
		for the state of the game. It can use the states for this.
		This method SHOULD NOT MODIFY anything.
		If the phase is not allowed to commence, an exception should be raised.
		The validate method can assume that the inputs have already been examined for domain by the validators of the respective types.
		"""
		raise NotImplementedError

	def toDom(self):
		r = Element("phase")
		r.setAttribute("name",self._name)
		reg = Registry()
		for n in self.variables.keys():
			i = reg.getVariableById(n).getName()
			g=Element("variable")
			g.setAttribute("id",str(i))
			if i in self.accounts:
				g.setAttribute("account","true")
			if i in self.inputs:
				g.setAttribute("input","true")
			if i in self.outputs:
				g.setAttribute("output","true")
			r.appendChild(g)
		return r

