#!/usr/bin/python

import unittest

from srv.simpletype import SimpleType, ValidationError

class TestSimpleType(unittest.TestCase):

	def test_simpletype(self):
		t1 = SimpleType("test:simpletype:range",minmax=(1,3))
		t2 = SimpleType("test:simpletype:enum",enum=('one','three','two'))
		t3 = SimpleType("test:simpletype:valuedenum",enumdict={'Three':42, 'One':-1, 'Two': 22})
		t4 = SimpleType("test:simpletype:valuedenum")

		#these should not raise an exception
		SimpleType("test:simpletype:range",minmax=(1,3))
		SimpleType("test:simpletype:enum",enum=('one','three','two'))

		with self.assertRaises(ValueError):
			SimpleType("test:simpletype:range",minmax=(1,2))
			SimpleType("test:simpletype:enum",enum=('one','thRee','two'))
			SimpleType("test:simpletype:valuedenum",enumdict={'ThRee':42, 'One':-1, 'Two': 22})

		self.assertTrue(t1.validate(3))
		self.assertTrue(t1.validate(1))
		self.assertTrue(t1.validate(2))
		self.assertEqual(t1.valueList(),[1,2,3])
		self.assertRaises(ValueError,t1.stringFor,1)
		self.assertRaises(ValidationError,t1.stringFor,0)
		self.assertRaises(ValidationError,t1.validate,0)
		self.assertRaises(ValidationError,t1.validate,4)

		self.assertEqual(t2.stringFor(0),'one')
		self.assertEqual(t2.intFor('one'),0)
		print t2.valueList()
		self.assertEqual(t2.valueList(),[0,1,2])
		self.assertTrue(t2.validate(0))
		self.assertTrue(t2.validate(1))
		self.assertTrue(t2.validate(2))
		self.assertRaises(ValidationError,t2.validate,-1)
		self.assertRaises(ValidationError,t2.validate,3)

		self.assertTrue(t3.validate(-1))
		self.assertTrue(t3.validate(42))
		self.assertTrue(t3.validate(22))
		self.assertEqual(t3.valueList(),[-1,22,42])
		self.assertRaises(ValueError,t3.stringFor,1)
		self.assertEqual(t3.stringFor(-1),'One')
		self.assertEqual(t3.intFor('Two'),22)
		self.assertRaises(ValidationError,t3.validate,1)
		
		self.assertTrue(t4.validate(-1))
		self.assertTrue(t4.validate(42))
		self.assertTrue(t4.validate(22))
		self.assertEqual(t4.valueList(),[-1,22,42])
		self.assertRaises(ValueError,t4.stringFor,1)
		self.assertEqual(t4.stringFor(-1),'One')
		self.assertEqual(t4.intFor('Two'),22)
		self.assertRaises(ValidationError,t4.validate,1)

	def tearDown(self):
		SimpleType("test:simpletype:range")._unpersist()
		SimpleType("test:simpletype:enum")._unpersist()
		SimpleType("test:simpletype:valuedenum")._unpersist()

if __name__ == '__main__':
	unittest.main()

