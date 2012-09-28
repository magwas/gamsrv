#!/usr/bin/python

import unittest

from srv.values import Values, ValidationError

valdict= {
1: ("test_1",3,4),
2: ("test_2",0,0),
3: ("test_3",-1,10),
4: ("test_4",-1000000,1000000),
}

class TestValues(unittest.TestCase):

	def setUp(self):
		self.v = Values()
		self.v.register(valdict)

	def test_validate(self):
		self.assertTrue(self.v.validate(1,3))
		self.assertTrue(self.v.validate(1,4))
		self.assertTrue(self.v.validate(2,0))
		self.assertTrue(self.v.validate(3,-1))
		self.assertTrue(self.v.validate(3,0))
		self.assertTrue(self.v.validate(3,8))
		self.assertTrue(self.v.validate(3,10))
		self.assertTrue(self.v.validate(4,10))
		self.assertTrue(self.v.validate(4,0))
		self.assertTrue(self.v.validate(4,1000000))
		self.assertTrue(self.v.validate(4,1000000))
		self.assertRaises(ValidationError, self.v.validate,1,5)
		self.assertRaises(ValidationError, self.v.validate,1,-1)
		self.assertRaises(ValidationError, self.v.validate,2,1)
		self.assertRaises(ValidationError, self.v.validate,2,-301)
		self.assertRaises(ValidationError, self.v.validate,3,-2)
		self.assertRaises(ValidationError, self.v.validate,3,11)
		self.assertRaises(ValidationError, self.v.validate,4,-1000001)
		self.assertRaises(ValidationError, self.v.validate,4,1000001)

if __name__ == '__main__':
	unittest.main()

