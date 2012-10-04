#!/usr/bin/python

class Ifaced:
	#virtual private
	_name = None
	#virtual private
	_idnum = None

	def getName(self):
		return self._name

	def getId(self):
		return self._idnum

