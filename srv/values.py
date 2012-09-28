
from lib.singleton import Singleton
from validator import ValidationError

class Values(Singleton):
	def __init__(self):
		self.valhash = {}

	def register(self,valdict):
		for k,v in valdict.items():
			self.valhash[k] = v

	def validate(self,key,value):
		if not self.valhash.has_key(key):
			raise ValidationError("key %d does not exists"%key)
		name, minval,maxval = self.valhash[key]
		if minval > value:
			raise ValidationError("value %d for key %s is less than minimal value of %d"%(value,name,minval))
		if maxval < value:
			raise ValidationError("value %d for key %s is greater than maximal value of %d"%(value,name,maxval))
		return True
	
