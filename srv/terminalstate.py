from lib.validator import ValidationError
from persistence.state import State
from srv.registry import Registry
from lib import log

class PhaseState(object):
	"""
		The phase state holds the state seen by a phase
		FIXME: getattr, setattr, getitem and setitem 
	"""
	def __init__(self,variables):
		vv = {}
		for k,v in variables.items():
			vv[k] = v.getName()
		log.debug("phasestate", 6, variables=vv)
		object.__setattr__(self, "__variables", vv)
		object.__setattr__(self, "__dict", {})

	def __setattr__(self,name,value):
		log.debug("phasestate", 6, name=name,value=value)
		thevars = object.__getattribute__(self,"__variables")
		log.debug("phasestate",7, thevars=thevars)
		if not name in thevars.values():
			raise KeyError("%s not a variable for this phase")
		thedict = object.__getattribute__(self,"__dict")
		thedict[name] = value

	def __getattribute__(self,name):
		thedict = object.__getattribute__(self,"__dict")
		if not thedict.has_key(name):
			raise KeyError("%s not a variable for this phase"%name)
		r = thedict[name]
		if r is None:
			r = 0
		log.debug("phasestate", 6, name=name, value=r)
		return r

	__setitem__ = __setattr__
	__getitem__ = __getattribute__

	def __str__(self):
		thedict = object.__getattribute__(self,"__dict")
		return "%s"%(thedict)

class TerminalState(State):
	"""
	The terminalstate is handling the state of a terminal.
	On init it initialises persistence, checks the right of the terminal to play, and reads up what is needed to read up, and 
	WHen a phase is initialised (phaseinit), it validates the input and fills in the phasestate with it and accounts (initialising values if needed)
		The rights of the terminal to play the given game is also checked.
	After a phase ran (afterphase), the output and accounts are validated in phasestate, incorporated back to terminalstate and persisted.
	
	"""

	def __init__(self, terminalid):
		State.__init__(self,"terminal/%s"%terminalid)
		if not self.get("enabled"):
			raise ValidationError("terminal %s is disabled"%terminalid)
		self.terminalid = terminalid
		
	def phaseinit(self, game, phase, inputs):
		reg = Registry()
		if not self.get("gameenabled/%s"%game.getId()):
			raise ValidationError("game %s for terminal %s is disabled"%(game.getName(),self.terminalid))
		phasestate = PhaseState(phase.variables)
		logstate = {}
		for (k,vobj) in phase.variables.items():
			v = vobj.getName()
			log.debug("phaseinit",6,key=k,value=v)
			if v in phase.inputs:
				if not inputs.has_key(k):
					raise ValidationError("input for phase %s does not contain %s"%(phase.getName(),v))
				var = reg.getVariableById(k)
				value = inputs[k]
				var.validate(value)
				phasestate[v] = value
				logstate[v] = value
			if v in phase.accounts:
				logstate[v] = phasestate[v] = self.get("accounts/%s"%v)
		log.log(log.LOG_INFO,"phaseinit",self.terminalid,phase.getName(),**logstate)
		return phasestate

	def afterphase(self, game, phase, phasestate):
		reg = Registry()
		outstate = {}
		logstate = {}
		for (k,vobj) in phase.variables.items():
			v = vobj.getName()
			if v in phase.accounts:
				var = reg.getVariableById(k)
				value = phasestate[v]
				var.validate(value)
				self.set("accounts/%s"%v,value)
			if v in phase.outputs:
				value = phasestate[v]
				var = reg.getVariableById(k)
				var.validate(value)
				outstate[k] = value
				logstate[v] = value
		log.log(log.LOG_INFO,"afterphase",self.terminalid,phase.getName(),**logstate)
		return outstate
				
