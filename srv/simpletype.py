
from lib.singleton import Singleton
from validator import ValidationError
from srv.config import maxenumlen
from srv.state import State

class SimpleType(State):

	def __init__(self, name, minmax=None, enum=None, enumdict=None):
		State.__init__(self,name)
		if minmax:
			if enum or enumdict:
				raise ValueError
			self.addOrSame("min",minmax[0])
			self.addOrSame("max",minmax[1])
		elif enum:
			if enumdict:
				raise ValueError
			self.addOrSame("min",0)
			self.addOrSame("max",len(enum)-1)
			n = 0
			for item in enum:
				self.addOrSame("%u.name"%n,item)
				n += 1
		elif enumdict:
			if len(enumdict.keys()) > maxenumlen:
				raise ValueError
			self.addOrSame("valuelist",sorted(enumdict.values()))
			for k,v in enumdict.items():
				self.addOrSame("%u.name"%v,k)
		#reread from db to make sure
		self.min = self.get("min")
		self.max = self.get("max")
		self.valuelist = self.get("valuelist")
		if self.min is not None:
			if self.get("%u.name"%self.min) is not None:
				self.enumdict = {}
				for i in range(self.min,self.max+1):
					self.enumdict[i] = self.get("%u.name"%i)
			else:
				self.enumdict = None
		elif self.valuelist is not None:
			self.enumdict = {}
			for i in self.valuelist:
				self.enumdict[i] = self.get("%u.name"%i)
		else:
			raise NotImplementedError("State problem")
			
	def _unpersist(self):
		self.remove("min")
		self.remove("max")
		self.remove("valuelist")
		if self.enumdict is not None:
			for i in self.enumdict.keys():
				self.remove("%u.name"%i)

	def register(self,valdict):
		for k,v in valdict.items():
			self.valhash[k] = v

	def validate(self,value):
		if self.min is not None:
			if value > self.max or value < self.min:
				raise ValidationError("%s%s not in range"%(self.prefix,value))
		else:
			if not self.enumdict.has_key(value):
				raise ValidationError("%s%s not in accepted values"%(self.prefix,value))
		return True
	
	def stringFor(self,value):
			if (self.enumdict is None) or (not self.enumdict.has_key(value)):
				raise ValidationError("%s%s not in accepted values"%(self.prefix,value))
			return self.enumdict[value]

	def intFor(self,name):
			if (self.enumdict is not None):
				for k, v in self.enumdict.items():
					if v == name:
						return k
			raise ValidationError("%s%s not in accepted values"%(self.prefix,value))

	def valueList(self):
		if self.enumdict is not None:
			return sorted(self.enumdict.keys())
		else:
			return range(self.min,self.max+1)

