
from lib.singleton import Singleton
from lib.validator import ValidationError
from state import State
from xml.dom.minidom import Element

class RangeType(State):
	"""
		A range type with a minimum and maximum
	"""

	def __init__(self, name, minmax=None, cleanup=False, incremental=False, persistant=True):
		State.__init__(self, name)
		t = self.get("type")
		if (t is not None) and (t != "range"):
			raise ValueError("%s not a range (%s)"%(self.prefix,t))
		self.incremental = incremental
		self.persistant = persistant
		if cleanup:
			self._unpersist()
		if (minmax is None):
			self._loadFromDB()
			persistant = False
		else:
			self._loadFromArgs(minmax)
		if persistant:
			self.persist(not incremental)

	def _checkRange(self,minmax):
		minkey = minmax[0]
		maxkey = minmax[1]
		if (type(minkey) != int ) or (type(maxkey) != int) or (minkey > maxkey):
				raise ValueError("invalid range: %s"%(minmax,))
		return (minkey,maxkey)

	def _loadFromArgs(self, minmax):
		(minkey,maxkey) = self._checkRange(minmax)
		self.minkey = minkey
		self.maxkey = maxkey
		if not self.incremental:
			self.checkSame()

	def checkSame(self):
			t = self.get("type")
			if (t is not None) and (t != "range"):
				raise ValueError("%s not a range (%s)"%(self.prefix,t))
			minkey = self.get("min")
			if (minkey is not None) and (minkey != self.minkey):
				raise ValueError("%s min db (%s) != arg (%u)"%(self.prefix,minkey,self.minkey))
			maxkey = self.get("max")
			if (maxkey is not None) and (maxkey != self.maxkey):
				raise ValueError("%s min db (%s) != arg (%u)"%(self.prefix,maxkey,self.minkey))

	def persist(self,check=True):
		if check:
			self.checkSame()
		self.set("type","range")
		if self.minkey is None:	
			return
		self.set("min",self.minkey)
		self.set("max",self.maxkey)

	def finalize(self):
		self.incremental = False

	def _loadFromDB(self):
		t = self.get("type")
		if (t is not None) and (t != "range"):
			raise ValueError("%s not a range (%s)"%(self.prefix,t))
		minkey = self.get("min")
		if minkey is None:
			if not self.incremental:
				raise ValueError("%s nonincremental empty range"%self.prefix)
			return
		self.minkey = minkey
		maxkey = self.get("max")
		self.maxkey = maxkey

	def _unpersist(self):
		self.remove("min")
		self.remove("max")
		self.remove("type")

	def modify(self, minmax):
		if not self.incremental:
			raise ValueError("nonincremental range")
		self._loadFromArgs(minmax)
		if self.persistant:
			self.persist(not self.incremental)
			
	def validate(self, value):
		if value < self.minkey or value > self.maxkey:
				raise ValidationError("%s%s not in accepted values"%(self.prefix, value))
		return True
	
	def boundaries(self):
		return (self.minkey,self.maxkey)

	def toDom(self):
		r = Element("range")
		r.setAttribute("name",self.prefix[:-1])
		r.setAttribute("minkey",str(self.minkey))
		r.setAttribute("maxkey",str(self.maxkey))
		return r

