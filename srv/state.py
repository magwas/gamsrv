import pylibmc

from srv.config import mcdbs

class State:
	def __init__(self,prefix):
		self.client=pylibmc.client.Client(mcdbs)
		self.prefix=prefix+':'

	def get(self,key):
		return self.client.get(self.prefix+key)

	def set(self,key,value):
		return self.client.set(self.prefix+key,value)

	def add(self,key,value):
		return self.client.add(self.prefix+key,value)

