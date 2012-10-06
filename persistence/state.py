import pylibmc

from srv.config import mcdbs
from lib.log import debug

class State:
	def __init__(self,prefix):
		self.client=pylibmc.client.Client(mcdbs)
		self.prefix=prefix+':'

	def get(self,key):
		r=self.client.get("%s:%s"%(self.prefix,key))
		debug("persistence",7,operation="get", prefix=self.prefix, key=key, value=r)
		return r

	def set(self,key,value):
		debug("persistence", 7, operation="set", prefix=self.prefix, key=key, value=value)
		return self.client.set("%s:%s"%(self.prefix,key),value)

	def add(self,key,value):
		debug("persistence", 7, operation="add", prefix=self.prefix, key=key, value=value)
		return self.client.add("%s:%s"%(self.prefix,key),value)

	def remove(self,key):
		debug("persistence", 7, operation="remove", prefix=self.prefix, key=key)
		return self.client.delete("%s:%s"%(self.prefix,key))

	def addOrSame(self,key,value):
		v = self.get(key)
		if v == value:
			pass
		elif v == None:
			self.add(key,value)
		else:
			raise ValueError("%s%s=%s != %s"%(self.prefix,key,v,value))
		return v

