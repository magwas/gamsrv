#!/usr/bin/python

import unittest

from persistence.rangetype import RangeType, ValidationError

from xml.dom.minidom import parseString

class TestRangeType(unittest.TestCase):

	def test_range(self):
		t1 = RangeType("test:rangetype:first",minmax=[1,2])
		n1 = parseString('<range maxkey="2" minkey="1" name="test:rangetype:first"/>').childNodes[0]
		self.assertEqual(t1.toDom().toxml(),n1.toxml())
		RangeType("test:rangetype:first",minmax=[1,2])
		with self.assertRaises(ValueError):
			RangeType("test:rangetype:first",minmax=[1,3])
			RangeType("test:rangetype:first",minmax=[0,2])
			RangeType("test:rangetype:first",minmax=[0,3])

		t2 = RangeType("test:rangetype:first")
		self.assertEqual(t1.toDom().toxml(),t2.toDom().toxml())

		self.assertTrue(t2.validate(1))
		self.assertTrue(t2.validate(2))
		with self.assertRaises(ValueError):
			t2.validate(-1)
			t2.validate(0)
			t2.validate(3)
			t2.validate(10)
			t2.validate(-10)


		return

if __name__ == '__main__':
	unittest.main()

