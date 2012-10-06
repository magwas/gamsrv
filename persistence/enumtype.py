
from lib.validator import ValidationError
from state import State
from xml.dom.minidom import Element

class EnumType(State):
	"""
		A type which can have predefined integer keys, and there is a name for each of the values
		we store the min and max value of the keys, and the name for each of the existing keys
		An EnumType can be defined either with a list of values (where keys will be autogeerated from 0),
		or with a dictionary.
		The initialisation from db is done by exhausting the {min,max} range, so be careful with sparse enums!
		In order to spot interface changes, we require the key/name pairs not to change wrt the value in storage.
		For those enums which are not defined incrementally, we can also require that min and max should not change.
		For enums used for non-interface purposes, we can request a cleanup before definition.
	"""

	def __init__(self, name, enum=None, enumdict=None, cleanup=False, incremental=False, persistant=True):
		State.__init__(self, name)
		t = self.get("type")
		if (t is not None) and (t != "enum"):
			raise ValueError("%s not an enum (%s)"%(self.prefix,t))
		self.incremental = incremental
		self.persistant = persistant
		if enum is not None:
			if enumdict is not None:
				raise ValueError("either enum or enumdict. not both")
			enumdict = {}
			n = 0
			for item in enum:
				enumdict[n] = item
				n += 1
		self._checkdict(enumdict)
		if cleanup:
			self._unpersist()
		self._loadFromArgs(enumdict)
		if (self.enumdict is None):
			self._loadFromDB()
			persistant = False
		if persistant:
			self.persist(not incremental)

	def _checkdict(self,enumdict):
		if enumdict is None:
			return True
		for k in enumdict.keys():
			if type(k) != int:
				raise ValueError("key should be int")
		return True

	def _loadFromArgs(self, enumdict):
		self.enumdict = enumdict
		if enumdict == None:
			return
		self._getMinMax()
		if not self.incremental:
			self.checkSame()

	def checkSame(self):
			t = self.get("type")
			if (t is not None) and (t != "enum"):
				raise ValueError("%s not an enum (%s)"%(self.prefix,t))
			minkey = self.get("min")
			if (minkey is not None) and (minkey != self.minkey):
				raise ValueError("%s min db (%s) != arg (%u)"%(self.prefix,minkey,self.minkey))
			maxkey = self.get("max")
			if (maxkey is not None) and (maxkey != self.maxkey):
				raise ValueError("%s min db (%s) != arg (%u)"%(self.prefix,maxkey,self.minkey))
			if (minkey is not None) and (maxkey is not None):
				for i in range(minkey,maxkey+1):
					n = self.get(i)
					if n is not None and not self.enumdict.has_key(i):
						raise ValueError("%s key %u is empty in initialisation and %s in db"%(self.prefix, i, n))

	def persist(self,check=True):
		if check:
			self.checkSame()
		self.set("type","enum")
		if self.enumdict is None:	
			return
		self.set("min",self.minkey)
		self.set("max",self.maxkey)
		for k,v in self.enumdict.items():
			self.set(k,v)

	def finalize(self):
		self.incremental = False

	def _loadFromDB(self):
		t = self.get("type")
		if (t is not None) and (t != "enum"):
			raise ValueError("%s not an enum (%s)"%(self.prefix,t))
		minkey = self.get("min")
		if minkey is None:
			if not self.incremental:
				raise ValueError("%s nonincremental empty enum"%self.prefix)
			self.enumdict = None
			return
		self.enumdict={}
		self.minkey = minkey
		maxkey = self.get("max")
		self.maxkey = maxkey
		if (minkey is not None) and (maxkey is not None):
			for i in range(self.minkey,self.maxkey+1):
				n = self.get(i)
				if n is not None:
					self.enumdict[i] = n

	def _unpersist(self):
		minkey = self.get("min")
		if minkey is None:
			return
		maxkey = self.get("max")
		for i in range(minkey,maxkey+1):
			self.remove(i)
		self.remove("min")
		self.remove("max")
		self.remove("type")


	def _getMinMax(self):
			keylist = sorted(self.enumdict.keys())
			self.minkey = keylist[0]
			self.maxkey = keylist[-1]
		
	def registerOne(self, name, value=None):
		if not self.incremental:
			raise ValueError("nonincremental enum")
		if (value is not None) and (type(value) != int):
			raise ValueError("value should be int")
		if self.enumdict is None:
			if value is None:
				value = 0
		else:
			if value is None:
				value = self.maxkey + 1
			if self.enumdict.has_key(value) and not (self.enumdict[value] == name):
				raise ValueError("%s: enum is unmodifiable (old=%s, new=%s for %s)"%(self.prefix,self.enumdict[value], name,value))
		if self.enumdict is None:
			self.enumdict = {}
		self.enumdict[value] = name
		self._getMinMax()
		if self.persistant:
			self.persist(not self.incremental)
			
	def validate(self, value):
		if (self.enumdict is None) or ( not self.enumdict.has_key(value) ):
				raise ValidationError("%s%s not in accepted values"%(self.prefix, value))
		return True
	
	def stringFor(self, value):
			self.validate(value)
			return self.enumdict[value]

	def intFor(self, name):
			if (self.enumdict is not None):
				for k, v in self.enumdict.items():
					if v == name:
						return k
			raise ValidationError("%s %s not in accepted names"%(self.prefix, name))

	def valueList(self):
		if self.enumdict is not None:
			return sorted(self.enumdict.keys())
		else:
			return []

	def toDom(self):
		r = Element("enum")
		r.setAttribute("name",self.prefix[:-1])
		if self.enumdict is None:
			return r
		for k in sorted(self.enumdict.keys()):
			i = Element("value")
			i.setAttribute("id",str(k))
			i.setAttribute("name",self.enumdict[k])
			r.appendChild(i)
		return r

