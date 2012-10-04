import pylibmc

from srv.config import mcdbs

class State:
	def __init__(self,prefix):
		self.client=pylibmc.client.Client(mcdbs)
		self.prefix=prefix+':'
		self.debug=False

	def get(self,key):
		r=self.client.get("%s:%s"%(self.prefix,key))
		if self.debug:
			print "%s get %s=%s"%(self.prefix,key,r)
		return r

	def set(self,key,value):
		if self.debug:
			print "%s set %s=%s"%(self.prefix,key,value)
		return self.client.set("%s:%s"%(self.prefix,key),value)

	def add(self,key,value):
		if self.debug:
			print "%s add %s=%s"%(self.prefix,key,value)
		return self.client.add("%s:%s"%(self.prefix,key),value)

	def remove(self,key):
		if self.debug:
			print "%s remove %s"%(self.prefix,key)
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

